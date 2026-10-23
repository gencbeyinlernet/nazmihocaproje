"""Build the local test ZIP without repository metadata or unrelated projects."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
files = [root / name for name in (
    "BASLAT-WINDOWS.bat", "BASLAT.py", "KAYNAKLAR.md", "KULLANIM-KOSULLARI.md",
    "README.md", "VIDEO-SENARYOLARI.md", "YEREL-TEST.md", "URETIM-ALTYAPISI.md", "SESLENDIRME-PLANI.md",
    "index.html", "logo.jpg", "scripts/generate-voices.py",
)]
for folder in ("assets", "backend", "metin-atolyesi", "siniflar", "sahne-atolyesi", "ses-planlari"):
    files.extend(p for p in (root / folder).rglob("*") if p.is_file())
for folder in (root / "video-ornekleri").glob("7-sahne-*"):
    files.extend(p for p in folder.rglob("*") if p.is_file())

target = root / "indir/merak-bahcesi-yerel-test.zip"
target.parent.mkdir(exist_ok=True)
with ZipFile(target, "w", compression=ZIP_DEFLATED) as archive:
    for file in sorted(files):
        archive.write(file, "merak-bahcesi/" + file.relative_to(root).as_posix())
with ZipFile(target) as archive:
    assert archive.testzip() is None
    assert len([name for name in archive.namelist() if "/scenes/" in name]) == 21
    assert "merak-bahcesi/sahne-atolyesi/index.html" in archive.namelist()
    assert len([name for name in archive.namelist() if name.endswith(".wav") and "/audio/" in name]) == 21
print(f"Local test package: {len(files)} files, {target.stat().st_size / 1024**2:.1f} MiB")
