#!/usr/bin/env python3
"""Kütüphane hikâyelerini tek anlatıcılı (ElevenLabs George) videolara dönüştürür.

Her hikâye: sahne metinleri + sonda "Bu hikâyenin mesajı" (kitaptaki ana fikir, `core`).
Görüntü: sahnenin fotoğraf kesiti, titremesiz yumuşak yakınlaşma, 1280x720.
Altyazı videonun içine yazılır. Her görüntü en fazla 8 sn; uzun cümleler aynı
fotoğrafla iki sahneye bölünür. En fazla 3 dk.

Kaldığı yerden devam eder: OUT/<id>/ klasöründe tamamlanan hikâye atlanır.
Kredi biterse durur ve o ana kadar bitenleri bırakır.

  python3 scripts/build-library-narrator.py --out DIR [--limit N] [--only ID,ID]
"""
import argparse, base64, hashlib, importlib.util, json, os, shutil, subprocess, sys, urllib.error, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('nar', ROOT / 'scripts' / 'build-narrator-video.py')
nar = importlib.util.module_from_spec(spec); spec.loader.exec_module(nar)
FPS, W, H, MAX_SCENE, MAX_TOTAL, TAIL = 30, 1280, 720, 8.0, 180.0, 1.2
ORDER = ['5', '6', '7', '8', '9', '10', '11', '12', 'common', 'university']


class Quota(Exception):
    pass


def tts(text):
    body = json.dumps({'text': text, 'model_id': nar.MODEL, 'language_code': 'tr',
                       'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75}}).encode()
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{nar.VOICE_ID}/with-timestamps?output_format=mp3_44100_128',
                                 data=body, headers={'Content-Type': 'application/json', 'xi-api-key': os.environ.get('ELEVENLABS_API_KEY', 'proxy-injected')})
    for attempt in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=600))
        except urllib.error.HTTPError as e:
            msg = e.read()[:400].decode(errors='replace')
            if e.code in (401, 402) or 'quota' in msg:
                raise Quota(msg)
            if attempt == 3:
                raise RuntimeError(f'{e.code} {msg}')
        except (urllib.error.URLError, TimeoutError):
            if attempt == 3:
                raise
        import time; time.sleep(5 * (attempt + 1))


def photo_image(photo, cache):
    dest = cache / f"{photo['key']}.png"
    if not dest.exists():
        x, y, w, h = photo['rect']
        im = Image.open(ROOT / photo['src']).convert('RGB').crop((x, y, x + w, y + h))
        tw, th = (w, round(w * 9 / 16)) if w * 9 / 16 <= h else (round(h * 16 / 9), h)
        l, t = (w - tw) // 2, (h - th) // 2
        im.crop((l, t, l + tw, t + th)).resize((1536, 864), Image.Resampling.LANCZOS).save(dest)
    return dest


def build(story, photos, out, cache):
    sid = story['id']; d = out / sid
    if (d / 'done.json').exists():
        return json.loads((d / 'done.json').read_text())
    d.mkdir(parents=True, exist_ok=True)
    segs = [{'text': s['text'].strip(), 'photo': s['photo']} for s in story['scenes'] if s['text'].strip()]
    if story.get('core'):
        segs.append({'text': 'Bu hikâyenin mesajı: ' + story['core'].strip(), 'photo': 'reflect' if 'reflect' in photos else segs[-1]['photo']})
    text = ' '.join(s['text'] for s in segs)
    cachef = d / 'tts.json'
    if cachef.exists() and json.loads(cachef.read_text())['text'] == text:
        r = json.loads(cachef.read_text())
    else:
        r = tts(text); r['text'] = text
        cachef.write_text(json.dumps(r))
    (d / 'anlatim.mp3').write_bytes(base64.b64decode(r['audio_base64']))
    al = r['alignment']; chars, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    assert ''.join(chars) == text
    audio_len = nar.duration(d / 'anlatim.mp3')
    if audio_len + TAIL > MAX_TOTAL:
        raise RuntimeError(f'{sid}: {audio_len:.0f} sn, 3 dakikayı aşıyor')
    # Segment sınırları
    pos, spans = 0, []
    for s in segs:
        spans.append((pos, pos + len(s['text']) - 1)); pos += len(s['text']) + 1
    bounds = [0.0] + [(en[a[1]] + st[b[0]]) / 2 for a, b in zip(spans, spans[1:])] + [audio_len + TAIL]
    # Uzun segmentleri kelime sınırından böl (aynı fotoğraf)
    shots, cues = [], []
    spaces_all = [j for j, c in enumerate(chars) if c == ' ']
    for i, s in enumerate(segs):
        t0, t1 = bounds[i], bounds[i + 1]
        a0, a1 = spans[i]
        spaces = [j for j in spaces_all if a0 < j < a1]
        n = max(1, int(-(-(t1 - t0) // 7.0)))
        while True:
            picks = []
            for k in range(1, n):
                target = t0 + (t1 - t0) * k / n
                cand = [j for j in spaces if j not in picks]
                if cand:
                    picks.append(min(cand, key=lambda j: abs(st[j] - target)))
            picks = sorted(set(picks))
            cuts = [t0] + [st[j] for j in picks] + [t1]
            if all(b - a <= MAX_SCENE - 0.1 for a, b in zip(cuts, cuts[1:])) or n > 12:
                break
            n += 1
        idx = [a0] + [j + 1 for j in picks] + [a1 + 1]
        for k in range(len(cuts) - 1):
            shots.append((cuts[k], cuts[k + 1], s['photo']))
            cues.append((cuts[k], min(cuts[k + 1], audio_len + .3), text[idx[k]:idx[k + 1]].strip()))
    frames = [round(a * FPS) for a, _, _ in shots] + [round(shots[-1][1] * FPS)]
    assert all(frames[k + 1] - frames[k] <= MAX_SCENE * FPS + 1 for k in range(len(shots))), sid
    def ts(t):
        return f'{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{t % 60:06.3f}'
    (d / 'altyazi.vtt').write_text('WEBVTT\n\n' + '\n'.join(f'{k + 1}\n{ts(a)} --> {ts(b)}\n{c}\n' for k, (a, b, c) in enumerate(cues)))
    silent = d / '.sessiz.mp4'
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-an', str(silent)], stdin=subprocess.PIPE)
    for k, (_, _, ph) in enumerate(shots):
        nar.render_scene(enc.stdin, photo_image(photos[ph] | {'key': ph}, cache), frames[k + 1] - frames[k], zoom_in=bool(k % 2 == 0), zoom=0.05)
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError('encode')
    total = frames[-1] / FPS
    video = d / f'{sid}.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(silent), '-i', str(d / 'anlatim.mp3'),
                    '-filter_complex', f"[0:v]subtitles=f={d / 'altyazi.vtt'}:force_style='{nar.SUB_STYLE}'[v];[1:a]apad=whole_dur={total:.3f}[a]",
                    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '27', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '96k', '-t', f'{total:.3f}', '-movflags', '+faststart', '-metadata', 'title=' + story['title'], str(video)], check=True)
    silent.unlink()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '1', '-i', str(video), '-frames:v', '1', '-vf', 'scale=640:-2', str(d / 'kapak.jpg')], check=True)
    row = {'id': sid, 'title': story['title'], 'grade': story.get('grade', ''), 'topic': story.get('topic', ''), 'sceneCount': len(shots),
           'duration': round(total, 3), 'bytes': video.stat().st_size, 'sha256': hashlib.sha256(video.read_bytes()).hexdigest(),
           'voice': 'ElevenLabs George (eleven_v4_turbo)', 'format': 'single-narrator', 'message': story.get('core', '')}
    (d / 'done.json').write_text(json.dumps(row, ensure_ascii=False, indent=1))
    (d / 'tts.json').unlink()  # büyük önbellek; ses ve altyazı yeterli
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--limit', type=int)
    ap.add_argument('--only')
    ap.add_argument('--shard', default='0/1', help='i/n: yalnız i. parçayı üret')
    a = ap.parse_args()
    job = json.loads(subprocess.check_output(['node', 'scripts/export-video-jobs.cjs'], cwd=ROOT))
    stories = sorted(job['stories'], key=lambda s: (ORDER.index(s.get('grade', 'common')) if s.get('grade', 'common') in ORDER else 99, s['id']))
    if a.only:
        ids = set(a.only.split(',')); stories = [s for s in stories if s['id'] in ids]
    i, n = map(int, a.shard.split('/')); stories = stories[i::n]
    if a.limit:
        stories = stories[:a.limit]
    cache = a.out / '.foto'; cache.mkdir(parents=True, exist_ok=True)
    done = 0
    for s in stories:
        try:
            row = build(s, job['photos'], a.out, cache)
            done += 1
            print(f"OK {done}/{len(stories)} {s['id']} {row['duration']:.0f}s {row['bytes'] // 1024}KB", flush=True)
        except Quota as e:
            print('QUOTA', s['id'], e, flush=True); break
        except Exception as e:
            print('FAIL', s['id'], repr(e)[:300], flush=True)
    print('FINISHED', done, flush=True)


if __name__ == '__main__':
    main()
