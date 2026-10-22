# Merak Bahçesi · Sınıf düzeylerine göre din kültürü eğitimi

Rize İl Millî Eğitim Müdürlüğü bünyesindeki çalışma için Türkçe, mobil uyumlu statik platform. Öğretmen takip sistemi ayrı `okultakipburakhoca` deposunda kalır.

## Yayın ve sayfalar

- Ana sayfa: https://gencbeyinlernet.github.io/nazmihocaproje/
- Ayrı sınıf sayfaları: `siniflar/4-sinif/` … `siniflar/12-sinif/`.
- İlkokul bağlantısı: `siniflar/ilkokul/`, yüklenen 4. sınıf kaynağını gösterir. 1–3. sınıflar için kaynak varmış gibi içerik eklenmez.
- İlk özgün metnin bağlantılı sekiz haftalık çalışması: `metin-atolyesi/`.

## Kaynak ve üretim durumu

Sekiz okunabilir kitap için 40 ünite, 182 konu planı ve 24 özgün hikâye taslağı vardır. Konu başlıkları ve basılı sayfa referansları kitapların içindekiler sırasındadır. 10. sınıf kitabının dosya adında 9 yazsa da kapak/ISBN bilgisi esas alınmıştır. Kaynak dökümü: [KAYNAKLAR.md](KAYNAKLAR.md).

**7.pdf, 32 MiB dosya aktarım sınırını aştığı için okunamadı.** 7. sınıfın ayrı sayfası hazırdır; konu sırası tahmin edilerek doldurulmamıştır. Daha küçük PDF veya içindekiler sayfaları gelince kaynak tamamlanabilir.

Hikâyeler ve kısa açıklamalar kitap metni değildir; öğretmen ve içerik sorumlusu incelemesi bekleyen özgün uyarlamalardır. Kitapların tam PDF'leri, görselleri veya soru bankaları depoya yüklenmez. Video dosyaları henüz üretilmemiştir. Boş video alanları “hazır” veya “izlendi” gibi gösterilmez.

Her kart konu, hikâye adı ve kahramanları gösterir. Açıldığında kısa bilgi → hikâye → video adımları vardır. Öğretmen, önceki/sonraki konuyla kitap sırasını izleyebilir; konu/ünite araması da kullanılabilir. Hikâye ve videoyu aynı anda üretmek yerine önce taslak değerlendirilir, sonra ilgili gerçek `videoUrl` bağlanır. Haftalık çalışma düzenini öğretmen belirler; sınıf sayfalarında takvime bağlı yayın kilidi yoktur.

## İçerik ve dosyalar

- `assets/catalog.js`: 4–12 sınıf, ünite ve sıralı konu verileri. 7. sınıfın kaynak listesi beklenir.
- `assets/portal.js`, `portal.css`: sınıf seçimi ve öğretmen içerik oynatıcısı.
- `assets/privacy.js`, `privacy.css`: içerikten önce gizlilik/kullanım ekranı. İzin mercii Rize İl Millî Eğitim Müdürlüğüdür.
- `assets/questions.js`, `question-service.js`: öğrenci sorusu, özel kodla cevap ve yetkili eğitimci ekranı.
- `backend/questions.sql`: gerçek soru hizmeti için sunucu yetkileri ve RPC'ler.
- `assets/weekly.js`, `VIDEO-SENARYOLARI.md`: ilk metne bağlı sekiz haftanın tam sahne ve seslendirme taslakları.
- `assets/source.txt`: ilk kullanıcının özgün metni, değişmeden korunur.
- `logo.jpg`: kullanıcının yüklediği kurum logosu; doğrudan kullanılır.

Eski bölüm ilerlemeleri metin atölyesine taşınırken yeni hafta sırasına göre eşlenir; önceki puanlar ve sertifika adı korunur. Videolar gelmeden yeni video izleme/değerlendirme tamamlaması yapılamaz. Ortak Drive klasörü bir hafta videosu yerine geçmez.

## Gizlilik ve kullanım

[KULLANIM-KOSULLARI.md](KULLANIM-KOSULLARI.md) metninin onayı başlangıçta istenir. Onay tarayıcıda sürüm ve tarihle tutulur. Bu, kimlik doğrulanmış sunucu sözleşmesi veya teknik kopyalama koruması değildir. Herkese açık GitHub dosyaları onay ekranı atlanarak da erişilebilir.

Son okunan içerik, eski ilerleme/sertifika adı ve kullanım onayı cihazda saklanır. Öğrenci soru metni otomatik kaydedilmez. Reklam/analiz takipçisi ve haricî yazı tipi isteği yoktur. Google Drive yalnızca kullanıcı bağlantıya tıkladığında açılır.

## Öğrenciden soru ve özel cevap

“Sizin merak ettiğiniz ne var?” alanında sınıf/konu seçimi, soru/görüş formu, özel takip koduyla cevap ve yetkili eğitimci ekranı vardır. Ad, okul veya iletişim bilgisi istenmez. Yanıt SMS/e-posta olarak gönderilmez; öğrenci özel koduyla sitede görüntüler.

**Sunucu bağlantısı henüz yoktur. Gerçek soru gönderimi ve cevap sorgusu şu anda devre dışıdır.** Bağlamak için [backend/QUESTIONS-SETUP.md](backend/QUESTIONS-SETUP.md). Canlı hizmet açılmadan kurumun aydınlatma, saklama ve kötüye kullanım önleme süreçleri tamamlanmalıdır. Şifre veya yetkili servis anahtarı GitHub'a yazılmaz.

## Yerelde çalıştırma

Küçük yerel paket: [indir/merak-bahcesi-yerel-test.zip](indir/merak-bahcesi-yerel-test.zip).

Windows’ta **BASLAT-WINDOWS.bat** dosyasına çift tıkla; Python 3 kuruluysa doğru klasör açılır. Ayrıntılı adımlar: [YEREL-TEST.md](YEREL-TEST.md).


Paket kurulumu ve derleme gerekmez:

```sh
python3 -m http.server 3000 --bind 127.0.0.1
```

Windows'ta `python3` yerine `python` kullanılabilir. HTTP üzerinden servis edin. Site GitHub Pages `main` / kök klasöründen yayınlanır. Testler `tests/` dizinindedir; test araçları uygulamanın çalışması için gerekli değildir.
