# Kayıtlı örnek sesler ve değiştirme planı

Önceki **232 Türkçe MP3** korunur; yeni konu kütüphanesine **1.225 ayrı Türkçe MP3** daha eklenmiştir. Toplam **1.457 kayıt** bağlıdır. Öğrenci/öğretmen görseli açıp dinler; uzun okuma metni takip etmez. Bunlar yerel modellerle üretilen, sonradan gerçek kayıtlarla değiştirilebilen sentetik örneklerdir. Gerçek çocuk veya karakter oyuncusu sesi oldukları iddia edilmez. Kaynak/lisans: [CREDITS.md](assets/audio/CREDITS.md).

## Eşleşmeler

- 5. sınıfın ilk üç hikâyesi: 21 sahne; Zehra, Ömer, Öğretmen ve Anlatıcı.
- Saraydan Dünyaya: 56 sahne; Elif, Deniz, Derya Öğretmen ve Anlatıcı.
- İğneden Kâinata: 28 sahne; aynı karakterler.
- Diğer hazır konuların ve üniversite taslaklarının anlatım/soruları: kalan kayıtlar.

Her dosya `assets/audio/anlatim/<grup>/<sahne-kimliği>.mp3` şeklindedir. Tam liste ve gerçek süreler `assets/audio/narration-manifest.json`; tarayıcıdaki karşılığı `assets/narration-data.js`. Her kaydın replik ve dosya SHA-256 özeti vardır. Kaynak metin ve replikler üretimde değiştirilmedi. Eski reddedilen 4. sınıf WAV'ları tekrar kullanılmadı.

## Gerçek sesleri gönderirken

Her replik ayrı kayıt olsun. Dosya adını sahne kimliğiyle eşleştirin; örneğin `gozlem-kulubu-02.mp3`, `ortak-01-02.mp3`, `ikinci-1-1.mp3`. MP3 veya WAV kabul edilir; yayımlamadan önce MP3'e dönüştürülebilir. Aynı karakterin sesi hikâyeler boyunca tutarlı olsun.

- Zehra / Elif: kız çocuk karaktere uygun, doğal ve meraklı ton.
- Ömer / Deniz: erkek çocuk karaktere uygun, canlı ve anlaşılır ton.
- Öğretmen / Derya Öğretmen: yetişkin kadın; sıcak ve sabırlı anlatım.
- Anlatıcı: yetişkin erkek; akıcı ve dengeli hikâye anlatımı.

Bu tarifler **gelecek kayıtların hedefidir**; mevcut yerel modellerin bu yaş/cinsiyetlere sahip gerçek ses sanatçıları olduğu anlamına gelmez. Konuşmayı hızlandırmadan, mekanik hecelemeden ve gereksiz dramatizasyondan kaçının. İlk üretim hedefi sekiz saniyedir; anlaşılır söyleyiş daha uzun sürüyorsa konuşmayı kesmeyin. Oynatıcı her zaman gerçek sesin sonunu bekler.

## Dosya geldiğinde

İlgili sahnede `audioUrl` yeni dosya yolu, `audioDuration` gerçek saniye, `audioApproval: "approved"` yapılır. Onaylı özel kayıt geçici örnekten önce kullanılır. `audioApproval: "rejected"` çalmaz. Başka bir URL kullanmadan aynı MP3'ü aynı dosya adıyla değiştirmek de mümkündür; önbellek sürümü güncellenir. Örnekler değiştikçe model lisansına bağlı geçici sesler kaldırılabilir.

Öğretmen atölyesinde kendi kaydını geçici denemek mümkündür: dosya sunucuya yüklenmez, sayfa yenilenince kaldırılır. Kalıcı yayına bağlama ayrı dosya güncellemesidir.

Yeni 198 hikâyenin ses listesi `ses-planlari/kutuphane-ses-metinleri.json`, kayıt özeti `assets/audio/library-manifest.json` dosyalarındadır. Her ses `kutuphane-<konu>-<örnek>-<sahne>.mp3` biçiminde eşleştirilir.
