# Örnek Türkçe seslendirmeler

Üç hikâye için 21 ayrı **gerçek WAV dosyası**. Her dosya kendi sahnesinin repliğini okur; sesler bir sayfa açılınca yeniden üretilmez. Her kayıt 8 saniye, 22.050 Hz, tek kanal PCM 16 bittir. Konuşmadan önce 120 ms boşluk, sonuna sahneyi tamamlayan sessizlik eklenmiştir. Uzun iki kayıtta konuşma kesilmeden yaklaşık %9 hız düzenlemesi yapılmıştır. Ayrıntılar `manifest.json` dosyasındadır.

Sesler **örnek yapay zekâ anlatıcı kayıtlarıdır**; Ece/Ali/öğretmen gibi gerçek kişilerin veya çocukların ses kayıtları değildir. Replikteki konuşmacı rolünü tek bir Türkçe anlatıcı okur. Kullanıcı bunları sonradan kendi kayıtlarıyla değiştirebilir. OpenAI.fm bu çalışma ortamından erişilemediği için kullanılmamıştır.

## Kaynak

- Motor: [Piper TTS](https://github.com/OHF-Voice/piper1-gpl), 1.8.0; yalnızca üretim sırasında çevrimdışı çalıştırıldı. Site motoru, modelini veya bağımlılıklarını dağıtmaz.
- Ses: `tr_TR-fettah-medium`, Piper Türkçe. [Modelin alındığı Sherpa-ONNX dağıtımı](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-fettah-medium.tar.bz2).
- Eğitim veri kaynağı: [Nabu Casa voice-datasets](https://github.com/NabuCasa/voice-datasets), model kartına göre **CC0**. Alınan kart değiştirilmeden `VOICE-MODEL-CARD.txt` dosyasında korunur.
- DFKI modeli araştırılmış ancak kullanılmamıştır; bu dizindeki dosyalar Fettah sesiyle üretilmiştir.

`manifest.json`, her ses dosyasını sahne, konuşmacı, metin, süre ve SHA-256 ile eşler. İsteğe bağlı yeniden üretim: `pip install piper-tts==1.8.0`, FFmpeg ve yukarıdaki model; ardından proje klasöründe `python scripts/generate-voices.py --model /model/klasoru/tr_TR-fettah-medium.onnx`. Bu komut mevcut örnek WAV dosyalarını ve ses alanlarını yeniden yazar. Siteyi açmak için bu araçlar gerekmez.
