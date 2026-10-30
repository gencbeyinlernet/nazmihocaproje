# Hikâye ses tasarımı

29 Ekim 2026 düzenlemesi, mevcut konuşma kayıtlarının üzerine ayrı ve kapatılabilir bir sahne sesi katmanı ekler. MP3 replikleri, konuşmacılar ve sözcükler değişmez. Hazır kayıtta bulunmayan bir oyunculuk veya vurgunun sonradan yaratıldığı iddia edilmez.

## Oynatım

- Bahçe, yağmur, akan su, arı, sayfa çevirme, yazma, tren ve küçük robot için sekiz özgün sentetik efekt vardır. Alan kaydı, gerçek kuş kaydı veya müzik değildir.
- Efektler ilgili nesne veya eylem replikte geçtiğinde kullanılır; genel dinî açıklamalarda zorunlu fon çalmaz. Görsel eşleştirmesi de kontrol edilir.
- Efekt dosyalarının tepe hedefi -27 dBFS'dir ve oynatıcı ses düzeyi 0,75'tir. Konuşmanın önüne geçmemesi amaçlanır. Mobil tarayıcı ses düzeyini değiştirmese de dosyanın kendisi düşük seviyededir.
- “Diğer seçenekler → Hafif sahne sesleri” kapatılabilir; tercih cihazda saklanır. Fon hatası konuşmayı durdurmaz. Duraklatma, gezinme, açılan menü, arka plana geçme veya ses yükleme beklemesi efektleri de durdurur.
- Otomatik geçişte soru sonrasında 700 ms, konuşmacı değişiminde 380 ms, diğer geçişlerde 280 ms ve soru içermeyen son sahnede 450 ms düşünme payı bırakılır. Duraklatma veya otomatik oynatmayı kapatma bu beklemeyi iptal eder. Hiçbir konuşma kesilmez.

## Ses oyunculuğunun sonraki kaydı

`ses-planlari/oyunculuk-yonergeleri.json`, ilk üç sınıf hikâyesi ve iki ortak hikâyenin 105 repliği için konuşma niyeti, önerilen vurgu ve durak yönlendirmesini içerir. Metinler aynıdır. Bu yönetim talimatları yeni kayıt veya ifade denetimini destekleyen bir ses motoru içindir; mevcut Emel/Piper kayıtlarına uygulanmış gibi gösterilmez. Bir sesin duygusunu yalnızca hız veya perde değiştirerek düzeltmeye çalışmayız.

Dosyalar `scripts/build-scene-sounds.py` ile yeniden üretilebilir. Ses–görsel eşleştirmesi `assets/story-sound.js` içindedir. Konuşma dosyalarındaki SHA-256 değerleri değişmez.
