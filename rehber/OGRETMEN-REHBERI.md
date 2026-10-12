# Öğretmenin dijital çantası — 8 adımda ücretsiz yayın

Kapak, hazırladığımız Burak TURGUT Öğretmen Takip ve Bilgi Kaynak Sistemi'nin ekranını gösterir. Ardından sekiz adım gelir. Tüm görsellerde neon çerçeveli Genç Beyinler logosu kullanılır.

## 1. Fikrini ChatGPT’ye anlat

Örnek istek: “Öğretmen takip ve bilgi kaynak sistemi hazırla. Görevler, ders programı ve kaynaklar olsun. HTML tabanlı ve mobil uyumlu olsun.” Kendi adını ve istediğin bölümleri belirt; tasarımı birlikte düzenle.

## 2. Dosyalarını hazırla

Proje dosyalarını indir. ZIP ise klasöre çıkart. `index.html` ana sayfadır; `assets` klasöründe tasarım ve uygulama dosyaları yer alır. Dosya adlarını değiştirme.

## 3. GitHub’da depo aç

GitHub hesabına giriş yap. **＋ → New repository** seç. Depo adı: **ogretmen-cantam**. **Public → Create repository**. Bu depo herkese açık site kodları içindir; kişisel evraklarını buraya koyma.

## 4. Site dosyalarını yükle

Boş depoda **uploading an existing file** bağlantısına tıkla. Dosyalar varsa **Add file → Upload files** seç. `index.html` ve `assets` klasörünü birlikte yükle. `index.html` deponun ana klasöründe olmalı. **Commit changes** düğmesine bas. ZIP dosyasını değil, çıkartılmış dosyaları yükle.

## 5. Pages ayarını bul

Depodaki **Settings** sekmesine tıkla. Soldan **Pages** seç. **Source: Deploy from a branch** olarak ayarla. Kişisel hesap ayarlarını değil, deponun ayarlarını aç.

## 6. main’i seç, Save’e bas

Orta alandaki **Branch** başlığı altında **None ▾** düğmesine tıkla. Listeden **main** seç. Klasör **/ (root)** olarak kalsın. **Save** düğmesine bas. Soldaki **Branches** menüsüne gitme. Dalın adı main değilse, site dosyalarını yüklediğin dalı seç.

## 7. Aç, test et ve paylaş

**Actions** sekmesinde **pages build and deployment** işlemini kontrol et. Sarı sürüyor, yeşil tamamlandı, kırmızı hata var demektir. Yayın birkaç dakika sürebilir. Tamamlandığında **Settings → Pages → Visit site** bağlantısını aç.

Ücretsiz adresin genellikle `https://KULLANICI-ADIN.github.io/ogretmen-cantam/` şeklindedir. Telefonda ve bilgisayarda test et. Dosyaları güncellediğinde aynı adres yeniden yayınlanır. Eski sürüm görünürse sayfayı yenile; bilgisayarda Ctrl+F5 kullanabilirsin.

Örnek çalışma: https://gencbeyinlernet.github.io/nazmihocaproje/ogretmen-takip-sistemi/

## 8. Evraklarını özel sakla

Kişisel evraklar için ayrı bir depo oluştur: **＋ → New repository → ogretmen-evraklarim → Private → Create repository**. Dosyalarını **Upload files → Commit changes** ile bu özel depoya yükle.

**Public = site kodları. Private = kişisel evraklar.** Ücretsiz özel depo açılabilir; erişim verdiğin kişileri ayrıca yönetirsin. Tarayıcıdan yüklemede dosya başına 25 MiB, normal Git yüklemesinde dosya başına 100 MiB sınırı vardır.

Bu örnek sitenin Evrak Çantam alanı dosyaları tarayıcıda saklar; GitHub'a otomatik yüklemez. Tarayıcı kayıtları için Yedekleme alanından yedek indir. GitHub'da saklamak istediğin evrakları özel depoya ayrıca yükle.

## Kısa paylaşım metni

“Her öğretmen kendi dijital çalışma alanını oluşturabilir. ChatGPT ile HTML sitemizi hazırladık; GitHub Pages üzerinden ücretsiz yayınladık. Görevler, ders programı, planlar ve kaynaklar tek yerde. Kişisel evraklar için ayrı bir Private depo kullanıyoruz. Kapaktan başlayıp sekiz adımı takip ederek sen de kendi dijital çantanı hazırlayabilirsin.”

GitHub Free hesabında herkese açık depolar Pages ile ücretsiz yayınlanabilir. Ücretli alan adı gerekmez. Bu yöntem statik HTML, CSS ve JavaScript içindir; sunucu veya veritabanı uygulaması sağlamaz. ChatGPT'nin ücretsiz kullanımında hesap ve kullanım sınırları geçerlidir.
