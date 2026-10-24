# Türkçe örnek seslendirmeler

Bu klasördeki `anlatim/` kayıtları, sonradan kullanıcı kayıtlarıyla değiştirilebilen sentetik örneklerdir. Gerçek çocuk veya karakter oyuncusu kaydı değildir. Konuşmacı adları senaryodaki rolleri gösterir. İki yerel Türkçe model ve küçük ton/tempo farkları kullanılır; stüdyo kalitesinde karakter oyunculuğu olarak sunulmaz.

- Motor: Piper TTS 1.8.0.
- `tr_TR-fettah-medium`: model kartındaki veri kümesi lisansı CC0. Kaynak: https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-fettah-medium.tar.bz2
- `tr_TR-dfki-medium`: DFKI Türkçe veri kümesi; CC BY-NC-SA 4.0. Kaynak: https://github.com/marytts/dfki-ot-data/ ve https://huggingface.co/rhasspy/piper-voices/tree/main/tr/tr_TR/dfki/medium
- DFKI örnekleri kaynak gösterilerek, ticari olmayan amaçlarla, aynı lisansla paylaşılır: https://creativecommons.org/licenses/by-nc-sa/4.0/

Eski, reddedilen 4. sınıf WAV kayıtları arşivdedir; burada veya etkin oynatıcıda kullanılmaz. Bu kayıtlar yeni replikler için yeniden üretildi; sekiz saniyeye zorla sıkıştırılmadı, kesilmedi. Her MP3'ün metin/dosya özeti, rolü ve gerçek süresi `narration-manifest.json` dosyasındadır.

## Gerçek kayıtlarla değiştirme

Her MP3 bir sahne kimliği taşır. Aynı dosya adıyla yeni MP3 koyabilir veya sahnenin `audioUrl` alanına yeni dosya yolunu yazıp `audioApproval: "approved"` yapabilirsiniz. Oynatıcı onaylı özel kaydı örnek kayıttan önce kullanır ve her zaman gerçek `ended` olayını bekler. Özel kayıtlar geldikçe bu geçici modellere ait örnekler kaldırılabilir.
