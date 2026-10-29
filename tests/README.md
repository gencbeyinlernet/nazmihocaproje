# Kontroller

Yeni bütünleşik ders testi: `CHROMIUM_PATH=/usr/bin/chromium node tests/pilot-lesson.cjs`. Gerçek yedi sahne MP3'ünün dinlenmesiyle açılan üç turlu oyunu, yanlış cevap ipuçlarını, üçüncü denemede açıklamayı, ilgili sahneye dönüşü, beş soruda ilk cevap üzerinden puanlamayı, son/en iyi puanı, yarım denemeden devamı ve öğrenci/öğretmen ekranları arasındaki ortak ilerlemeyi kontrol eder. Ayrıca 27 yeni kaydın metin/dosya özetlerini, menü açılınca sesin durmasını ve beş ekran genişliğini doğrular.

Testler Node.js, Playwright ve Chromium kullanır. Sistem tarayıcısı için `CHROMIUM_PATH=/usr/bin/chromium` belirtilebilir. Her test kendi geçici HTTP sunucusunu açıp kapatır; canlı platforma veri yazmaz.

```sh
CHROMIUM_PATH=/usr/bin/chromium node tests/guided-journey.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/guided-wayfinding.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/automatic-playback.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/story-library.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/audio-workflow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/public-learning-flow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/studio-workflow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/common-story-flow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/visual-story-flow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/audience-flow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/navigation-flow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/discovery-flow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/questions-workflow.cjs
CHROMIUM_PATH=/usr/bin/chromium node tests/portal-smoke.cjs
node tests/questions-permissions.cjs
```

- Ses testi 232 gerçek MP3'ün metin/dosya özetlerini, 105 görselli sahnenin doğru kayıtla açılmasını, gerçek `ended` sonrasında aynı sahnede beklemeyi ve İleri ile geçişi, üç temel düğme, kapalı ek seçenekler, duraklatma, isteğe bağlı altyazı, hata/yeniden deneme, tek medya öğesiyle üst üste binmeyen sesleri, değiştirme önceliğini ve altı ekran genişliğini doğrular. Testte zaman kazanmak için ses bitişine yaklaştırma ve hızlı oynatma kullanılır; uygulamanın normal ses hızı değiştirilmez.
- Öğretmen testi düzenlenebilir ders taslaklarını, metin indirme/yazdırmayı, güvenli altyazıları ve sesli sınıf sunumunu kontrol eder. Atölye testi yerel dosya denemesini ve sekiz saniyeyi aşan kayıtların kesilmemesini doğrular.
- Hikâye testleri bölüm adreslerini, kaynak metinlerin aynen korunmasını, senaryo indirmeyi, sahne/görsel eşleşmesini ve yalnızca açıp geçerek tamamlanamamasını doğrular.
- Arayüz testleri yaşa göre alanları, slaytları, mobil sol menüyü, odak/scroll yönetimini ve soru penceresi açılınca sesin durmasını kontrol eder.
- Portal testi mevcut öğretmen senaryo arşivini, kitap sırasını, kaynak metni ve eski ilerleme taşınmasını korur. Bu yazılı arşiv öğrenciye zorunlu okuma olarak açılmaz.
- Soru testi taklit API yanıtlarıyla özel takip kodu, yetkisiz erişimin reddi ve HTML kaçışlarını doğrular. SQL testi `@electric-sql/pglite` ile özel veri yetkilerini kontrol eder.

Testler gerçek öğrenci verilerini veya canlı Supabase bağlantısını kullanmaz; soru servisi henüz yapılandırılmamıştır. Hesap ve zorunlu sözleşme onayı yoktur. Kitapların tam PDF'leri yayımlanmaz.

Kütüphane testi 163 kitap konusuna bağlı 205 hikâyeyi, konu/sayfa sırasını, 1.506 kayıt eşleşmesini, konu kelimelerini, ünite filtresini, alternatifleri ve mobil sunumu doğrular. 7. sınıf kaynak sırası doğrulanmış gibi sunulmaz.

Otomatik oynatma testi gerçek MP3 kayıtlarıyla aralıksız sahne sırasını ve tamamlanmayı, elle moda dönüşü, duraklatmayı, geç yüklenen görselde bekleyen sesin iptalini, ses hatasında durmayı, özel öğretmen sesini ve desteklenen ekran uyanık tutma isteğinin temizlenmesini doğrular.

Yönlendirilmiş giriş testi karşılama, sınıf seçimi, gerçek yedi sahnenin dinlenmesi, otomatik tamamlanma, sonraki keşif önerisi, kayıtlı devam, tarayıcı Geri işlemi, öğretmen/serbest girişleri, menü/ses/scroll temizliği ve bozuk yerel kayıtların güvenli karşılanmasını kontrol eder. Önceki katalog ana sayfa kontrolleri bilinçli olarak serbest `kesfet/` adresinde korunur.

Yön bulma testi görünür adım şeridini, gerçek dinleme sonrasında renklenen sahne ilerlemesini, tamamlanma durumlarını, eski sınıf/soru bağlantılarını, erişilebilir içerik bağlantısının oynatıcıyı kapatmamasını ve tamamlanan yolun ilk sahneden tekrar izlenmesini kontrol eder.

Mobil uygulama testi: `CHROMIUM_PATH=/usr/bin/chromium node tests/mobile-app.cjs`. Alt menü ve seçili ekranı, oynatıcıda odaklı görünümü, ton korunarak hız değiştirmeyi, sahneler ve yenileme arasında tercihin korunmasını, ses temizliğini ve beş ekran ölçüsünü kontrol eder.

Fotoğraf gerçekliğindeki görseller: `CHROMIUM_PATH=/usr/bin/chromium node tests/photo-library.cjs`. 205 hikâyenin 1.395 sahnesini, diğer ortak/akademik sahneleri, 48 karenin dosya ve görüntü alanlarını, gerçek yüklemeyi, mobil görünümü ve görsel hatasında durup yeniden denemeyi doğrular.

Kadın sesi yenileme testi: `CHROMIUM_PATH=/usr/bin/chromium node tests/female-audio.cjs`. 60 Emel kaydının replik ve dosya özetlerini, gerçek sürelerini, açık sahne URL’si ile manifest üzerinden önbellek sürümünü, onaylı özel kayıt önceliğini ve öğrenci/öğretmen oynatımını kontrol eder.
