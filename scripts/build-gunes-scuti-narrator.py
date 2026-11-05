#!/usr/bin/env python3
"""Güneş ve UY Scuti · tek anlatıcılı sürüm.

Adımlar:
  1. ElevenLabs (George, eleven_v4_turbo) ile tek parça anlatım + karakter zamanlaması.
  2. Her görselin süresini anlatımdaki cümle sınırlarından hesaplar (en fazla 8 sn).
  3. Hafif kamera hareketiyle 1280x720, 30 fps MP4 oluşturur.
  4. Sahne sesleri, altyazı, CSV, JSON ve ZIP dosyalarını yazar.

Kullanım:
  python3 scripts/build-gunes-scuti-narrator.py --images DIR --out DIR [--tts]
  --images : video-medya dalındaki gunes-scuti/gorseller klasörü
  --out    : çıktı (video-medya dalına anlatici-v2/gunes-scuti olarak eklenir)
  --tts    : ElevenLabs'tan yeni kayıt ister; yoksa out/anlatim.mp3 ve
             out/.alignment.json önbelleği kullanılır.
API anahtarı ortamdaki ağ vekili tarafından eklenir; ELEVENLABS_API_KEY
tanımlıysa o kullanılır.
"""
import argparse, base64, csv, hashlib, json, os, shutil, subprocess, sys, urllib.error, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'flow-hazirlik' / 'gunes-scuti'
SEGMENTS = SITE / 'anlatim-sahneleri.json'
VOICE_ID, VOICE_NAME, MODEL = 'JBFqnCBsd6RMkjVDRZzb', 'George', 'eleven_v4_turbo'
FPS, W, H, MAX_SECONDS, TAIL = 30, 1280, 720, 8, 1.5
VIDEO_NAME = 'gunes-scuti-tek-anlatici.mp4'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)]))


def tts(text, out):
    body = json.dumps({'text': text, 'model_id': MODEL, 'language_code': 'tr',
                       'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75}}).encode()
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps?output_format=mp3_44100_128',
        data=body, headers={'Content-Type': 'application/json', 'xi-api-key': os.environ.get('ELEVENLABS_API_KEY', 'proxy-injected')})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=600))
    except urllib.error.HTTPError as e:
        sys.exit(f'ElevenLabs hatası {e.code}: {e.read()[:600].decode(errors="replace")}')
    (out / 'anlatim.mp3').write_bytes(base64.b64decode(r['audio_base64']))
    (out / '.alignment.json').write_text(json.dumps({'text': text, 'alignment': r['alignment']}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--images', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--tts', action='store_true')
    a = ap.parse_args()
    out = a.out
    out.mkdir(parents=True, exist_ok=True)
    segs = json.loads(SEGMENTS.read_text())
    text = ' '.join(s['text'] for s in segs)
    if a.tts:
        tts(text, out)
    cache = json.loads((out / '.alignment.json').read_text())
    if cache['text'] != text:
        sys.exit('Önbellekteki kayıt güncel metne ait değil; --tts ile yeniden üretin.')
    al = cache['alignment']
    chars, starts, ends = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    assert ''.join(chars) == text, 'Zamanlama metni eşleşmiyor'
    audio_len = duration(out / 'anlatim.mp3')

    # Sahne sınırları: önceki cümlenin son harfi ile sonraki cümlenin ilk harfi arasındaki sessizliğin ortası.
    offsets, pos = [], 0
    for s in segs:
        offsets.append((pos, pos + len(s['text']) - 1))
        pos += len(s['text']) + 1
    bounds = [0.0]
    for (_, prev_end), (next_start, _) in zip(offsets, offsets[1:]):
        bounds.append((ends[prev_end] + starts[next_start]) / 2)
    total = audio_len + TAIL
    bounds.append(total)
    frames = [round(b * FPS) for b in bounds]
    too_long = [(i + 1, (frames[i + 1] - frames[i]) / FPS) for i in range(len(segs)) if frames[i + 1] - frames[i] > MAX_SECONDS * FPS]
    if too_long:
        sys.exit(f'8 saniyeyi aşan sahneler: {too_long}. Bu cümleleri kısaltıp yeniden üretin.')

    for d in ('gorseller', 'sesler', '.klipler'):
        (out / d).mkdir(exist_ok=True)
    scenes, clips = [], []
    for i, s in enumerate(segs):
        n = i + 1
        img = out / 'gorseller' / f'{n:02d}-gorsel.jpg'
        shutil.copyfile(a.images / f"{s['sourceScene']:02d}-gorsel.jpg", img)
        f0, f1 = frames[i], frames[i + 1]
        st, en = f0 / FPS, f1 / FPS
        count = f1 - f0
        # Dönüşümlü hafif yakınlaşma / uzaklaşma.
        z = f"1+0.06*on/{count}" if n % 2 else f"1.06-0.06*on/{count}"
        clip = out / '.klipler' / f'{n:02d}.mp4'
        run('ffmpeg', '-y', '-loop', '1', '-framerate', str(FPS), '-i', str(img),
            '-vf', f"scale={W*2}:{H*2},zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},format=yuv420p",
            '-frames:v', str(count), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-an', str(clip))
        clips.append(clip)
        audio_end = min(en, audio_len)
        sound = out / 'sesler' / f'{n:02d}-anlatici.mp3'
        run('ffmpeg', '-y', '-ss', f'{st:.3f}', '-to', f'{audio_end:.3f}', '-i', str(out / 'anlatim.mp3'), '-c:a', 'libmp3lame', '-b:a', '128k', str(sound))
        (out / f'{n:02d}-seslendirme.txt').write_text(s['text'] + '\n')
        scenes.append({'number': n, 'speaker': 'Anlatıcı', 'text': s['text'], 'chapter': s['chapter'],
                       'sourceScene': s['sourceScene'], 'imageFile': f'gorseller/{n:02d}-gorsel.jpg', 'image': f'gorseller/{n:02d}-gorsel.jpg',
                       'audioFile': f'sesler/{n:02d}-anlatici.mp3', 'speechTextFile': f'{n:02d}-seslendirme.txt',
                       'startFrame': f0, 'endFrame': f1, 'startSeconds': st, 'endSeconds': en, 'durationSeconds': en - st,
                       'imageSha256': sha(img), 'audioDurationSeconds': duration(sound), 'maxSeconds': MAX_SECONDS})

    lst = out / '.klipler' / 'liste.txt'
    lst.write_text(''.join(f"file '{c.name}'\n" for c in clips))
    video = out / VIDEO_NAME
    run('ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst), '-i', str(out / 'anlatim.mp3'),
        '-filter_complex', f'[1:a]apad=whole_dur={total:.3f}[a]', '-map', '0:v', '-map', '[a]',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-t', f'{frames[-1] / FPS:.3f}', '-movflags', '+faststart', str(video))
    shutil.rmtree(out / '.klipler')

    def ts(t):
        return f'{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{t % 60:06.3f}'
    (out / 'altyazi.vtt').write_text('WEBVTT\n\n' + '\n'.join(
        f"{s['number']}\n{ts(s['startSeconds'])} --> {ts(min(s['endSeconds'], audio_len + .3))}\n{s['text']}\n" for s in scenes))
    with open(out / 'sahne-listesi.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(['Sahne', 'Başlangıç', 'Bitiş', 'Konu', 'Anlatım', 'Görsel', 'Ses'])
        for s in scenes:
            w.writerow([s['number'], s['startSeconds'], s['endSeconds'], s['chapter'], s['text'], s['imageFile'], s['audioFile']])
    (out / 'anlatim.txt').write_text('\n\n'.join(s['text'] for s in segs) + '\n')
    for name in ('ozgun-metin.txt', 'OKU.md'):
        shutil.copyfile(SITE / name, out / name)

    data = {'id': 'gunes-scuti-kesif', 'title': 'Güneş ve UY Scuti', 'order': 2,
            'adaptation': 'Özgün metin ayrı dosyada korunur. Bu tek anlatıcılı uyarlamada bütün konu başlıkları kısaltılarak işlenmiş, bilimsel düzeltmeler korunmuştur. Bilimsel açıklamalar ve İslam inancına ilişkin yorumlar ayrılır.',
            'sourceSha256': sha(SITE / 'ozgun-metin.txt'), 'voiceName': VOICE_NAME, 'model': MODEL,
            'format': 'single-narrator', 'audioMode': 'continuous', 'speaker': 'Anlatıcı',
            'fullAudioFile': 'anlatim.mp3', 'videoFile': VIDEO_NAME, 'fps': FPS, 'frameCount': frames[-1],
            'durationSeconds': frames[-1] / FPS, 'continuousNarration': True,
            'masterAudioSha256': sha(out / 'anlatim.mp3'), 'videoSha256': sha(video), 'scenes': scenes}
    (out / 'sahneler.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

    with zipfile.ZipFile(out / 'gunes-scuti-tek-anlatici-sahneler.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file() and p.suffix != '.zip' and p.name != VIDEO_NAME and not p.name.startswith('.'):
                z.write(p, p.relative_to(out))
    print(f'Tamam: {len(scenes)} sahne, {frames[-1] / FPS:.1f} sn, en uzun sahne {max(s["durationSeconds"] for s in scenes):.2f} sn')


if __name__ == '__main__':
    main()
