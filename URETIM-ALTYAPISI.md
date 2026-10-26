# Merak Bahçesi · Görsel, ses ve video altyapısı

26 Ekim 2026 güncellemesi. Yeni video çalışmaları, kullanıcının yüklediği eğitim videosu hazırlama kılavuzuna göre yürütülür. Teknik ve pedagojik ölçütler ile sahne kartı [VIDEO-URETIM-STANDARDI.md](VIDEO-URETIM-STANDARDI.md) içindedir.

## Mevcut içerik

Aktif çalışma 5. sınıftan başlar. Kitap sırasına bağlı 163 konu için 198 özgün hikâye taslağı vardır. 7. sınıfın kaynak sırası henüz doğrulanmamıştır. Üniversite içerikleri özgün tartışma taslaklarıdır.

Öğrenci deneyimi görsel ve sahneye bağlı Türkçe ses oynatımıdır. Toplam 1.457 geçici sentetik MP3 yaklaşık 154 dakika sürer. Kaynak ve lisanslar [ses kayıt bilgisi](assets/audio/CREDITS.md) dosyasındadır. Konuşmacı adları gerçek çocuk veya karakter oyuncusu kaydı bulunduğu anlamına gelmez.

5. sınıf kitabının ilk üç konusuna ait üç hikâyede toplam 21 özgün sahne görseli vardır: Evrendeki Mükemmel Düzen (s. 14), Allah’ın Varlığı ve Birliği (s. 20), Allah’ın Güzel İsimleri (s. 29). Diğer konularda ortak görseller ve konu simgeleri de kullanılır; yüzlerce ayrı film sahnesi hazırlanmış gibi sunulmaz.

## Dosya düzeni

- `assets/productions.js`: üç görselli hikâyenin sahne ve replikleri.
- `assets/scenes/<hikâye>/<01..07>.png`: 21 ayrı görsel.
- `assets/common-story-data.js`, `assets/visual-story-data.js`: iki ortak hikâye.
- `assets/story-library-data.js`: kitap sırasındaki özgün örnekler.
- `assets/audio/anlatim/`: sahne kimlikleriyle eşleşen MP3 kayıtları.
- `assets/audio/narration-manifest.json`, `assets/audio/library-manifest.json`: kayıt yolları, gerçek süreler, metin ve dosya özetleri.
- `assets/narration.js`: ortak görsel ve ses oynatıcısı.
- `video-ornekleri/7-sahne-*/`: senaryo ve hedef altyazı taslakları; son kayda göre yeniden zamanlanır.

Eski senaryo dökümlerindeki “sesler sonra eklenecek” veya “56 saniye” ifadeleri ilk planı anlatır; güncel durum yukarıdadır. Yedi sahne ve yaklaşık sekiz saniye üretim hedefidir. Oynatıcı gerçek ses bitişini bekler; kaydı sekizinci saniyede kesmez.

## Oynatma ve yeni kayıt

Öğrenci İzle ve dinle düğmesiyle başlar. Varsayılan elle modda konuşma bitince İleri düğmesiyle geçer. Otomatik oynat seçilirse ses bitişi sonraki görsel ve kaydı açar. Bütün sahneler dinlenmeden içerik tamamlanmaz. Hesap, zorunlu onay veya uzun okuma ekranı yoktur.

Gerçek ses geldiğinde sahnenin `audioUrl`, `audioDuration`, `audioVoice` ve `audioApproval: "approved"` alanları güncellenir. Onaylı kayıt geçici örnekten önce kullanılır. Her replik ayrı dosyadır. [SESLENDIRME-PLANI.md](SESLENDIRME-PLANI.md) eşleştirmeleri açıklar.

Öğretmen `sahne-atolyesi/?gorunum=ogretmen` alanında yerel bir sesi deneyebilir. Deneme yalnız açık sayfada kalır; sunucuya yüklenmez ve yenilemede kaldırılır. Bu görünüm seçimi bir yönetici yetkilendirmesi değildir.

## Daha sonraki video aşaması

Şimdiki oynatım, tamamlanmış MP4 veya tam karakter animasyonu değildir. Sonraki videolar için aynı konu ve sahne kimlikleri korunur. Kılavuza göre **senaryo → sahne taslağı → görsel → ses → kurgu → kontrol** sırası izlenir.

Kaynak metinler `assets/source.txt` ve `assets/ikinci-hikaye-kaynak.txt` içinde değiştirilmeden korunur. Kitapların tamamı yayımlanmaz. Kurum logosu kullanıcının sağladığı gerçek `logo.jpg` dosyasıdır. Önceki 4. sınıf denemeleri arşivdedir ve aktif uygulama tarafından yüklenmez.
