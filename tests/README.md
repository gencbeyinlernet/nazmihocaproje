# Kontroller

Testler Node.js, Playwright ve Chromium kullanır. Sistem tarayıcısı için `CHROMIUM_PATH=/usr/bin/chromium` belirtilebilir. Her test kendi geçici HTTP sunucusunu açıp kapatır; canlı platforma veri yazmaz.

```sh
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

- Ses testi 232 gerçek MP3'ün metin/dosya özetlerini, 105 görselli sahnenin doğru kayıtla açılmasını, gerçek `ended` geçişini, duraklatma, altyazı, hata/yeniden deneme, tek medya öğesiyle üst üste binmeyen sesleri, değiştirme önceliğini ve altı ekran genişliğini doğrular. Testte zaman kazanmak için ses bitişine yaklaştırma ve hızlı oynatma kullanılır; uygulamanın normal ses hızı değiştirilmez.
- Öğretmen testi düzenlenebilir ders taslaklarını, metin indirme/yazdırmayı, güvenli altyazıları ve sesli sınıf sunumunu kontrol eder. Atölye testi yerel dosya denemesini ve sekiz saniyeyi aşan kayıtların kesilmemesini doğrular.
- Hikâye testleri bölüm adreslerini, kaynak metinlerin aynen korunmasını, senaryo indirmeyi, sahne/görsel/efekt eşleşmesini ve yalnızca açıp geçerek tamamlanamamasını doğrular.
- Arayüz testleri yaşa göre alanları, slaytları, mobil sol menüyü, odak/scroll yönetimini ve soru penceresi açılınca sesin durmasını kontrol eder.
- Portal testi mevcut öğretmen senaryo arşivini, kitap sırasını, kaynak metni ve eski ilerleme taşınmasını korur. Bu yazılı arşiv öğrenciye zorunlu okuma olarak açılmaz.
- Soru testi taklit API yanıtlarıyla özel takip kodu, yetkisiz erişimin reddi ve HTML kaçışlarını doğrular. SQL testi `@electric-sql/pglite` ile özel veri yetkilerini kontrol eder.

Testler gerçek öğrenci verilerini veya canlı Supabase bağlantısını kullanmaz; soru servisi henüz yapılandırılmamıştır. Hesap ve zorunlu sözleşme onayı yoktur. Kitapların tam PDF'leri yayımlanmaz.
