# Özel soru ve cevap kutusunu etkinleştirme

Şu anda bağlantı alanları boştur. Sitede arayüz vardır; soru gönderimi, cevap sorgulama ve eğitimci girişi devre dışıdır. Bunlar yerel bir formu başarılı gibi göstererek taklit edilmez.

1. Kurumun onayladığı Supabase projesinde `questions.sql` dosyasını SQL Editor ile çalıştır.
2. Supabase Authentication içinde yetkili eğitimci hesabı oluştur. Kopyalanan User UID için SQL Editor'da `insert into public.merak_qa_admins(user_id) values ('GERCEK-USER-UUID');` çalıştır. Her giriş yapan hesap yönetici olmaz; bu listede olmalıdır. Herkese açık kullanıcı kaydını kapat.
3. `assets/question-service.js` başındaki Project URL ve public publishable/anon key alanlarını doldur. Şifre, service_role veya secret key ön yüz dosyalarına yazılmaz.
4. Kurumun çocukların verilerine ilişkin süreçlerini, gerekli aydınlatmayı, saklama süresini, yetkilileri ve başvuru/itiraz kanallarını kesinleştir. Kullanım koşullarını gerçek hizmetle uyumlu güncelle. Veri silme/saklama operasyonu planlanmadan canlı öğrenci sorusu alma.
5. Soru spam koruması için canlı yayından önce kurumun seçtiği CAPTCHA/istek sınırı katmanını ekle. SQL'de günlük toplam 500 yeni soru sınırı bulunur; tek başına güçlü kötüye kullanım koruması değildir. Ücretsiz servis kotaları geçerlidir.
6. Ayrı tarayıcı profilleriyle öğrenci sorusu → takip kodu → eğitimci girişi → cevap → doğru kodla özel cevap akışını doğrula. Başka kodla, yanlış hesapla veya doğrudan tablo isteğiyle sorular listelenememelidir.

Takip kodu tarayıcıda kriptografik rastgele 32 bayttan üretilir; 64 onaltılık karakterdir. Sunucuda yalnızca SHA-256 özeti saklanır. Kod bir erişim anahtarıdır; öğrenci isterse kendi cihazında saklar. Kodu bilen kişi ilgili soruya/cevaba erişebilir. E-posta, telefon veya SMS bildirimi yoktur; öğrenci aynı sayfaya koduyla döner. Soru gövdesi ve özel cevap GitHub deposunda tutulmaz.

Eğitimci oturumu sekmenin sessionStorage alanında tutulur; gerçek yetki sunucudaki fonksiyonlarda kontrol edilir. Yetki kaldırmak için UID'yi `merak_qa_admins` tablosundan sil. Soru listesi son 200 kayıtla sınırlıdır; yüksek kullanımda sayfalama ve kurum içi yönetim ekranı eklenmelidir.
