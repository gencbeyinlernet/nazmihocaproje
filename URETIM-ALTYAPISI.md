# Görsel ve karakter sesi altyapısı

Üç örnek hikâye, her biri 7 sahne × 8 saniye olarak planlanmıştır. Toplam 21 ayrı görsel hazırdır. **Eski tek anlatıcılı kayıtlar kullanıcı tarafından reddedildi; yeni doğal Türkçe karakter sesleri henüz hazır değildir.**

4. sınıf 1.1 “Bir Selamın Açtığı Kapı”, 1.2 “Dilek Kutusundaki İyilik” kitap sırasındaki yerlerinde kalır. “Bir Saray, Bir Soru”, kullanıcının özgün metninden ayrı ek uyarlamadır. İlk kaynak metin `assets/source.txt` içinde değiştirilmeden korunur.

`assets/productions.js` beş hedef ses profili ve 21 sahnenin görsel, konuşmacı, replik, hareket, `voiceProfileId` ve ses durumunu içerir. Ece kız çocuk, Ali erkek çocuk, öğretmen kadın; anlatıcı ve rehber farklı yetişkin erkek sesleriyle planlanır. Bunlar ses tarifidir; hazır karakter kaydı olarak sunulmaz. Tam görev dosyası [SESLENDIRME-PLANI.md](SESLENDIRME-PLANI.md), makine tarafından okunabilen eşleştirme `ses-planlari/karakter-sesleri.json` içindedir.

Eski WAV dosyaları silinmez. Sahnenin `audioApproval` değeri `rejected` ise varsayılan ses kaynağı olarak seçilmez ve hazır ses sayısına eklenmez. Site sessiz görsel önizlemesiyle açılır. Eski kayıtları dinleme seçeneği açıkça kullanıcı tarafından işaretlenmelidir; bu, dosyanın onaylandığı veya yenilendiği anlamına gelmez. Seçim sayfa yenilenince sıfırlanır.

Yeni dosya geldiğinde `audioUrl`, ölçülen `audioDuration`, gerçek `audioVoice` ve inceleme sonrası `audioApproval: "approved"` alanları güncellenir. Her sahne ayrı replik kaydı kullanır; aynı karakterin farklı cümlelerinde tek bir ses dosyası tekrarlanmaz. Aynı karakter sesi hikâyeler boyunca korunur.

Sesli oynatım `ended` olayını bekler; uzun konuşmayı 8. saniyede kesmez. Varsayılan sessiz görsel önizlemesi 8 saniyede bir ilerler. Bilgisayardan seçilen deneme sesi yalnızca açık sayfada kalır, sunucuya yüklenmez ve yenilemede kaldırılır. Ses dosyası yokken veya oynatma engellendiğinde ses varmış gibi devam edilmez.

Bu ortamdan OpenAI.fm, OpenAI, ElevenLabs ve Microsoft ses hizmetlerine erişim kapalıdır. Bu nedenle yeni kaliteli kayıtların üretimi tamamlanamamıştır. Siteye bir API anahtarı eklenmez. Mevcut sistem ses dosyalarını ücretsiz statik yayından oynatır; video/MP4 üretilmez. `videoUrl` alanları boştur.
