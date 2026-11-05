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
SUB_STYLE = ('FontName=DejaVu Sans,Fontsize=15,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,'
             'BackColour=&H80000000,BorderStyle=1,Outline=1.2,Shadow=0.8,MarginV=20,MarginL=40,MarginR=40,Alignment=2')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)]))


def render_scene(pipe, img_path, count, zoom_in, zoom=0.06):
    """Hafif ve yumuşak yakınlaşma: kesirli kırpma kutusu + Lanczos örnekleme."""
    from PIL import Image
    src = Image.open(img_path).convert('RGB')
    sw, sh = src.size
    for k in range(count):
        p = k / max(count - 1, 1)
        p = p * p * (3 - 2 * p)  # yumuşak başlayıp yumuşak biten hareket
        z = 1 + zoom * (p if zoom_in else 1 - p)
        cw, ch = sw / z, sh / z
        x0, y0 = (sw - cw) / 2, (sh - ch) / 2
        frame = src.resize((W, H), Image.Resampling.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
        pipe.write(frame.tobytes())


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

    for d in ('gorseller', 'sesler'):
        (out / d).mkdir(exist_ok=True)
    video = out / VIDEO_NAME
    silent = out / '.sessiz.mp4'
    # Kareler Python'da piksel altı hassasiyetle hesaplanır; ffmpeg zoompan'ın
    # tam piksele yuvarlamasından doğan titreme oluşmaz.
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-an', str(silent)], stdin=subprocess.PIPE)
    scenes = []
    for i, s in enumerate(segs):
        n = i + 1
        img = out / 'gorseller' / f'{n:02d}-gorsel.jpg'
        shutil.copyfile(a.images / f"{s['sourceScene']:02d}-gorsel.jpg", img)
        f0, f1 = frames[i], frames[i + 1]
        st, en = f0 / FPS, f1 / FPS
        count = f1 - f0
        render_scene(enc.stdin, img, count, zoom_in=bool(n % 2))
        audio_end = min(en, audio_len)
        sound = out / 'sesler' / f'{n:02d}-anlatici.mp3'
        run('ffmpeg', '-y', '-ss', f'{st:.3f}', '-to', f'{audio_end:.3f}', '-i', str(out / 'anlatim.mp3'), '-c:a', 'libmp3lame', '-b:a', '128k', str(sound))
        (out / f'{n:02d}-seslendirme.txt').write_text(s['text'] + '\n')
        scenes.append({'number': n, 'speaker': 'Anlatıcı', 'text': s['text'], 'chapter': s['chapter'],
                       'sourceScene': s['sourceScene'], 'imageFile': f'gorseller/{n:02d}-gorsel.jpg', 'image': f'gorseller/{n:02d}-gorsel.jpg',
                       'audioFile': f'sesler/{n:02d}-anlatici.mp3', 'speechTextFile': f'{n:02d}-seslendirme.txt',
                       'startFrame': f0, 'endFrame': f1, 'startSeconds': st, 'endSeconds': en, 'durationSeconds': en - st,
                       'imageSha256': sha(img), 'audioDurationSeconds': duration(sound), 'maxSeconds': MAX_SECONDS})

    enc.stdin.close()
    if enc.wait():
        sys.exit('Video kodlanamadı')
    def ts(t):
        return f'{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{t % 60:06.3f}'
    (out / 'altyazi.vtt').write_text('WEBVTT\n\n' + '\n'.join(
        f"{s['number']}\n{ts(s['startSeconds'])} --> {ts(min(s['endSeconds'], audio_len + .3))}\n{s['text']}\n" for s in scenes))
    # Türkçe altyazı videonun üstüne yazılır; her oynatıcıda ve indirilen dosyada görünür.
    run('ffmpeg', '-y', '-i', str(silent), '-i', str(out / 'anlatim.mp3'),
        '-filter_complex', f"[0:v]subtitles=f={out / 'altyazi.vtt'}:force_style='{SUB_STYLE}'[v];[1:a]apad=whole_dur={total:.3f}[a]",
        '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '128k', '-t', f'{frames[-1] / FPS:.3f}', '-movflags', '+faststart', str(video))
    silent.unlink()

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
