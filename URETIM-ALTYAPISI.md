# 5. sınıftan başlayan görsel ve ses altyapısı


> 24 Ekim 2026 güncellemesi: Hazır içeriklere 232 ayrı Türkçe örnek MP3 bağlandı. Öğrenci akışı artık görsel + ses oynatımıdır; aşağıdaki yazılı dökümler öğretmenin senaryo arşividir. Sekiz saniye üretim hedefidir; oynatıcı konuşmayı kesmez. Güncel ses durumu ve değiştirme yolu SESLENDIRME-PLANI.md içindedir.

Kullanıcı isteğiyle aktif çalışma 5. sınıftan başlar; ses kayıtları en son eklenecektir. 4. sınıfın önceki verileri, görselleri ve reddedilen sesleri `arsiv/4-sinif/` altında korunur ve uygulama tarafından yüklenmez.

5. sınıf kitabının sırasındaki ilk üç konuya ait üç bağlantılı senaryo vardır: Evrendeki Mükemmel Düzen (s. 14), Allah’ın Varlığı ve Birliği (s. 20), Allah’ın Güzel İsimleri (s. 29). Her içerik 7 sahne × 8 saniye = 56 saniyedir. Toplam 21 yeni görsel, her sahneye ait konuşmacı, replik ve ilerideki hareket tarifi bulunur. Ses/video alanları boştur; görseller sessiz önizlenir.

`assets/productions.js` aktif senaryoları ve Zehra, Ömer, öğretmen, anlatıcı ses profillerini tutar. Profiller ses tarifidir; oluşturulmuş kayıt gibi gösterilmez. `assets/scenes/<hikâye>/<01..07>.png` ayrı görsellerdir. Senaryo ve altyazı taslakları `video-ornekleri/7-sahne-*/` altındadır.

Kullanıcı sesi yüklediğinde ilgili sahnenin `audioUrl`, ölçülen `audioDuration`, gerçek `audioVoice` ve `audioApproval: "approved"` alanları güncellenir. Her sahne ayrı replik kaydı kullanır; bir karakterin farklı repliklerinde aynı dosya tekrarlanmaz. `SESLENDIRME-PLANI.md` ve `ses-planlari/karakter-sesleri.json`, sahne/karakter/dosya eşleştirmesini içerir.

Oynatıcı onaylı ses veya cihazdan seçilmiş deneme sesi varsa sesli çalışabilir; `ended` olayını bekler ve uzun kaydı 8. saniyede kesmez. Ses bulunmaz veya oynatılamazsa durur ve bilgi verir. Öğrenci görünümü elle Geri/İleri ile ilerler ve tüm görseller ziyaret edilip “Bitirdim” denince okuma ilerlemesini kaydeder. `?gorunum=ogretmen` ile açılan üretim görünümünde sessiz önizleme 8 saniyede bir ilerler. Deneme dosyası yalnızca açık sayfada kalır, sunucuya yüklenmez ve yenilemede kaldırılır. Video/MP4 üretilmez; görsel eklenmesi bir konuyu video izlenmiş yapmaz.

Replikler yaş düzeyine uygun özgün uyarlamalardır. Kitap başlıkları ve sırası korunur; tam kitap metinleri veya PDF’leri yayımlanmaz. Kullanıcının ilk özgün metni `assets/source.txt` içinde değişmeden korunur. Kurum logosu kullanıcının sağladığı gerçek `logo.jpg` dosyasıdır.

## Görünüm ayrımı

`assets/studio.js` sade öğrenci oynatıcısıdır; üretim araçları `assets/studio-authoring.js` içinde, yalnızca öğretmen görünümü seçildiğinde yüklenir. Sınıfların sade akışı `portal.js`, tüm planları inceleme görünümü `portal-authoring.js` ile çalışır. Görünüm seçimi bir yetkilendirme mekanizması değildir. Ortaokul, lise ve üniversite girişleri ayrıdır; üniversite tartışma taslakları kaynak seçimi bekler ve sınıf kataloğunun kitap sırasını değiştirmez.
