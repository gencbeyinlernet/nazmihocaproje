# Görsel ve seslendirme üretim altyapısı

Her içerik 7 sahne × 8 saniye olarak planlanmıştır: toplam **56 saniye**. Şu an üç örneğin **21 görseli ve 21 ayrı Türkçe ses kaydı** vardır; video dosyası üretilmez.

İlk örnekler: 4. sınıf 1.1 “Bir Selamın Açtığı Kapı”, 4. sınıf 1.2 “Dilek Kutusundaki İyilik” ve özgün saray metnine bağlı ek çalışma “Bir Saray, Bir Soru”. İlk iki içerik kitap sırasındaki yerinde kalır; saray çalışması kitaptan alıntı veya yeni bir müfredat konusu gibi gösterilmez. Diğer sınıf/konularda görsel veya ses hazırmış gibi durum gösterilmez.

`assets/productions.js` sahne, görsel, konuşmacı, replik, hareket tarifi ve ses dosyası bağlantılarını tutar. Görseller `assets/scenes/<içerik>/<01..07>.png`, sesler `assets/audio/<içerik>/<01..07>.wav` altındadır. Kullanılan kurum logosu kullanıcının sağladığı gerçek logodur. `videoUrl` alanları boştur.

`sahne-atolyesi/` varsayılan olarak **Görsel + seslendirme** oynatır. Her sahnenin gerçek ses dosyası açılır; `ended` olayı gelmeden sonraki görsele geçilmez. Duraklatma, devam etme, önceki/sonraki sahne ve başa dönme kullanılabilir. Ses yüklenemez veya tarayıcı oynatmayı engellerse oynatım durur; ses varmış gibi sessiz devam edilmez. Ayrı **Sessiz görsel önizleme** seçeneği, 8 saniyede bir görüntü değiştirir.

Mevcut örnek WAV dosyaları tam 8 saniyedir. Kullanıcının deneme sesi daha uzunsa görsel, konuşmayı kesmeden ses tamamlanana kadar kalır. Deneme sesi yalnızca açık sayfada kullanılır, sunucuya yüklenmez, yenilemede kaldırılır ve yayımlanan örnek ses geri gelir. Kalıcı yayın için sahnenin `audioUrl` alanı değiştirilmelidir.

Örnek sesler ücretsiz, çevrimdışı Piper Türkçe motoruyla oluşturulmuştur; **OpenAI.fm sesi veya karaktere özel oyuncu kaydı değildir**. Tek anlatıcı, repliklerdeki rolleri okur. Kaynak/model kartı ve ses dosyası dökümü: [assets/audio/README.md](assets/audio/README.md). Kullanıcı örnekleri sonradan kendi kayıtlarıyla değiştirebilir. Ses üretimi için bir API anahtarı veya sitede çalışan ücretli hizmet yoktur.

Replikler yaşa uygun özgün uyarlamalardır; ayet/hadis veya özgün metnin doğrudan alıntısı olarak sunulmaz. İlk özgün metin `assets/source.txt` içinde değişmeden korunur. Gerçek sesler değiştiğinde süreler yeniden ölçülür; SRT taslağı 8 saniyelik örneklere aittir.

Genişletme: kitap sırasıyla yeni hikâyeyi hazırlayıp 7 ayrı görsel ve bunların 7 ayrı sesini aynı şemaya ekle. Klipler ileride gelirse `videoUrl` bağlanabilir. Görsel veya ses eklenmesi bir konuyu video izlenmiş/tamamlanmış yapmaz.
