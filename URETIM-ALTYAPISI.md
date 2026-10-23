# Sahne ve seslendirme üretim altyapısı

Her içerik 7 sahneden, her sahne 8 saniyeden oluşur: toplam **56 saniye**.

İlk örnekler: 4. sınıf 1.1 “Bir Selamın Açtığı Kapı”, 4. sınıf 1.2 “Dilek Kutusundaki İyilik” ve özgün saray metnine bağlı ek çalışma “Bir Saray, Bir Soru”. İlk iki içerik kitap sırasındaki yerinde kalır; saray çalışması kitaptan alıntı veya yeni bir müfredat konusu gibi gösterilmez.

`assets/productions.js` içerik, sahne, görsel, konuşmacı, replik, hareket tarifi ve boş ses/video bağlantılarını tutar. `sahne-atolyesi/` görselleri ve konuşmaları incelenebilir hâlde gösterir. Ayrı görsel dosyaları `assets/scenes/<içerik>/<01..07>.png` altındadır. Görseller özgün yapay zekâ üretimidir; kullanılan kurum logosu kullanıcının sağladığı gerçek logodur.

Sahne önizlemesi, 8 saniyede bir değişen görsellerdir; üretilmiş MP4 veya animasyon olarak sunulmaz. Seslendirmeyi kullanıcı hazırlayacaktır. `audioUrl` ve `videoUrl` alanları bu yüzden boştur. Geçerli medya bağlantıları eklendiğinde oynatıcı bunları kullanır. Bilgisayardan seçilen deneme sesi yalnızca açık sayfada kullanılır; sunucuya yüklenmez veya yayına kalıcı kaydedilmez.

Replikler yaşa uygun özgün uyarlamalardır; ayet/hadis veya özgün metnin doğrudan alıntısı olarak sunulmaz. Yedi sahnenin toplamı değiştirilemez süre gibi video üretim aracına zorlanmaz: gerçek sesler 8 saniyeye sığmıyorsa kurgu öncesinde düzenlenmelidir. Ses taslağında kelime sayısı kısa tutulmuştur; kesin süre gerçek ses kaydıyla ölçülür.

Genişletme: aynı şemayla yeni içerik ekle, 7 ayrı görselini yerleştir. Seslendirmeler geldiğinde sahnelere `audioUrl`, klipler geldiğinde `videoUrl`. Tamamı birleştirilmiş video geldiğinde dersin `assets/catalog.js` içindeki `videoUrl` alanı bağlanabilir. Sırf resim veya ses eklenmesi bir konuyu video izlenmiş/tamamlanmış yapmaz.
