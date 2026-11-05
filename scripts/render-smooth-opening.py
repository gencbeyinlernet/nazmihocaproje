#!/usr/bin/env python3
"""Tek anlatıcılı bir giriş videosunu görsellerinden titremesiz yeniden oluşturur.

sahneler.json içindeki kare aralıklarını kullanır, hareketi piksel altı
hassasiyetle hesaplar (build-gunes-scuti-narrator.render_scene), kesintisiz
anlatımı ekler ve Türkçe altyazıyı videonun üstüne yazar.

  python3 scripts/render-smooth-opening.py SAHNELER_JSON MEDYA_KLASORU ALTYAZI_VTT CIKTI_MP4
MEDYA_KLASORU: gorseller/ ve anlatim.mp3 dosyasını içeren video-medya klasörü.
"""
import importlib.util, json, subprocess, sys
from pathlib import Path

spec = importlib.util.spec_from_file_location('narrator', Path(__file__).with_name('build-narrator-video.py'))
nar = importlib.util.module_from_spec(spec); spec.loader.exec_module(nar)

data_path, media, vtt, out = map(Path, sys.argv[1:5])
d = json.loads(data_path.read_text())
fps, total = d['fps'], d['frameCount'] / d['fps']
silent = out.with_suffix('.sessiz.mp4')
enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{nar.W}x{nar.H}', '-r', str(fps), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-an', str(silent)], stdin=subprocess.PIPE)
for s in d['scenes']:
    nar.render_scene(enc.stdin, media / s['imageFile'], s['endFrame'] - s['startFrame'], zoom_in=bool(s['number'] % 2))
enc.stdin.close()
if enc.wait():
    sys.exit('Video kodlanamadı')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(silent), '-i', str(media / d['fullAudioFile']),
                '-filter_complex', f"[0:v]subtitles=f={vtt}:force_style='{nar.SUB_STYLE}'[v];[1:a]apad=whole_dur={total:.3f}[a]",
                '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '128k', '-t', f'{total:.3f}', '-movflags', '+faststart', str(out)], check=True)
silent.unlink()
print(f'Tamam: {len(d["scenes"])} sahne, {total:.2f} sn')
