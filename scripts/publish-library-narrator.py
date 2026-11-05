#!/usr/bin/env python3
"""Tamamlanan tek anlatıcılı kütüphane videolarını yayına hazırlar.

1. OUT/<id>/ klasörlerindeki bitmiş videoları video-medya dalına (kutuphane/) ekleyen
   bir commit oluşturur ve gönderir.
2. videos/manifest.json ve assets/video-library-data.js içindeki kayıtları yeni
   videolara (raw.githubusercontent.com) yönlendirir, altyazıyı videos/captions/ altına yazar.
3. Yerine yenisi gelen eski MP4 dosyasını videos/files/ altından siler (site boyutu).

  python3 scripts/publish-library-narrator.py --out DIR [--no-push]
"""
import argparse, json, os, shutil, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = 'https://raw.githubusercontent.com/gencbeyinlernet/nazmihocaproje/{sha}/kutuphane/{name}'


def git(*a, env=None, inp=None):
    return subprocess.run(['git', *a], cwd=ROOT, check=True, capture_output=True, text=True, env=env, input=inp).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--no-push', action='store_true')
    a = ap.parse_args()
    manifest_path = ROOT / 'videos' / 'manifest.json'
    m = json.loads(manifest_path.read_text())
    done = {}
    for d in sorted(a.out.iterdir()):
        f = d / 'done.json'
        if f.exists():
            row = json.loads(f.read_text())
            cur = m['videos'].get(row['id'])
            if cur and cur.get('sha256') == row['sha256']:
                continue  # zaten yayında
            done[row['id']] = (row, d)
    if not done:
        print('Yeni video yok'); return
    git('fetch', '-q', 'origin', 'video-medya')
    parent = git('rev-parse', 'origin/video-medya')
    with tempfile.TemporaryDirectory() as td:
        stage = Path(td) / 'kutuphane'; stage.mkdir()
        for sid, (row, d) in done.items():
            os.link(d / f'{sid}.mp4', stage / f'{sid}.mp4')
            os.link(d / 'kapak.jpg', stage / f'{sid}.jpg')
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(td) / 'index'))
        git('read-tree', parent, env=env)
        git('--work-tree', td, 'add', '-f', 'kutuphane', env=env)
        tree = git('write-tree', env=env)
    msg = (f'Add {len(done)} single-narrator library videos\n\n'
           'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'
           'Claude-Session: https://claude.ai/code/session_01GwQsQamrKgY1snz75JvFhF')
    sha = git('commit-tree', tree, '-p', parent, '-m', msg)
    if not a.no_push:
        git('push', 'origin', f'{sha}:refs/heads/video-medya')
    for sid, (row, d) in done.items():
        old = m['videos'].get(sid, {})
        cap = ROOT / 'videos' / 'captions' / f'{sid}.vtt'
        shutil.copyfile(d / 'altyazi.vtt', cap)
        oldsrc = old.get('src', '')
        if oldsrc.startswith('videos/files/') and (ROOT / oldsrc).exists():
            git('rm', '-q', oldsrc)
        m['videos'][sid] = {**{k: v for k, v in old.items() if k in ('title', 'grade', 'topic')}, **row,
                            'src': RAW.format(sha=sha, name=f'{sid}.mp4'), 'poster': RAW.format(sha=sha, name=f'{sid}.jpg'),
                            'captions': f'videos/captions/{sid}.vtt'}
    m['version'] = '2026-11-06-tek-anlatici'
    m['method'] = 'single-narrator-elevenlabs'
    manifest_path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
    order = {s['id']: i for i, s in enumerate(json.loads(subprocess.check_output(['node', 'scripts/export-video-jobs.cjs'], cwd=ROOT))['stories'])}
    vids = sorted(m['videos'].values(), key=lambda v: order.get(v['id'], 9999))
    (ROOT / 'assets' / 'video-library-data.js').write_text("'use strict';\nwindow.MERAK_VIDEO_LIBRARY = " + json.dumps({'version': m['version'], 'videos': vids}, ensure_ascii=False, indent=2) + ';\n')
    new = sum(1 for v in vids if v.get('format') == 'single-narrator')
    print(f'{len(done)} video yayına hazırlandı (medya {sha[:7]}); toplam tek anlatıcılı: {new}/{len(vids)}')


if __name__ == '__main__':
    main()
