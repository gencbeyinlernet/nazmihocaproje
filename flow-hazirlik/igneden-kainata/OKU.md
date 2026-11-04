# İğneden Kâinata · Görsel, metin ve sesler

59 sahnelik görsel planı ve 58 ayrı ElevenLabs ses kaydı hazırdır. 59. sahne konuşmasız kapanıştır; bu sahne için ses dosyası yoktur. Müzik veya ortam efekti üretilmedi.

- Görseller/metinler: `igneden-kainata-flow-sahneleri.zip`. İlk paketin HTML önizlemesi görsel ve metin içerir.
- Hazır sesler: `igneden-kainata-elevenlabs-sesleri.zip`. 58 MP3 ve dosya/metin/süre eşleştirmeleri içerir.
- Güncel web önizlemesinde görseli açıp sahnenin sesini dinleyebilir ve tek tek indirebilirsin.

Ses dosyasının başındaki numara, görselin başındaki sahne numarasıyla eşleşir. Örneğin `01-ali.mp3`, `01-gorsel.jpg` ile kullanılır. Video düzenleme programında numara sırasıyla birleştirebilirsin; sesler ayrı dosyalardır.

Bütün MP3 dosyaları ffprobe ile ölçülmüştür ve 8 saniyeden kısadır. Hızlandırma veya cümle kesme yapılmadı. Gerçek süreler `sesler/seslendirme-plani.csv` dosyasındadır. Flow görüntü süreleri ayrıca 8 saniyeyi geçmemelidir.

Metin `ozgun-metin.txt` dosyasında korunur. 58 konuşmanın metinleri birleştirildiğinde özgün kaynak sırası elde edilir; yalnızca boşluk ve tek başına duran nokta satırları düzenlenmiştir. Oyunculuk/efekt yönergeleri okutulmadı.

Sesler ElevenLabs / Eleven v4 modelinde Türkçe dil ayarıyla oluşturuldu. Dört karakter dört ayrı hazır sentetik ses kullanır. Ses kaynağı kimlikleri anadili Türkçe etiketli değildir. Ücretsiz hesapta kütüphane seslerinin API kullanımı kapalı olduğu için hazır çok dilli sesler seçildi. Ücretli abonelik satın alınmadı.

Görseller yapay zekâ ile oluşturulmuştur. Kişiler kurmacadır. Ses sağlayıcısı: https://elevenlabs.io/

Kaynak metin, yazarın inanç temelli benzetmelerini aktarır. Tren ve emir zinciri gibi örnekler benzetmedir; bilimsel veya hukuki açıklama olarak sunulmamalıdır. Öğretimde kullanım öncesi alan incelemesi ve seslerin son dinleme/telaffuz kontrolü yapılmalıdır.

## Tek video

59 görsel, 58 ses kaydıyla sahne numarası sırasına göre birleştirildi. `video.html` üzerinden izlenebilir; `indir/igneden-kainata-tam-video.mp4` dosyası tek MP4 olarak indirilebilir. Süresi 3 dakika 42 saniyedir; HD 1280×720, 30 fps, H.264/AAC biçimindedir. Son sahne 4 saniyelik sessiz kapanıştır. Sesler yeniden üretilmedi; mevcut ElevenLabs kayıtları kullanıldı. Konuşmalar kesilmedi veya hızlandırılmadı. Görüntü/ses eşleştirmeleri `kurgu-video.json` içinde saklıdır.
