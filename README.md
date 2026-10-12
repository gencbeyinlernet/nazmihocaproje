# Merak Bahçesi

Çocuklar için beş bölümden oluşan Türkçe öğrenme platformu. Her bölüm: özgün metne bağlı ayrı hikâye → Google Drive video klasörü → beş soruluk sınav. Sınavda her doğru yanıt 20 puandır. Tüm sorular cevaplandığında sonraki bölüm açılır; tekrar denemede en yüksek puan saklanır. Beş bölümün sonunda rozet ve yazdırılabilir katılım sertifikası açılır.

## Çalıştırma

Node.js paketleri veya derleme gerektirmez. Python 3 ile:

```sh
cd /workspace/nazmihocaproje
python3 -m http.server 3000 --bind 0.0.0.0
```

Herhangi bir statik web sunucusunda da çalışır. `index.html` dosyasını doğrudan açmak yerine HTTP üzerinden servis edin; özgün metin fetch ile yüklenir.

## İçerik

- `assets/source.txt`: Kullanıcının özgün metni; hikâyelerden ayrı tutulur.
- `assets/app.js`: Beş hikâye, 25 soru, video klasör bağlantısı ve uygulama akışı.
- `assets/style.css`: Mobil tasarım, klavye odağı ve sertifika yazdırma stili.

Videolar henüz üretilmedi veya bölümlere ayrı ayrı bağlanmadı. Şimdilik verilen ortak Drive klasörü açılır. Kullanıcı izlediğini işaretler; otomatik video izleme doğrulaması yoktur. Hikâyeler video senaryolarının ilk anlatı taslaklarıdır; sahne planı ve seslendirme metni ayrı bir üretim aşamasıdır.

İlerleme ve sertifika adı yalnızca tarayıcının localStorage alanında tutulur. Sunucu, kullanıcı hesabı, cihazlar arası eşitleme ve resmi sertifika doğrulaması yoktur. Google Fonts isteğe bağlıdır; erişilemezse yerel sans-serif font kullanılır. Yayına alma daha sonraki aşamadır.
