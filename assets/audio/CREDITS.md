# Türkçe örnek seslendirmeler

Bu klasördeki `anlatim/` kayıtları, sonradan kullanıcı kayıtlarıyla değiştirilebilen sentetik örneklerdir. Gerçek çocuk veya karakter oyuncusu kaydı değildir. Konuşmacı adları senaryodaki rolleri gösterir. Erkek anlatıcı ve erkek rollerinde yerel Piper örnekleri; kadın rollerinde aşağıda açıklanan yeni Emel kayıtları kullanılır. Stüdyo oyunculuğu veya gerçek çocuk sesi olarak sunulmaz.

- Motor: Piper TTS 1.8.0.
- `tr_TR-fettah-medium`: model kartındaki veri kümesi lisansı CC0. Kaynak: https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-fettah-medium.tar.bz2
- Önceki sürümde kullanılan `tr_TR-dfki-medium`: DFKI Türkçe veri kümesi; CC BY-NC-SA 4.0. Kaynak: https://github.com/marytts/dfki-ot-data/ ve https://huggingface.co/rhasspy/piper-voices/tree/main/tr/tr_TR/dfki/medium
- Önceki DFKI örnekleri kaynak gösterilerek, ticari olmayan amaçlarla, aynı lisansla paylaşılır: https://creativecommons.org/licenses/by-nc-sa/4.0/

Eski, reddedilen 4. sınıf WAV kayıtları arşivdedir; burada veya etkin oynatıcıda kullanılmaz. Bu kayıtlar yeni replikler için yeniden üretildi; sekiz saniyeye zorla sıkıştırılmadı, kesilmedi. Her MP3'ün metin/dosya özeti, rolü ve gerçek süresi `narration-manifest.json` dosyasındadır.

## Gerçek kayıtlarla değiştirme

Her MP3 bir sahne kimliği taşır. Aynı dosya adıyla yeni MP3 koyabilir veya sahnenin `audioUrl` alanına yeni dosya yolunu yazıp `audioApproval: "approved"` yapabilirsiniz. Oynatıcı onaylı özel kaydı örnek kayıttan önce kullanır ve her zaman gerçek `ended` olayını bekler. Özel kayıtlar geldikçe bu geçici modellere ait örnekler kaldırılabilir.

## Yeni konu kütüphanesi

`anlatim/kutuphane/` altındaki 1.225 yeni kayıt yalnızca CC0 veri kümesi kullanan `tr_TR-fettah-medium` modeliyle oluşturulmuştur. Önceki DFKI örneklerinin lisansı değişmez. Yeni anlatımlar geçici sentetik anlatıcı örnekleridir; gerçek karakter oyuncusu kaydı değildir. Kayıt ve metin özetleri `library-manifest.json` içinde bulunur.

## Örnek dersin etkinlik sesleri

`etkinlik/` altındaki 27 ayrı MP3, 5. sınıf Evrendeki Mükemmel Düzen dersinin yönerge, soru/seçenek, ipucu, açıklama ve sonuç sesleridir; yaklaşık 6,2 dakika sürer. Yalnız yukarıda kaynağı verilen CC0 veri kümesine sahip Fettah modeli kullanılmıştır. Bunlar değiştirilebilir sentetik anlatıcı örnekleridir; çocuk sesi veya gerçek öğretmen kaydı olarak sunulmaz.

Kaynak metinler `ses-planlari/etkinlik-ses-metinleri.json`, üretim betiği `scripts/generate-activity-audio.py` içindedir. Dosya ve metin SHA-256 özetleri, gerçek süreler ve lisans bilgisi `activity-manifest.json` dosyasındadır. Tarayıcı eşleştirmesi `assets/activity-narration.js` içindedir. Gerçek kayıtlarla değiştirirken bu eşleştirme ve manifest birlikte güncellenir. Önceki hikâye kayıtlarının lisans koşulları değişmez.

## 28 Ekim 2026 ek hikâyeleri

`anlatim/kutuphane/ek20261028-*.mp3` biçimindeki 49 yeni kayıt, yukarıdaki CC0 veri kümesine sahip Fettah modeliyle oluşturulmuştur. Sentetik anlatıcı örnekleridir; özgün metinler `ses-planlari/yeni-hikayeler-20261028.json`, eşleştirmeler `library-manifest.json` içindedir.

28 Ekim mobil düzenleme: Son 49 Fettah anlatıcı kaydı aynı metinlerle, 1,02 uzunluk ölçeği ve 48 kbps MP3 olarak yeniden üretildi. Hedef ses seviyesi -18 LUFS, tepe sınırı -2 dBTP; 70 Hz alt frekans süzme uygulandı. Kaynak/model lisansı değişmez. Üretim betiği `scripts/polish-recent-audio.py` dosyasındadır.

## 29 Ekim 2026 · Yeni kadın sesi

Kullanıcının `yeni-kadin-sesleri.zip` dosyasındaki 60 kayıt, eski DFKI kadın rolü kayıtlarının tamamının yerine eklendi: Zehra 6, Elif 26, Öğretmen 6, Derya Öğretmen 22. Ses, Microsoft Edge çevrim içi TTS hizmetindeki `tr-TR-EmelNeural` sesidir. Kadın öğretmen repliklerinde hız -%3, diğer kadın rollerinde normal hız ve değiştirilmeyen perde kullanılmıştır. Bu sesler sentetiktir; çocuk rollerinde de yetişkin sentetik ses kullanılır. Hizmet sağlayıcının kullanım koşulları geçerlidir; Piper veri kümesi lisansları bu yeni kayıtlara atfedilmez.

Yüklenen MP3 dosyaları yeniden kodlanmadan korunmuştur. 60 dosyanın metin/dosya özetleri, çözümlenebilirliği ve gerçek süreleri doğrulanmıştır. Toplam süre yaklaşık 9 dakika 6 saniyedir. Erkek sesleri, özgün replikler ve görseller değişmemiştir. Yeni dosya özetine bağlı bağlantı sürümü, tarayıcının eski kadın sesini önbellekten çalmasını önler.

İçe aktarma: `python scripts/import-female-audio.py <yeni-kadin-sesleri.zip>`. Betik bütün kayıtları doğrulamadan dosyaları değiştirmez. İlgili sahne veri dosyalarındaki süre/ses tanımları da manifestle birlikte güncellenmiştir. Sonraki Piper üretimi, yeni içe aktarılmış kayıtları korur.

## 29 Ekim 2026 · Sahne efektleri

`ambience/` altındaki sekiz efekt bu proje için `scripts/build-scene-sounds.py` ile sentezlenmiştir. Alan kaydı veya müzik değildir. Konuşma kayıtlarını değiştirmeyen, ayrı oynatılan ve kapatılabilen düşük seviyeli bir katmandır. Kaynak ve sınırlar: [HIKAYE-SES-TASARIMI.md](../../HIKAYE-SES-TASARIMI.md).
