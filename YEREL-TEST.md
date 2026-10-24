# Bilgisayarında test et

1. [Yerel test paketini indir](https://gencbeyinlernet.github.io/nazmihocaproje/indir/merak-bahcesi-yerel-test.zip).
2. ZIP’i tamamen çıkar; `merak-bahcesi` klasörünü aç.
3. Windows’ta **BASLAT-WINDOWS.bat** dosyasına çift tıkla. Python 3 kuruluysa doğru proje klasörü otomatik açılır. Terminali açık bırak.

Mac/Linux için proje klasöründe `python3 BASLAT.py`; Windows terminalinde `py -3 BASLAT.py` veya `python BASLAT.py` kullanılabilir. Başlatıcı kendi klasörünü yayınlar; başka klasörün dosya listesini açmaz. Varsayılan 3000 portu doluysa boş port seçilir ve adres terminalde yazılır. Sayfayı HTML dosyasına çift tıklayarak açma.

## Kontrol edilecekler

- İlk açılışta ortak kullanım koşulları ve onay ekranı.
- Ana sayfanın ortasında hazır hikâyelerin kaydırmalı gösterisi, altında Ortaokul, Lise ve Üniversite seçenekleri.
- Geniş ekranda solda kategorili sınıf menüsü; mobilde “Sınıflar” düğmesiyle açılan menü ve seçili sınıf vurgusu. Menü sınıf seçince, kapatma düğmesiyle, dışına dokunarak veya Escape ile kapanır.
- Ortaokulda 5–8, lisede 9–12 sınıf seçimi; 4. sınıf kartı yoktur. Eski 4. sınıf/ilkokul adresleri 5. sınıfa yönlenir.
- 5. sınıfın ilk üç konu kartındaki görselli atölye bağlantıları.
- Atölyede üç hikâye, her hikâyede yedi ayrı görsel ve sahneye göre konuşmacı/replik.
- Öğrencide “Hikâyeye başla”, büyük görsel/replik ve Geri/İleri; en sonda “Bitirdim” ile tamamlanma rengi.
- Öğretmen görünümünde 8 saniyelik sahnelerle sessiz 56 saniyelik önizleme, önceki/sonraki sahne ve üretim araçları.
- Üniversitede üç özgün çalışma taslağı, tartışma soruları ve çalışma notu indirme; kaynakların henüz eklenmediği bilgisi.
- “Öğretmen görünümü” bağlantısında indirilebilir senaryo, seslendirme planı ve altyazı taslağı.
- Sağ üstteki “Soru sor” düğmesinin soru penceresini açması; altında diğer menüler. Mobilde diğer menüler açılır başlıktadır.
- Slaytların 7 saniyede otomatik geçmesi; durdurma/başlatma, oklar, seçim noktaları, klavye okları ve telefonda yatay kaydırma. Hareket azaltma tercihinde otomatik geçiş kapalıdır.
- Tam kullanım koşullarının isteğe bağlı açılması; onay zorunluluğunun korunması.
- Dar ekranlarda taşmayan mobil arayüz.
- İlk özgün metnin sekiz haftalık çalışması ve değiştirilmeden korunan kaynak metin.

Ses dosyaları kullanıcı tarafından en son eklenecek; şu an ses veya video bekleme durumu normaldir. Gerçek soru/özel cevap servisi bağlı değildir. 7. sınıfın kaynak sırası küçük/okunabilir kaynak dosyası bekler. Bunlar yerel sunucu hatası değildir.

Paket yalnızca aktif içerikleri taşır; eski 4. sınıf arşiv görselleri/sesleri pakete dahil değildir. Deneme sesi seçersen dosya yalnızca açık sayfada kullanılır; yenileyince kaldırılır. Sunucu sadece kendi bilgisayarında `127.0.0.1` üzerinden çalışır. Bitirince terminalde **Ctrl+C** ile durdur.
