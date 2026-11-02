# İlk MP4 · Gökyüzü Kulübü

2 Kasım 2026. Yedi mevcut görsel ve sahnelere ait ses kayıtları, Full HD H.264/AAC MP4 dosyasında birleştirildi. Görsellerde yumuşak dijital kamera yaklaşması kullanılır; karakter veya dudak animasyonu yoktur. Yeni ElevenLabs sesi veya Flow üretimi yapılmadı: bu oturumda kullanıcının bilgisayarındaki tarayıcıya erişim aracı bulunmuyordu.

Seslendirme metinleri ve kaynak görseller korunur. Her sahne en az sekiz saniyedir; uzun konuşma kesilmeden sahne uzatılır. Son seslere göre Türkçe VTT/SRT ve MP4 içinde ek altyazı izi bulunur. Altyazı zorunlu okumaya dönüşmez; isteğe bağlıdır. Rize İl Millî Eğitim Müdürlüğü için kullanıcının sağladığı özgün logo kullanılır. Ön izleme eğitsel/resmî onay anlamına gelmez.

- `gozlem-kulubu-ilk-video.mp4`: izlenebilir/indirilebilir ilk video.
- `video-kurgusu.json`: sahne, gerçek süre, ses özeti ve görsel eşleşmesi.
- `altyazi.vtt`, `altyazi.srt`: son kurguya göre Türkçe altyazı.
- `index.html`: telefon ve bilgisayarda video sayfası.

Yeniden üretim: depo kökünde `python scripts/render-first-video.py`.

Flow klipleri sonradan geldiğinde aynı yedi sahnenin görsel katmanı değiştirilebilir; konuşma dosyaları ve eşleştirme korunabilir. Her sahne için mevcut hareket tarifleri `SENARYO.md` içindedir. Seslendirme değiştirilirse kurgu ve altyazı süreleri tekrar hesaplanır.
