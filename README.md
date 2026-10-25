# Merak Bahçesi

Rize İl Millî Eğitim Müdürlüğü çalışması için Türkçe, herkese açık, mobil uyumlu din kültürü ve değerler eğitimi platformu. Öğretmen takip sistemi ayrı `okultakipburakhoca` deposundadır.

## Öğrenci için adım adım uygulama

Ana adres artık menü katalogu yerine yönlendiren bir öğrenci uygulamasıdır. İlk girişte **Keşfe başla → Sınıfını seç → İlk keşfi izle → Sonraki keşfe geç** yolu izlenir. Karşılama ekranında tek belirgin başlangıç düğmesi vardır; sürekli sol/sağ menüler gösterilmez. Öğretmen alanı ve serbest gezinme ayrı erişimlerdir.

Sınıf seçilince ilk ortak hikâyenin ilk kısa durağı açılır. Keşif yolu ortak hikâyenin sekiz bağlantılı durağı, seçilen sınıfın kitap sırasındaki konuları ve ikinci ortak hikâyenin dört bölümünden oluşur. 7. sınıfta doğrulanmış kitap konuları bulunmadığından yalnız ortak keşifler gösterilir. Üniversitedeki üç özgün taslak kaynaklandırılmış müfredat gibi sunulmaz.

Her durakta görsel ve kayıtlı ses vardır. Öğrenci elle ilerleyebilir veya Otomatik oynat seçeneğini açabilir. Bütün sahneler dinlenmeden keşif tamamlanmaz. Tamamlanınca kısa bir kutlama ve **Sonraki keşfe geç** düğmesi çıkar; başka bir içerik istemeden başlatılmaz. Keşif yolundan farklı bir konuya serbestçe geçilebilir; zorunlu sıra veya kilit yoktur.

Sınıf seçimi, izleme ve devam adımları kısa bir şeritte gösterilir. Oynatıcıda yalnız dinlenmesi biten sahneler yeşile döner; geçip bakılan sahne tamamlanmış sayılmaz. Keşif listesinde **Tamamlandı / Devam ediyor / Henüz tamamlanmadı** durumları yazıyla da belirtilir. Tamamlanmış bir hikâye yeniden açıldığında ilk sahneden başlar. Bütün yol tamamlandıysa yeni içerik varmış gibi önerilmez; yeniden dinleme sunulur. Önceki `#siniflar` ve `#merak` bağlantıları yeni sınıf seçimini ve soru penceresini açar.

Sınıf, dinlenen sahneler, son açılan sahne ve tamamlanan keşifler yalnızca bu cihazın `merak-guided-journey-v1` kaydında tutulur. Hesap, ad, e-posta ve izleme analitiği yoktur. Geri dönüşte kaldığı yer önerilir; tarayıcı Geri işlemi oynatıcıyı durdurur. Yenilenen sayfa sesi kendiliğinden başlatmaz; Devam et düğmesi gösterilir. Kayıtlar isteğe bağlı paylaşım/gizlilik alanından silinebilir. Sayaç dinlenen keşif sayısıdır, öğrenme ölçümü veya sınav puanı değildir.

Öğretmenler doğrudan `hikayeler/` alanından konu arayabilir. Önceki serbest keşif ekranı `kesfet/` altında korunur; öğrencinin ilk girişine eklenmez. Kaynak metinler, 198 örnek, 1.457 ses ve diğer sayfalar korunmuştur. Arayüz `assets/guided-app.js` ve `assets/guided-app.css` içindedir.

## Aç ve dinle

- [Ana sayfa](https://gencbeyinlernet.github.io/nazmihocaproje/)
- [5. sınıf sesli hikâyeleri](https://gencbeyinlernet.github.io/nazmihocaproje/sahne-atolyesi/)
- [Saraydan Dünyaya · Ortak ilk hikâye](https://gencbeyinlernet.github.io/nazmihocaproje/ortak-hikaye/)
- [İğneden Kâinata · İkinci hikâye](https://gencbeyinlernet.github.io/nazmihocaproje/igneden-kainata/)
- [Öğretmen için ders hazırlığı](https://gencbeyinlernet.github.io/nazmihocaproje/ders-hazirla/)

Sınıfını ve konunu seç; **İzle ve dinle** düğmesine dokun. Her görsel kendi Türkçe ses kaydıyla oynar; varsayılan elle ilerleme modunda konuşma bitince aynı görselde bekler. **Otomatik oynat** anahtarı açılırsa, kullanıcı yeniden dokunmadan bir sonraki görsel ve kayıt açılır. **İleri** düğmesine dokunulduğunda sonraki görsel açılır ve o görselin sesi başlar. Öğrenci veya öğretmenin bir okuma metni takip etmesi gerekmez. Altyazı kapalı başlar; istenirse açılır. Ana ekranda yalnızca Geri, Dinle/Duraklat ve İleri düğmeleri bulunur. Ses çubuğu, altyazı, tam ekran ve bölüm seçimi kapalı başlayan “Diğer seçenekler” altındadır. Sesler sayfa açılır açılmaz değil, kullanıcının ilk oynatma dokunuşuyla başlar.

Platformun girişi şifresiz, üyeliksiz ve zorunlu onaysızdır. Özgün içerikler paylaşılabilir. [Paylaşım ve gizlilik](KULLANIM-KOSULLARI.md) isteğe bağlı bilgidir. Kişisel sorular eğitim materyali sayılmaz; özel kalır.

## Kitap sırasına göre hikâye kütüphanesi

`hikayeler/` sayfası ile 5–12 sınıf sayfalarının ana akışı **Hangi konuyu işliyorsunuz? → Hikâyeleri bul → İzle ve dinle** şeklindedir. Sınıf ve konu kelimesi seçilir; sonuçlar kitap sırasını korur. Türkçe karakterler, bazı eş anlamlılar ve kısa konu anlatımları desteklenir. Bu alan bir hazır içerik aramasıdır; çevrim içi yapay zekâdan yeni içerik üretiyormuş gibi gösterilmez.

Kütüphanede doğrulanmış **163 konu için 198 özgün hikâye** vardır. Her konuya bir örnek; her ünitenin ilk konusuna ek bir alternatif hazırlanmıştır. Sınıf başına dağılım: 5. sınıf 40, 6. sınıf 25, 8. sınıf 30, 9. sınıf 25, 10. sınıf 30, 11. sınıf 22, 12. sınıf 26. **7. sınıfın kaynak sırası doğrulanmadı; içerik uydurulmaz.** Dosya 32 MiB aktarım sınırını aşmaktadır.

Ünite/konu adı, sınıf, basılı kitap sayfası ve sıra katalogla aynıdır. Yeni 140 ana hikâyenin olay, açıklama, seçim, sonuç ve düşünme sorusu ayrı ayrı yazıldı; yalnız başlık değiştiren boş yer tutucular değildir. Bunlar özgün **öğretmen kontrolü bekleyen taslaklardır**; kitaptan alınmış metin veya resmî kazanım onayı olarak sunulmaz.

Yeni hikâyeler için **1.225 ayrı Türkçe MP3** üretildi; önceki 232 kayıt da korunur. Toplam 1.457 kayıt vardır. Yeni kayıtlar CC0 veri kümesi kullanan Fettah modelinin geçici anlatıcı örnekleridir; gerçek çocuk veya karakter oyuncusu kaydı değildir. Görseller konulara eşlik eden kitap, doğa, dayanışma, adalet, mimari ve düşünme simgeleridir; yüzlerce özgün film sahnesi hazırlanmış gibi gösterilmez. Mevcut 21 özgün resimli üç hikâye ayrıca korunur.

Yeni kaynaklar: `ses-planlari/mufredat-hikaye-tohumlari.txt`, `ses-planlari/unite-alternatifleri.txt`; derleme betiği `scripts/build-story-library.py`; 198 hikâye `assets/story-library-data.js`. Yeni ses metinleri `ses-planlari/kutuphane-ses-metinleri.json`, ses/dosya özetleri `assets/audio/library-manifest.json`; tarayıcıda `assets/library-narration.js` önceki kayıt haritasına eklenir. Metin veya kayıt değiştiğinde birbirine karşılık gelen özetler de yenilenmelidir.

Öğretmen hazırlık alanında yeni konular da sesli hikâyeyle sunulabilir. İlgili konunun bütün alternatiflerine doğrudan bağlantı vardır. Öğrenci akışında uzun metin gösterilmez; her sahne dinlendikten sonra **İleri** ile veya isteğe bağlı **Otomatik oynat** seçeneğiyle geçilir. Tamamlanan yeni örnekler `merak-library-progress-v1` altında yalnızca bu cihazda tutulur; paylaşım/gizlilik alanındaki kayıt silme işlemi bunu da temizler.

## Sesli içerik kapsamı

Önceki içeriklerdeki **232 ayrı MP3 dosyası** `assets/audio/anlatim/` altında bulunur; çalışma anında bir ses hizmetine bağlanılmaz. Yeni kütüphane kayıtları yukarıdaki bölümde açıklanmıştır. Bunlar sonradan kullanıcının kendi kayıtlarıyla değiştirilebilen **sentetik Türkçe örnek seslerdir**. Gerçek çocuk veya karakter oyuncusu kaydı ya da stüdyo kalitesinde seslendirme olarak sunulmaz. Konuşmacı adları hikâyedeki rolleri gösterir; hedef karakter tarifleri gelecekteki kayıtların talimatıdır. Yerel iki Türkçe ses modeli ve küçük ton/tempo farkları kullanıldı. Kaynak ve lisanslar [ses kayıt bilgisi](assets/audio/CREDITS.md) içinde; DFKI örnekleri kaynak gösterilerek ticari olmayan amaçlarla, aynı lisansla paylaşılır.

- 5. sınıf kitabının ilk üç konusuna ait 21 özgün görsel + 21 ayrı sahne sesi.
- İlk ortak hikâyede 8 bölüm × 7 = 56 ayrı sahne sesi.
- İkinci hikâyede 4 bölüm × 7 = 28 ayrı sahne sesi; konuşmaya uygun görsel, odak işaretleri ve efektler.
- Hazır sınıf konularının bilgilendirme, hikâye ve düşünme sorularına ait kayıtlar.
- Üniversitenin üç özgün çalışma taslağına ait sesli anlatım ve sorular.

Önceki 232 kayıt yaklaşık 34 dakika; yeni kütüphaneyle birlikte toplam 1.457 kayıt yaklaşık 154 dakika sürer. Her sahne hedef sekiz saniyeye zorla sıkıştırılmaz; **oynatıcı gerçek kayıt bitişini bekler**. Görsel veya ses hatasında ses durur; yeniden deneme mümkündür. Elle ilerleme modunda kayıt bitişi sahne değiştirmez. Otomatik modda kayıt bitişi sonraki sahneyi açar; öğretmenin cihaz sesiyle okunan özel metinlerinde de aynı seçim uygulanır. Eski sesi durdurmadan yenisi başlamaz. Menü açılması, başka bir pencere açılması, sayfa değişimi ve sekmenin gizlenmesi sesi durdurur. Tamamlanma için bütün sahnelerin dinlenmesi gerekir; elle modda Bitir düğmesi kullanılır, otomatik modda son kayıt bitince hikâye kendiliğinden tamamlanır; yalnızca resme bakmak yeterli değildir.

İlk ortak hikâyenin 56 ayrı yeni resmi henüz yoktur: hazır saray, doğa, atölye ve kâinat görselleri ilgili bölümlerde tekrar kullanılır. İkinci hikâyede dört özgün resim ve bir görev şeması tekrar kullanılır. Diğer hazır konular sesli anlatıma eşlik eden sade konu kartlarıyla açılır. Bunlar tamamlanmış video dosyaları değildir; görsel + kayıtlı ses oynatıcısıdır. Yeni videoların yeri korunur.

## Sınıflar ve kaynaklar

Etkin sınıflar 5–12; ortaokul, lise ve üniversite ayrı alanlardır. Masaüstünde sınıflar solda, soru alanı ve diğer menüler sağdadır. Mobilde Sınıflar düğmesi soldan menüyü açar. Serbest keşif ve öğretmen araması **Sınıf → Konu → İzle ve dinle** yolunu kullanır; ana giriş ise yukarıdaki yönlendirilmiş öğrenci uygulamasıdır. Uzun tanıtım yazıları kısaltıldı; ikinci menüler tüm ekranlarda kapalı başlar. Kurumsal görünüm lacivert, zümrüt yeşili ve altın tonlarını kullanır. Rize İl Millî Eğitim logosu, beyaz içerik kartları, belirgin başlıklar ve tutarlı çizgi simgeleriyle sade bir gezinme sunulur. Ortaokul, lise ve üniversite alanları kendi renk vurgularını korur.

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
CHROMIUM_PATH=/usr/bin/chromium node tests/guided-journey.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/audio-workflow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/public-learning-flow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/questions-workflow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/discovery-flow.cjs
python3 scripts/package-local.py
```

Ses testi gerçek MP3'lerle 105 görselli sahnenin akışını, 232 dosya/metin özeti eşleşmesini, ses bitişini beklemeyi, altyazının isteğe bağlı olmasını, öğretmen sunumunu, altı ekran genişliğini ve kaynak metinlerin korunmasını doğrular. Önceki sessiz/okuma oynatıcılarının testleri yeni sesli akışa göre güncellenmiştir.

GitHub Pages: `main` dalı, `/ (root)`. Güncel yerel paket: `indir/merak-bahcesi-yerel-test.zip`; kayıtlı MP3'leri içerir, eski 4. sınıf WAV arşivini içermez.

## Otomatik izleme

Oynatıcıdaki görünür anahtar elle modda kapalı başlar. Açıldığında duraklatılmış ses devam eder; sahne zaten bittiyse sıradaki görsele geçilir. Son ses bittiğinde bütün sahneler dinlenmişse mevcut hikâye tamamlanır. Atlanan sahneler varsa önce bunlara dönülür; başka bir konu rastgele başlatılmaz. Anahtarın kapatılması mevcut kaydı kesmez, sonraki geçişi elle yapmaya döndürür. Duraklatma, menü açılması, sekmenin gizlenmesi ve hata halinde ses durur; kullanıcının Dinle düğmesiyle devam etmesi gerekir. Destekleyen tarayıcılarda otomatik ses çalarken ekran uyanık tutma isteği yapılır; destek yoksa oynatım bozulmaz. Yeni bir hikâye açıldığında otomatik seçim yeniden kapalıdır.
