# Eski ses denemeleri · yenilenecek

Bu dizindeki 21 WAV dosyası, önceki tek anlatıcılı Piper denemeleridir. **Türkçe akıcılık ve karakter uyumu bakımından kullanıcı tarafından uygun bulunmadı. Yeni karakter kayıtları henüz üretilmedi.**

Eski dosyalar arşivde korunur; varsayılan oynatımda ve hazır ses sayımında kullanılmaz. Yalnızca atölyedeki açık “Eski deneme kayıtları” seçeneğiyle dinlenebilir. Yeni ses hedefleri: Ece kız çocuk, Ali erkek çocuk, kadın öğretmen, ayrı erkek anlatıcı ve erkek rehber. Sahneye göre tam talimatlar: [SESLENDIRME-PLANI.md](../../SESLENDIRME-PLANI.md).

Her eski WAV 8 saniye, 22.050 Hz, tek kanal PCM 16 bittir. Kaynak: [Piper TTS](https://github.com/OHF-Voice/piper1-gpl) 1.8.0, `tr_TR-fettah-medium`. [Alınan model dağıtımı](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-fettah-medium.tar.bz2). Eğitim veri kaynağı [Nabu Casa voice-datasets](https://github.com/NabuCasa/voice-datasets), model kartına göre CC0; kart `VOICE-MODEL-CARD.txt` dosyasında aynen korunur. Model veya TTS motoru siteye dağıtılmaz.

`manifest.json` eski dosyaları metin, süre ve SHA-256 ile eşler; kalite durumu `rejected` olarak işaretlidir. Önceki üretici, aynı motorla tekrar kayıt oluşturmayı önlemek için kapatılmıştır. Yeni kaydın dosyası, süresi, ses profili ve `audioApproval: "approved"` bilgisi gerçek kayıt dinlenerek güncellenmelidir. Yalnızca hedef ses etiketi yazılması ses dosyası oluşturmaz.
