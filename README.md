# Merak Bahçesi

Rize İl Millî Eğitim Müdürlüğü çalışması için Türkçe, herkese açık, mobil uyumlu din kültürü ve değerler eğitimi platformu. Öğretmen takip sistemi ayrı `okultakipburakhoca` deposundadır.

## Aç ve dinle

- [Ana sayfa](https://gencbeyinlernet.github.io/nazmihocaproje/)
- [5. sınıf sesli hikâyeleri](https://gencbeyinlernet.github.io/nazmihocaproje/sahne-atolyesi/)
- [Saraydan Dünyaya · Ortak ilk hikâye](https://gencbeyinlernet.github.io/nazmihocaproje/ortak-hikaye/)
- [İğneden Kâinata · İkinci hikâye](https://gencbeyinlernet.github.io/nazmihocaproje/igneden-kainata/)
- [Öğretmen için ders hazırlığı](https://gencbeyinlernet.github.io/nazmihocaproje/ders-hazirla/)

Sınıfını ve konunu seç; **İzle ve dinle** düğmesine dokun. Her görsel kendi Türkçe ses kaydıyla oynar; konuşma bitince sonraki sahneye geçilir. Öğrenci veya öğretmenin bir okuma metni takip etmesi gerekmez. Altyazı kapalı başlar; istenirse açılır. Geri/İleri, duraklatma, sesin içinde ilerleme, bölüm seçimi ve destekleyen cihazlarda tam ekran vardır. Sesler sayfa açılır açılmaz değil, kullanıcının ilk oynatma dokunuşuyla başlar.

Platformun girişi şifresiz, üyeliksiz ve zorunlu onaysızdır. Özgün içerikler paylaşılabilir. [Paylaşım ve gizlilik](KULLANIM-KOSULLARI.md) isteğe bağlı bilgidir. Kişisel sorular eğitim materyali sayılmaz; özel kalır.

## Sesli içerik kapsamı

**232 ayrı gerçek MP3 dosyası** `assets/audio/anlatim/` altında bulunur; çalışma anında bir ses hizmetine bağlanılmaz. Bunlar sonradan kullanıcının kendi kayıtlarıyla değiştirilebilen **sentetik Türkçe örnek seslerdir**. Gerçek çocuk veya karakter oyuncusu kaydı ya da stüdyo kalitesinde seslendirme olarak sunulmaz. Konuşmacı adları hikâyedeki rolleri gösterir; hedef karakter tarifleri gelecekteki kayıtların talimatıdır. Yerel iki Türkçe ses modeli ve küçük ton/tempo farkları kullanıldı. Kaynak ve lisanslar [ses kayıt bilgisi](assets/audio/CREDITS.md) içinde; DFKI örnekleri kaynak gösterilerek ticari olmayan amaçlarla, aynı lisansla paylaşılır.

- 5. sınıf kitabının ilk üç konusuna ait 21 özgün görsel + 21 ayrı sahne sesi.
- İlk ortak hikâyede 8 bölüm × 7 = 56 ayrı sahne sesi.
- İkinci hikâyede 4 bölüm × 7 = 28 ayrı sahne sesi; konuşmaya uygun görsel, odak işaretleri ve efektler.
- Hazır sınıf konularının bilgilendirme, hikâye ve düşünme sorularına ait kayıtlar.
- Üniversitenin üç özgün çalışma taslağına ait sesli anlatım ve sorular.

Toplam yaklaşık 34 dakikalık kayıt vardır. Her sahne hedef sekiz saniyeye zorla sıkıştırılmaz; **oynatıcı gerçek kayıt bitişini bekler**. Görsel veya ses hatasında otomatik ilerleme durur; yeniden deneme mümkündür. Eski sesi durdurmadan yenisi başlamaz. Menü açılması, başka bir pencere açılması, sayfa değişimi ve sekmenin gizlenmesi sesi durdurur. Tamamlanma için sahnelerin dinlenmesi ve Bitir düğmesi gerekir; yalnızca resme bakmak yeterli değildir.

İlk ortak hikâyenin 56 ayrı yeni resmi henüz yoktur: hazır saray, doğa, atölye ve kâinat görselleri ilgili bölümlerde tekrar kullanılır. İkinci hikâyede dört özgün resim ve bir görev şeması tekrar kullanılır. Diğer hazır konular sesli anlatıma eşlik eden sade konu kartlarıyla açılır. Bunlar tamamlanmış video dosyaları değildir; görsel + kayıtlı ses oynatıcısıdır. Yeni videoların yeri korunur.

## Sınıflar ve kaynaklar

Etkin sınıflar 5–12; ortaokul, lise ve üniversite ayrı alanlardır. Masaüstünde sınıflar solda, soru alanı ve diğer menüler sağdadır. Mobilde Sınıflar düğmesi soldan menüyü açar. Ana ekran **Sınıf → Konu → İçerik** yolunu ve ortak hikâyeleri öne çıkarır. Cam görünümlü kartlar zümrüt, turkuaz, mor ve altın tonlarındadır.

Kitaplardaki ünite ve konu sırası `assets/catalog.js` içinde korunur. 7. sınıfın doğrulanmış kaynak sırası henüz eklenmediği için hazır içerik varmış gibi gösterilmez. Kaynak ayrıntıları [KAYNAKLAR.md](KAYNAKLAR.md) dosyasındadır. Üniversite içeriği kaynaklandırılmış müfredat değil, özgün tartışma taslaklarıdır.

Kullanıcının iki kaynak metni `assets/source.txt` ve `assets/ikinci-hikaye-kaynak.txt` içinde **değiştirilmeden** korunur. Öğretmen isteğe bağlı açıp indirebilir; öğrenciye zorunlu okuma olarak gösterilmez. Senaryo replikleri ses üretiminde değiştirilmedi. Önceki 4. sınıf çalışmaları `arsiv/4-sinif/` altında korunur; aktif uygulama bunları veya reddedilen eski WAV seslerini yüklemez. İlgisiz eski projeler yayın paketine katılmaz.

## Öğretmen hazırlığı

`ders-hazirla/` alanında sınıf, ünite ve konu seçilir. Ders hedefi, kısa giriş, düşünme sorusu ve sınıf etkinliği düzenlenebilir. Hedef bir öğretmen taslağıdır; resmî kazanım kodu olarak sunulmaz. Plan metin dosyası olarak indirilebilir; Yazdır / PDF, tarayıcının yazdırma ekranını açar.

Sınıfta sun düğmesi aynı sade görsel/ses oynatıcısını açar. Hazır sahneler kayıtlı MP3'leriyle çalışır. Öğretmenin kendi değiştirdiği giriş veya sorular ancak cihazda Türkçe metin sesi varsa seslendirilebilir; destek yoksa açık mesaj gösterilir, öğretmen İleri ile hazır hikâyeye geçebilir. Kayıtlı platform sesleri bu cihaz özelliğine ihtiyaç duymaz. Hedef ve sınıf etkinliği indirilen öğretmen planında bulunur; öğrenciye uzun bir okuma slaytı çıkarılmaz.

Taslaklar sayfada geçicidir; hesap, otomatik sunucu kaydı veya yayımlanmış içeriği değiştirme yoktur. Ses dosyası denemeleri için `sahne-atolyesi/?gorunum=ogretmen` alanı korunur. Öğretmen burada her sahneye kendi yerel sesini seçip deneyebilir; dosya sunucuya yüklenmez ve sayfa yenilenince kaldırılır.

## Kayıtları değiştirme

`assets/audio/narration-manifest.json` ve tarayıcıdaki karşılığı `assets/narration-data.js`, 232 dosyanın yolunu, süresini, rolünü ve metin/dosya SHA-256 özetlerini içerir. Oynatıcı `assets/narration.js`, görünüm `assets/narration.css` içindedir. Üç hikâye veri dosyasında sahnelerin `audioUrl`, `audioDuration`, `audioApproval: "demo"` alanları örnek kayıtlara bağlıdır.

Gerçek kayıt geldiğinde ilgili sahnenin `audioUrl` yolunu değiştirin ve kontrol edilen kayda `audioApproval: "approved"` verin; onaylı kayıt örnek kayıttan önce kullanılır. Aynı dosya adıyla MP3 değiştirmek de mümkündür. `rejected` kayıt çalmaz. Gönderilecek hedef karakter tarifleri [SESLENDIRME-PLANI.md](SESLENDIRME-PLANI.md) içinde.

Yerel üretimin tekrar edilebilir betiği `scripts/generate-audio.py`; Piper ve FFmpeg ile, `ses-planlari/anlatim-metinleri.json` metin listesi ve yerel modellerin klasörü verilerek çalışır. Model dosyaları, hizmet anahtarları veya kullanıcı oturumu depoya konulmaz. Çevrim içi ses hizmetine bu yürütme ortamından erişilemediği için örnekler yerel modellerle üretildi.

## Soru ve görüşler

Soruların özel takip koduyla yanıtlanması için Supabase bağlantısı gerekir; henüz yapılandırılmamıştır. Bağlı değilken gönderme ve sorgulama düğmeleri devre dışıdır. Gönderilmiş gibi başarı mesajı verilmez. Genel sayfalarda yönetici kullanıcı adı/şifre formu yoktur; gelecekteki özel soru yönetimi sunucu yetkilendirmesi ister. Ayrıntılar [backend/QUESTIONS-SETUP.md](backend/QUESTIONS-SETUP.md) dosyasında.

## Yerelde açma ve doğrulama

Windows: `BASLAT-WINDOWS.bat`; diğer sistemler: proje klasöründe `python3 BASLAT.py`. Başlatıcı kendi klasörünü yayınlar ve uygun localhost adresini yazar. HTML dosyasına çift tıklamak yerine yerel sunucu kullanın. [Yerel test rehberi](YEREL-TEST.md).

```sh
CHROMIUM_PATH=/usr/bin/chromium node tests/audio-workflow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/public-learning-flow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/questions-workflow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/discovery-flow.cjs
python3 scripts/package-local.py
```

Ses testi gerçek MP3'lerle 105 görselli sahnenin akışını, 232 dosya/metin özeti eşleşmesini, ses bitişini beklemeyi, altyazının isteğe bağlı olmasını, öğretmen sunumunu, altı ekran genişliğini ve kaynak metinlerin korunmasını doğrular. Önceki sessiz/okuma oynatıcılarının testleri yeni sesli akışa göre güncellenmiştir.

GitHub Pages: `main` dalı, `/ (root)`. Güncel yerel paket: `indir/merak-bahcesi-yerel-test.zip`; kayıtlı MP3'leri içerir, eski 4. sınıf WAV arşivini içermez.
