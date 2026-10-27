# Görsel başına Türkçe seslendirme

Aktif içerikler video beklemeden görsel ve kayıtlı sesle çalışır. Her sahne kendi MP3 dosyasına bağlıdır. 1.457 hikâye kaydına, örnek dersin 27 etkinlik sesi eklendi: toplam 1.484 MP3 yaklaşık 160 dakika sürer. Oynatıcı sesi sekiz saniyeye sıkıştırmaz veya kesmez. Kullanıcı İzle ve dinle düğmesine dokunur; Otomatik oynat seçilirse kayıt bitince sonraki görsel ve onun sesi başlar.

Bunlar sonradan değiştirilebilen sentetik Türkçe örneklerdir. Konuşmacı adları hikâyedeki rolleri gösterir; gerçek çocuk veya karakter oyuncusu kaydı değildir. Kaynak ve lisanslar [CREDITS.md](CREDITS.md) dosyasındadır.

İlk 232 kaydın sahne kimliği, metin özeti, yolu ve süresi `narration-manifest.json`; kütüphanedeki 1.225 yeni kaydın karşılıkları `library-manifest.json` içindedir. Bir sahneye yeni ses eklendiğinde `audioUrl` ve `audioApproval: "approved"` kullanılır; onaylı kayıt geçici örnekten önce çalar. Ayrıntılar [seslendirme planında](../../SESLENDIRME-PLANI.md) bulunur.

27 etkinlik kaydı `etkinlik/` altında, ayrı `activity-manifest.json` ve `assets/activity-narration.js` eşleştirmesiyle bulunur. Bu sesler soru ve seçenekleri, ipuçlarını, açıklamaları ve sonuçları okur. Dinle/Duraklat, yeniden deneme ve menü açılınca durma desteklenir. Sayfa yenilendiğinde ses kendiliğinden başlamaz.

Videolar daha sonra aynı içeriklere eklenecek; mevcut MP3 dosyaları video dosyası olarak sunulmaz. Şimdiki öğrenci deneyimi uzun okuma metni yerine görsel ve ses oynatıcısıdır. Önceki 4. sınıf denemeleri arşivde korunur ve aktif uygulama tarafından yüklenmez.
