# Türkçe örnek seslendirmeler

Bu klasördeki `anlatim/` kayıtları, sonradan kullanıcı kayıtlarıyla değiştirilebilen sentetik örneklerdir. Gerçek çocuk veya karakter oyuncusu kaydı değildir. Konuşmacı adları senaryodaki rolleri gösterir. İki yerel Türkçe model ve küçük ton/tempo farkları kullanılır; stüdyo kalitesinde karakter oyunculuğu olarak sunulmaz.

- Motor: Piper TTS 1.8.0.
- `tr_TR-fettah-medium`: model kartındaki veri kümesi lisansı CC0. Kaynak: https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-fettah-medium.tar.bz2
- `tr_TR-dfki-medium`: DFKI Türkçe veri kümesi; CC BY-NC-SA 4.0. Kaynak: https://github.com/marytts/dfki-ot-data/ ve https://huggingface.co/rhasspy/piper-voices/tree/main/tr/tr_TR/dfki/medium
- DFKI örnekleri kaynak gösterilerek, ticari olmayan amaçlarla, aynı lisansla paylaşılır: https://creativecommons.org/licenses/by-nc-sa/4.0/

Eski, reddedilen 4. sınıf WAV kayıtları arşivdedir; burada veya etkin oynatıcıda kullanılmaz. Bu kayıtlar yeni replikler için yeniden üretildi; sekiz saniyeye zorla sıkıştırılmadı, kesilmedi. Her MP3'ün metin/dosya özeti, rolü ve gerçek süresi `narration-manifest.json` dosyasındadır.

## Gerçek kayıtlarla değiştirme

Her MP3 bir sahne kimliği taşır. Aynı dosya adıyla yeni MP3 koyabilir veya sahnenin `audioUrl` alanına yeni dosya yolunu yazıp `audioApproval: "approved"` yapabilirsiniz. Oynatıcı onaylı özel kaydı örnek kayıttan önce kullanır ve her zaman gerçek `ended` olayını bekler. Özel kayıtlar geldikçe bu geçici modellere ait örnekler kaldırılabilir.

## Yeni konu kütüphanesi

`anlatim/kutuphane/` altındaki 1.225 yeni kayıt yalnızca CC0 veri kümesi kullanan `tr_TR-fettah-medium` modeliyle oluşturulmuştur. Önceki DFKI örneklerinin lisansı değişmez. Yeni anlatımlar geçici sentetik anlatıcı örnekleridir; gerçek karakter oyuncusu kaydı değildir. Kayıt ve metin özetleri `library-manifest.json` içinde bulunur.

## Örnek dersin etkinlik sesleri

`etkinlik/` altındaki 27 ayrı MP3, 5. sınıf Evrendeki Mükemmel Düzen dersinin yönerge, soru/seçenek, ipucu, açıklama ve sonuç sesleridir; yaklaşık 6,2 dakika sürer. Yalnız yukarıda kaynağı verilen CC0 veri kümesine sahip Fettah modeli kullanılmıştır. Bunlar değiştirilebilir sentetik anlatıcı örnekleridir; çocuk sesi veya gerçek öğretmen kaydı olarak sunulmaz.

Kaynak metinler `ses-planlari/etkinlik-ses-metinleri.json`, üretim betiği `scripts/generate-activity-audio.py` içindedir. Dosya ve metin SHA-256 özetleri, gerçek süreler ve lisans bilgisi `activity-manifest.json` dosyasındadır. Tarayıcı eşleştirmesi `assets/activity-narration.js` içindedir. Gerçek kayıtlarla değiştirirken bu eşleştirme ve manifest birlikte güncellenir. Önceki hikâye kayıtlarının lisans koşulları değişmez.
