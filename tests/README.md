# Kontroller

Uygulama paket kurulumu gerektirmez. Testler Node.js, Playwright/Chromium ve SQL testi için `@electric-sql/pglite` kullanır. Test araçlarını ayrı bir geçici klasöre kurup `NODE_PATH` ile onun `node_modules` dizinini gösterebilirsin. Sistem Chromium kullanılıyorsa `CHROMIUM_PATH` yolunu belirt.

```sh
node tests/portal-smoke.cjs
node tests/questions-workflow.cjs
node tests/questions-permissions.cjs
```

- Portal testi geçici HTTP sunucusunu kendisi başlatıp kapatır. Gerçek proje alt dizinini, başlangıç sözleşmesini, sınıf/kitap sırasını, 320/390/768/1440 piksel ekranları, hikâye/video/öğretmen gezinmesini, eski ilerleme taşınmasını, kaynak metni ve dış isteksiz çalışmayı kontrol eder.
- Soru iş akışı testi, gerçek bir sunucuya veri göndermeden API yanıtlarını tarayıcı içinde taklit eder. Gönderim/takip kodu/özel cevap/yanlış kod/yetkisiz hesap/eğitimci yanıtı ve HTML kaçışlarını kontrol eder.
- Yetki testi SQL dosyasını gerçek bir yerel Postgres motorunda (PGlite) çalıştırır. Supabase Auth için test şeması kullanır; tabloya doğrudan erişimi, özel kod ayrımını, normal kullanıcı ile yetkili eğitimciyi, cevap yazmayı, token özetini ve istek sınırını kontrol eder.

Bu testler canlı Supabase bağlantısı veya canlı veri işleme izni anlamına gelmez. Soru hizmeti kaynak kodda şu anda bağlı değildir. Testler yeni tarayıcı profili kullanır; gerçek öğrenci kayıtlarını değiştirmez. Kitapların tam PDF'leri test çıktısına veya depoya dahil edilmez.
