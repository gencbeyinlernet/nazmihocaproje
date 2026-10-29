# Hikâye görselleri · 28 Ekim 2026

Aktif hikâyelerin simge veya çizim gösteren sahneleri, fotoğraf gerçekliğinde temsili görsellerle eşleştirildi. 48 kare; doğa, okul, ibadet, yardımlaşma, kültür, saray benzetmesi, üretim, tarihî çevre, düşünme, farklı dinlerin ibadet yapıları ve günlük yaşam konularını kapsar. 205 kütüphane hikâyesinin bütün sahnelerinde görsel vardır. Ortak iki hikâye, üç ilk üretim, sınıf konuları ve üniversite taslakları da eşleştirmeye dahildir.

Görseller OpenAI görsel üretim aracıyla bu çalışma için üretilmiştir. **Gerçek çekim veya tarihî olay belgesi değildir.** Kişiler kurgusaldır; benzer konularda aynı kare yeniden kullanılır. Her hikâye için ayrı bir oyuncu kadrosu veya her repliğe özel çekim yapıldığı iddia edilmez. Allah veya peygamber tasviri kullanılmaz. İbadet mekânları temsilidir; gerçek bir binanın mimari belgesi olarak değerlendirilmemelidir. Eski çizim dosyaları önceki üretim taslağı olarak korunur; aktif öğrenci oynatıcısı yeni görselleri gösterir.

## Eşleştirme ve doğrulama

- `assets/photo-data.js`: her görselin açıklaması, dosyası, görüntülenecek alanı ve sahne eşleştirmesi.
- `assets/photos/scene-map.json`: hikâye ve sahne bazında incelenebilir tam liste.
- `scripts/build-photo-library.cjs`: eşleştirmeleri yeniden üretir. Belirgin nesneler (arı, yağmur, robot, tren vb.) önceliklidir; diğer sahneler kitabın konu başlığıyla eşleştirilir. İlk üç üretim ve saray hikâyesi ayrıca elle eşleştirilmiştir.
- `tests/photo-library.cjs`: kapsam, dosya, görsel yüklenmesi, sahne geçişi ve mobil görünüm kontrolü.

Sayfada kolaj gösterilmez: her sahnede tek kare görünür. İndirme boyutunu azaltmak için dört kare aynı WebP dosyasında saklanır; SVG görüntü alanı yalnızca ilgili kareyi gösterir. Yükleme tamamlanmadan ses başlamaz; görsel yüklenemediğinde kullanıcıya yeniden deneme mesajı verilir. Ses metinleri ve ses dosyaları değiştirilmemiştir.
