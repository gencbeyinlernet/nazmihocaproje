# Merak Bahçesi · Ortaokul, Lise ve Üniversite

Rize İl Millî Eğitim Müdürlüğü çalışması için Türkçe ve mobil uyumlu din kültürü platformu. Öğretmen takip sistemi ayrı `okultakipburakhoca` deposundadır.

## Sayfalar

- Ana sayfa: https://gencbeyinlernet.github.io/nazmihocaproje/
- Ortaokul (5–8): https://gencbeyinlernet.github.io/nazmihocaproje/ortaokul/
- Lise (9–12): https://gencbeyinlernet.github.io/nazmihocaproje/lise/
- Üniversite: https://gencbeyinlernet.github.io/nazmihocaproje/universite/
- Görselli hikâyeler: https://gencbeyinlernet.github.io/nazmihocaproje/sahne-atolyesi/
- Diğer sınıflar: `siniflar/6-sinif/` … `siniflar/12-sinif/`.
- İlk özgün metnin sekiz haftalık çalışması: `metin-atolyesi/`.

24 Ekim 2026 tarihli kullanıcı isteğiyle **4. sınıf aktif katalogdan, sınıf seçicisinden, soru formundan ve sahne atölyesinden kaldırıldı**. Önceki çalışmalar `arsiv/4-sinif/` altında korunur. Eski 4. sınıf ve ilkokul bağlantıları 5. sınıfa yönlenir; uygulama arşiv dosyalarını yüklemez.

## Hazır içerikler

Aktif katalog 5–12. sınıflarda 35 ünite ve 163 konu planı içerir. Başlıklar ve sayfa referansları yüklenen kitapların sırasındadır. Kaynak dökümü: [KAYNAKLAR.md](KAYNAKLAR.md). 7. sınıf dosyası aktarım sınırını aştığından o sınıfın ayrı sayfasında konu sırası beklenir; tahminî başlık eklenmez.

5. sınıf “Allah İnancı” ünitesinin ilk üç konusu görselli hikâyelere bağlanır:

1. **Evrendeki Mükemmel Düzen** · “Gökyüzü Kulübünün İlk Buluşması” · s. 14.
2. **Allah’ın Varlığı ve Birliği** · “Birliğin Anlamını Ararken” · s. 20.
3. **Allah’ın Güzel İsimleri** · “İsimlerin Açtığı Pencere” · s. 29.

Her hikâye **7 sahne × 8 saniye = 56 saniye** olarak planlanır. Toplam 21 ayrı görsel, her görsele ait konuşmacı ve replik, ilerideki hareket tarifi, indirilebilir senaryo ve SRT taslağı bulunur. Zehra ve Ömer’in gözlem kulübü, üç konuyu sırayla birbirine bağlar. Diğer konular görselleri veya sesi hazırmış gibi gösterilmez.

**Ses dosyalarını kullanıcı çalışmanın sonunda yükleyecek.** Şu an aktif içeriklerde ses veya video dosyası yoktur; önizleme sessizdir. Eski ses denemeleri kullanılmaz. Her repliğin hedef karakter sesi ve dosya adı [SESLENDIRME-PLANI.md](SESLENDIRME-PLANI.md) ve `ses-planlari/karakter-sesleri.json` içinde hazırdır.

## Yaşa göre sade görünüm

Ana sayfa yalnızca üç eğitim düzeyi gösterir. Ortaokulda sınıf → tek belirgin “Hikâyeye başla” düğmesi → büyük görsel ve replik → Geri/İleri akışı vardır. Hazırlanmamış konular ve kaynak bilgileri kapalı ayrıntılardadır. Tamamlanma, yedi görsel ziyaret edilip öğrenci “Bitirdim” dediğinde kaydedilir; video izlenmiş veya sınav geçilmiş sayılmaz. Mevcut okuma ilerlemesi ve tamamlanan kartların yeşil durumu korunur.

Lisede daha olgun renkler, ünite/konu araması, kısa okuma ve düşünme soruları kullanılır. Üniversite alanında profesyonel okuma düzeniyle üç özgün tartışma planı ve indirilebilir çalışma notları vardır. **Üniversite kaynakları henüz eklenmemiştir; bu planlar kaynaklandırılmış üniversite dersleri olarak sunulmaz.** Notlar sayfada geçici tutulur; kullanıcı isterse metin dosyası olarak indirir.

Teknik senaryo, hareket tarifi, ses dosyası deneme ve indirme araçları öğrenci ekranında görünmez. Atölyede `?gorunum=ogretmen`, sınıf sayfasında aynı parametre öğretmen görünümünü açar. Bu bir görünüm seçimidir; yönetici girişi veya yetkilendirme değildir. Araçlar site kaynağını değiştirmez, sunucuya dosya yüklemez.

## Çalışma akışı

Öğrenci önce eğitim düzeyini, sonra sınıfını seçer. Sınıf sayfası hazır hikâyelerden birini belirgin bir başlangıç düğmesiyle önerir. Görselli içerik öğrenci oynatıcısında açılır; yalnızca görsel, konuşmacı/replik ve ilerleme düğmeleri görünür. Görseli olmayan hazır hikâyeler kısa bilgi → hikâye şeklinde ilerler. Gerçek video eklenene kadar öğrenciye boş bir video adımı gösterilmez. Sesler daha sonra bağlanır; kayıt bitmeden otomatik ilerlenmez.

Öğretmen görünümünde bütün kitap konu planları ve önceki ayrıntılı inceleme araçları korunur. Ortak soru/cevap alanı “Bir sorum var” altında isteğe bağlı açılır. Kullanım koşulları başlangıçta kısa özet ve açılabilir tam metinle gösterilir; mevcut onay zorunluluğu değişmez.

Görseller özgün yapay zekâ üretimidir. Açıklama ve hikâyeler, öğretmen/içerik sorumlusu incelemesi bekleyen özgün uyarlamalardır; kitap metni, ayet veya hadis alıntısı gibi sunulmaz. Kitapların tam PDF’leri depoya eklenmez. İlk kullanıcının `assets/source.txt` metni değişmeden korunur. Gerçek kurum logosu `logo.jpg` dosyasıdır.

## Gizlilik ve soru alanı

Başlangıçta [KULLANIM-KOSULLARI.md](KULLANIM-KOSULLARI.md) için onay istenir. İzin mercii Rize İl Millî Eğitim Müdürlüğüdür. Onay tarayıcıda tutulur; kimlik doğrulanmış sunucu sözleşmesi veya teknik kopyalama koruması değildir. Kamuya açık GitHub dosyalarına doğrudan erişilebilir.

Soru/görüş, takip koduyla özel cevap ve yetkili eğitimci ekranları vardır. **Soru sunucusu henüz bağlı değildir; gerçek gönderme ve sorgu kapalıdır.** Kurulum: [backend/QUESTIONS-SETUP.md](backend/QUESTIONS-SETUP.md). Sunucu anahtarı veya şifre GitHub’a yazılmaz. Cihazdan seçilen deneme sesi yalnızca açık sayfada kalır; sunucuya yüklenmez ve yenilemede kaldırılır.

## Yerel test ve dosyalar

[Yerel test paketini indir](indir/merak-bahcesi-yerel-test.zip). ZIP’i çıkarıp Windows’ta `BASLAT-WINDOWS.bat`, Mac/Linux’ta `python3 BASLAT.py` çalıştır. Python 3 gerekir; paket kurulumu ve derleme gerekmez. Ayrıntılar: [YEREL-TEST.md](YEREL-TEST.md).

- `assets/catalog.js`: aktif 5–12 katalog, ünite ve konu sırası.
- `assets/productions.js`: üç 5. sınıf senaryosu, 21 sahne ve dört hedef ses profili.
- `assets/scenes/`: yeni sahne görselleri.
- `assets/portal.js`, `portal.css`, `audiences.css`: eğitim düzeyleri, yaşa uygun sınıf görünümü ve gezinme.
- `assets/university.js`: kaynak seçimi bekleyen üç özgün üniversite tartışma planı.
- `assets/portal-authoring.js`: öğretmenin tüm konu planlarını incelediği görünüm.
- `assets/studio.js`: sade öğrenci hikâye oynatıcısı.
- `assets/studio-authoring.js`, `studio.css`: öğretmen için görsel/replik/ses ve üretim araçları.
- `assets/privacy.js`, `privacy.css`: ortak onay ekranı.
- `assets/questions.js`, `question-service.js`, `backend/`: özel soru/cevap altyapısı.
- `scripts/package-local.py`: arşivi dışarıda tutarak güncel yerel paketi oluşturur.
- `tests/`: tarayıcı testleri; uygulamayı çalıştırmak için test araçları gerekmez.
