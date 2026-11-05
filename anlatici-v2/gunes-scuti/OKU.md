# Güneş ve UY Scuti · Tek anlatıcılı sürüm

29 görsel sahne, tek ve kesintisiz anlatım. Konuşan karakter veya karşılıklı diyalog yoktur. Görseller anlatılan konuya göre değişir; hafif kamera hareketi kullanılır. Son sahnede anlatım bittikten sonra kısa bir sessiz kapanış vardır. Her sahne 8 saniyeden kısadır.

Ses: ElevenLabs API, eleven_v4_turbo, George. Sürekli kayıt anlatim.mp3 dosyasıdır. Videoda bu kayıt tek parça olarak kullanılır; görsel geçişlerinde ses yeniden başlatılmaz. Sahne sınırları, ElevenLabs'ın verdiği karakter zamanlamasıyla cümle aralarına yerleştirilir. sesler klasöründeki kayıtlar, aynı sürekli kayıttan alınan sahne kesitleridir. Ek müzik kullanılmamıştır.

Görseller önceki diyalog sürümünün uzay, doğa ve nesne sahnelerinden seçilmiştir; konuşan öğrenci ve öğretmen görselleri kullanılmamıştır. Her sahnenin özgün görsel numarası sahneler.json içindeki sourceScene alanındadır. Önceki dört karakterli diyalog sürümü arsiv/gunes-scuti-diyalog klasöründe korunur.

Üretim: scripts/build-gunes-scuti-narrator.py. Anlatım metni anlatim-sahneleri.json dosyasındadır; metin değişirse betik --tts ile yeniden çalıştırılır.

## Kaynak ve uyarlama

Yüklenen belgenin çıkarılan özgün metni ozgun-metin.txt dosyasında korunur. Bu sürüm birebir okuma değildir: bütün konu başlıklarını kısaltarak işleyen, bilimsel düzeltmeler içeren tek anlatıcılı bir uyarlamadır. Bilimsel açıklamalarla İslam inancına ilişkin yorumlar birbirinden ayrılmıştır.

Güneş'te yapılmış bombalar yoktur; çekirdekte doğal füzyon gerçekleşir. Tüp dükkânı benzetmesi Güneş'in patlamak zorunda olduğunu göstermez; kütleçekim ve basınç dengededir. Uzaya yayılan enerji yok olmaz. Kaynak metindeki "bir milyar atom bombası" ifadesi yerine, Hiroşima türü bomba ölçü alınarak saniyede yaklaşık altı trilyon bomba karşılaştırması verilir. Saatte 200 km ile 150 milyon km yaklaşık 85,6 yıldır (yuvarlanmış 86 yıl). Dev yıldızların hacim oranları yarıçap tahminlerine dayanır; kütle oranı değildir ve ölçümler değişebilir. Çar Bombası için yaygın yaklaşık 50 megaton ve eski 57 megaton tahminleri ayrıştırılır. 965 km ifadesi ateş topunun çapı olarak sunulmaz.

Görseller ve ses yapay zekâ ile oluşturulmuştur. Uzay görselleri temsilidir. Seslendirme: https://elevenlabs.io/

## Başvuru bağlantıları

- NASA, Sun Facts: https://science.nasa.gov/sun/facts/
- OpenStax, Astronomy 2e: https://openstax.org/details/books/astronomy-2e
- CTBTO, tarihsel nükleer test kayıtları: https://www.ctbto.org/
- Kullanıcının belgesindeki karşılaştırma bağlantısı: https://uzay.yetkinforum.com/t167-uy-scuti
