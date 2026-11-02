# Toplu video üretimi · 2 Kasım 2026

Mevcut 220 hikâye ve toplam 1.500 sahne MP4 olarak hazırlanmıştır: 205 sınıf hikâyesi, Saraydan Dünyaya'nın 8 bölümü, İğneden Kâinata'nın 4 bölümü ve 3 üniversite çalışma taslağı. 7. sınıfın kitap sırası için daha önce belirtilen doğrulama eksikliği devam eder; yeni müfredat veya kaynak uydurulmamıştır.

Her video Full HD 1920 × 1080 H.264 görüntü, Türkçe AAC ses, yumuşak dijital kamera hareketi, Rize İl Millî Eğitim Müdürlüğü için kullanıcının verdiği logo ve isteğe bağlı Türkçe VTT altyazı ve MP4 içine eklenmiş Türkçe altyazı izi içerir. Kaynak görsel ve sesler korunur. Dosya boyutunu düşürmek için ortak hareketli görsel katmanları yeniden kullanılır. İlk örnekteki videonun kendisi korunmuştur; toplu videoların alt bandında genel Merak Bahçesi adı kullanılır. Hikâye adı oynatıcıda, konuşma metni isteğe bağlı altyazıda bulunur.

Bu aşama fotoğraf gerçekliğindeki sabit görsellere kamera hareketi verilen video kurgusudur. Flow'da üretilmiş karakter, nesne, çevre veya dudak animasyonu değildir. Sonraki aşamada gerçek hareketli klipler geldiğinde mevcut hikâye/sahne/konuşma kimlikleriyle değiştirilebilir. Sentetik sesler kaynak kayıtlarıdır; bu işlem yeni bir ses oyunculuğu üretmez.

## Tekrar üretim

1. `python scripts/build-all-videos.py --workers 3`: ses ve görsel eşleştirmelerini alır, ortak görüntü katmanlarını önbelleğe alır ve eksik/değişmiş videoları üretir. Tamamlandığında altyazı izlerini yeniden kodlama yapmadan MP4 dosyalarına ekler.
2. `node scripts/publish-video-index.cjs`: beklenen 220 dosya tamamlanmışsa özetlerini kontrol edip kullanıcı arayüzü listesini yayıma hazırlar.
3. `CHROMIUM_PATH=/usr/bin/chromium node tests/video-library.cjs`: tüm dosyalar, altyazılar, konu araması ve oynatma kontrolleri.

`videos/manifest.json` dosyasında her hikâyenin kimliği, dosya yolu, süre, sahne sayısı, poster, altyazı ve SHA-256 özeti bulunur. Kaynak sahne eşleştirmeleri `node scripts/export-video-jobs.cjs` ile tekrar alınabilir. Ortak önbellek yalnızca `/tmp/merak-video-cache` altında tutulur ve siteye yüklenmez.

Üretim doğal konuşma süresini korur: sahne en az 8 saniyedir; uzun repliklerde uzar. Hiçbir replik 8 saniyeye sıkıştırılmaz. Altyazı süreleri son kurguya göre hesaplanır. Her video 6 dakikanın ve 300 MB'ın altındadır. Toplam video boyutu yaklaşık 566 MiB'dir; siteyle birlikte GitHub Pages'ın 1 GB sınırının altında tutulmuştur.

## Kullanım

`videos/` sayfasında sınıf ve konu seçilebilir, MP4 indirilebilir. İsteğe bağlı “Bittiğinde sonraki videoya geç” seçeneği aynı arama/sınıf listesindeki sıradaki videoyu açar. Önceki/sonraki ve kapatma işlemleri eski videonun sesini durdurur. Hikâye ve sınıf sayfalarında video bağlantıları bulunur. Önceki sahne sahne dinleme ve ilerleme kayıtları korunur; yalnız videoyu açmak eski sınav/rozet tamamlanması sayılmaz.

Temel yerel test ZIP'i yüzlerce MB video dosyası içermez. Video kütüphanesi bu pakette internet üzerinden oynatılır; ayrı indirilen MP4 dosyaları internet olmadan izlenebilir.
