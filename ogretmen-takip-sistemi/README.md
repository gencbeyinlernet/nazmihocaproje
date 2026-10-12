# Burak TURGUT Öğretmen Takip Sistemi

Öğretmenin dijital çantası: görevler, haftalık ders programı, hazırlık planları ve kontrol listeleri, kişisel evraklar, önemli tarihler, notlar ve eğitim bağlantıları. Öğrenci bilgisi ve öğrenci evrakı için alan içermez.

## Çalıştırma

Paket kurulumu veya derleme gerektirmez. Python 3 ile proje klasöründe:

```sh
python3 -m http.server 3001 --bind 127.0.0.1
```

Windows'ta `python3` yerine `python` kullanılabilir. HTTP üzerinden servis edin. Modern tarayıcı gerekir.

## Saklama ve yedekleme

Görevler ve planlar localStorage, dosyalar IndexedDB içinde saklanır. Kişisel kayıtlar GitHub'a gönderilmez ve cihazlar arasında otomatik eşitlenmez. Aynı web adresi ve tarayıcı profili kullanılmalıdır. Tarayıcı verileri temizlenince kayıtlar silinebilir; “Yedekleme & ayarlar” alanından dosyaları da içeren JSON yedeği indirin. Yedek içeri aktarmadan önce onay gerekir; mevcut kayıtların tamamının yerine geçer.

Dosya başına 20 MB, içe alınan yedek için 150 MB sınırı vardır. Depolama kapasitesi tarayıcıya bağlıdır. Hatırlatmalar site içinde gösterilir; e-posta ve arka plan bildirimi yoktur. Resmî tarihler otomatik gelmez; kullanıcı kendi kurumunun duyurularına göre ekler.

## Ücretsiz yayın

GitHub Free hesabında herkese açık bir depo ve GitHub Pages kullanılabilir. HTML/CSS/JavaScript dosyaları statik yayınlanır; sunucu veya ücretli hizmet gerekmez. Özel öğretmen belgelerini depoya koymayın; sitedeki evrak alanı dosyaları yalnızca tarayıcıya kaydeder.

Bağımsız bir depo açıldığında `index.html` kökte, `assets` klasörü yanında olmalıdır. Settings → Pages → Deploy from a branch → main → / (root) → Save. Ayrıntılı paylaşım rehberi: `YAYIN-REHBERI.md`.

Bu çalışma için ilk test yayını mevcut nazmihocaproje Pages sitesindeki `/ogretmen-takip-sistemi/` klasörü altında hazırlanmıştır; ana Merak Bahçesi uygulamasına dokunulmaz.
