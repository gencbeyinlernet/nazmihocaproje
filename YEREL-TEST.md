# Yerelde test

Proje dosyalarını açtıktan sonra Windows'ta **BASLAT-WINDOWS.bat** dosyasına çift tıkla. Diğer sistemlerde proje klasöründe `python3 BASLAT.py` çalıştır. Terminalde yazan `http://localhost:3000/` veya seçilen boş portun adresini aç. HTML dosyasını doğrudan açma; başlatıcı proje klasörünü yayınlar.

1. Site kullanıcı adı, şifre ve sözleşme onayı olmadan açılmalı.
2. Ana sayfada sınıf ve konu seç. **İzle ve dinle** düğmesine bas: görsel açılmalı ve o sahnenin sesi duyulmalı.
3. Konuşma bitince aynı görselde beklemeli. **İleri** düğmesine dokununca sonraki görsel ve onun sesi başlamalı. Ses sekiz saniyeyi aşarsa konuşma kesilmemeli.
4. Duraklat/Devam et çalışmalı. Geri/İleri düğmesiyle açılan görsel kendi sesini başlatmalı; önceki ses aynı anda sürmemeli.
5. Uzun okuma metni görünmemeli. İstersen **Diğer seçenekler → Altyazı** düğmesiyle yalnızca o sahnenin metnini açıp kapatabilmelisin.
6. Ortak ilk hikâyede 56, ikinci hikâyede 28, 5. sınıfın üç hikâyesinde toplam 21 sahne sesi bulunur. Diğer hazır konular ve üniversite taslakları da kayıtlı sesleriyle açılır.
7. Sahneleri yalnızca açıp geçmek tamamlanma değildir. Konuşmaları dinleyip Bitir'e basınca dinleme tamamlanmalı ve ilgili bölüm renklenmeli. Oyun/sınav içeren ilk örnek derste bütün dersin tamamlandı sayılması için bu aşamalar da bitirilmeli.
8. Mobilde Sınıflar düğmesi soldan menüyü açmalı. Menü açılınca veya sekmeden çıkınca ses durmalı. Altyazı, oynatma ve ileri/geri düğmeleri dar ekranda taşmamalı.
9. Öğretmen için Derse hazırlan alanında sınıf/ünite/konu ve ders hedefi düzenlenebilir. Sınıfta sun, sesli oynatıcıyı açar; Planı indir ve Yazdır / PDF öğretmen planını verir.
10. Öğretmenin değiştirdiği giriş için cihazda Türkçe metin sesi bulunması gerekir. Yoksa mesaj gösterilir; İleri ile kayıtlı hikâyeye geçilebilir. Platformdaki hazır MP3'ler cihaz sesine bağlı değildir.
11. Öğretmen senaryo görünümünde her sahnenin sesi dinlenebilir; kendi MP3/WAV kaydınla geçici deneme yapılabilir. Bu dosya sunucuya yüklenmez.
12. Özgün iki kaynak metin öğretmen ayrıntılarında değişmeden açılıp indirilebilir. Hikâyeler ve sayfa bağlantıları paylaşılabilir.

İlk oynatma için bir dokunuş gerekir; tarayıcılar kullanıcı dokunuşu olmadan sesi başlatmayabilir. Ses düğmesi açık olduğu hâlde ses duyulmuyorsa cihaz ve tarayıcı sekmesinin sesini kontrol et.

1.457 hikâye sesi ve 27 etkinlik sesi (toplam 1.484 MP3, yaklaşık 160 dakika) indirilen yerel pakete dahildir. Geçici sentetik Türkçe örneklerdir; daha sonra kendi kayıtlarımızla değiştirilebilir. Gerçek çocuk/karakter oyuncusu veya stüdyo kaydı değildir. [Ses kaynak ve lisansları](assets/audio/CREDITS.md).

Gerçek soru/özel cevap servisi henüz bağlı değildir; bu nedenle gönderme/sorgulama kapalıdır. 7. sınıfın doğrulanmış kaynak sırası hazırlanıyor. Bunlar yerel sunucu hatası değildir.

Kütüphane testi: Ana sayfada 5. sınıfı seçip “namaz” yazın. Hikâyeleri bul ile ilgili kitap konuları ve her konunun örnekleri açılmalı. Sınıf sayfalarında konu sırası korunmalı; ünite filtresi ve sonraki konular düğmesi çalışmalı. 7. sınıfta doğrulanmış sıra bekleniyor bilgisi görünmeli.

Otomatik test: Bir hikâyeyi açıp **Otomatik oynat** anahtarını açın. Her kayıt bitince sonraki görselin sesi başlamalı; İleri veya Bitir düğmesine basmadan tüm hikâye tamamlanmalı. Anahtarı kapatınca mevcut kayıt sürmeli ve bitişinde beklemeli. Duraklatıp devam etme, menü açınca durma ve eksik ses dosyasında ilerlememe çalışmalı. Tüm sahneler dinlenmeden tamamlandı kaydı oluşmamalı. Destekleyen cihazlarda otomatik izleme sırasında ekran uyanık tutulur.

## İlk kez gelen öğrenci

Ana adres Keşfe başla ekranını açar. Sınıf seçimi ilk keşfin önizlemesine götürür; İzle ve dinle düğmesi kayıtları başlatır. Tamamlandı ekranında Sonraki keşfe geç önerisi görünür. Keşif yolum menüsünden istediğin içeriğe geri dönülebilir. Yenileme ve geri dönüşte aynı cihazdaki ilerleme korunur; ses izin almadan başlamaz. Öğretmen alanı konu aramasına doğrudan gider. Önceki serbest ekran `kesfet/` adresindedir.

## Oyun ve sınav içeren örnek dersi dene

Yerel sunucu açıkken `http://localhost:3000/sahne-atolyesi/#icerik=gozlem-kulubu` adresini aç; başlatıcı başka port seçtiyse onu kullan.

1. **İzle ve dinle** ile yedi sahneyi dinle. İstersen Otomatik oynat seç. Dinleme bitince **Oyuna başla** görünmeli; sınav puanı henüz oluşmamalı.
2. Doğa Dedektifi oyununda üç olayın bağlantısını seç. Yanlış cevapta ipucu, üçüncü denemede doğru bağlantının açıklaması gelmeli. İlgili sahneyi yeniden dinleyip aynı soruya dönebilmelisin.
3. **5 soruluk sınava başla** düğmesine dokun. Soruları ve seçenekleri Dinle düğmesi okur. Her gönderilen cevabın açıklaması gösterilir; cevap aynı denemede değiştirilemez. Her doğru cevap 20 puandır.
4. **Sonucumu gör** ile son puan, en iyi puan ve katılım rozeti görünmeli. Tekrar denemede önceki en iyi puan korunmalı. Sadece dinlemek bütün dersi bitirmiş sayılmamalı.
5. Sayfayı yenileyince oyun/sınav ilerlemesi korunmalı, ses kendiliğinden başlamamalı. Ana öğrenci yolu ve öğretmen hikâye kütüphanesi aynı sonucu göstermeli. Paylaşım ve gizlilik alanındaki kayıt silme işlemi oyun ve sınav kayıtlarını da temizlemeli.
