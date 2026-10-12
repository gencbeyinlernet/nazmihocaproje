# Merak Bahçesi

Çocuklar için sekiz bölümden oluşan Türkçe öğrenme platformu. Her bölüm: özgün metne bağlı ayrı hikâye → Google Drive video klasörü → konu oyunu → beş soruluk sınav. Oyun bitirilmeden sınava geçilemez; oyunlar sınav puanını etkilemez. Sınavda her doğru yanıt 20 puandır. Tüm sorular cevaplandığında sonraki bölüm açılır; tekrar denemede en yüksek puan saklanır. Sekiz bölümün sonunda rozet ve yazdırılabilir katılım sertifikası açılır.

## Çalıştırma

Node.js paketleri veya derleme gerektirmez. Python 3 ile:

```sh
cd /workspace/nazmihocaproje
python3 -m http.server 3000 --bind 0.0.0.0
```

Herhangi bir statik web sunucusunda da çalışır. `index.html` dosyasını doğrudan açmak yerine HTTP üzerinden servis edin; özgün metin fetch ile yüklenir.

## İçerik

- `assets/source.txt`: Kullanıcının özgün metni; hikâyelerden ayrı tutulur.
- `assets/app.js`: İlk beş bölüm ve uygulama akışı.
- `assets/activities.js`: Üç ek bölüm ve sekiz konu oyunu; toplam 40 soru.
- Oyun türleri: kavram eşleştirme, sıralama ve sınıflandırma. Mobil ve klavyeyle oynanır, zaman sınırı yoktur.
- Önceki beş bölümlük sürümde kaydedilen puanlar korunur; ek bölümler tamamlanınca sertifika yeniden açılır.
- `assets/style.css`: Mobil tasarım, klavye odağı ve sertifika yazdırma stili.

Videolar henüz üretilmedi veya bölümlere ayrı ayrı bağlanmadı. Şimdilik verilen ortak Drive klasörü açılır. Kullanıcı izlediğini işaretler; otomatik video izleme doğrulaması yoktur. Hikâyeler video senaryolarının ilk anlatı taslaklarıdır; sahne planı ve seslendirme metni ayrı bir üretim aşamasıdır.

İlerleme ve sertifika adı yalnızca tarayıcının localStorage alanında tutulur. Sunucu, kullanıcı hesabı, cihazlar arası eşitleme ve resmi sertifika doğrulaması yoktur. Google Fonts isteğe bağlıdır; erişilemezse yerel sans-serif font kullanılır. Yayına alma daha sonraki aşamadır.

## Kurum logosu

Kullanıcının yüklediği özgün `logo.jpg` başlıkta ve sertifikada doğrudan kullanılır. Görselin renkleri ve orantıları korunur; mobilde ve yazdırmada uygun boyutta gösterilir.
