'use strict';
// Original practice items, matched to the existing seven-scene story. Teacher review draft.
window.MERAK_LESSON_ACTIVITIES = {
  version: '2026-10-27-pilot-1',
  lessons: {
    'g5-1-1': {
      id: 'g5-1-1', productionId: 'gozlem-kulubu', storyId: 'g5-1-1-ornek-1', grade: '5',
      title: 'Evrendeki Mükemmel Düzen', gameTitle: 'Doğa Dedektifi', badge: 'Doğa Gözlemcisi', reviewed: false,
      goal: 'Doğadaki olaylar arasında ilişki kurarak evrendeki düzen üzerine akıl yürütmek.',
      curriculum: { program: 'Türkiye Yüzyılı Maarif Modeli', code: 'DKAB.5.1.1', text: 'Evrendeki mükemmel düzene ilişkin akıl yürütebilme', evidence: 'DÖGM, Dijital İçeriklerin Türkiye Yüzyılı Maarif Modeli Çerçevesinde Öğrenme Çıktılarıyla İlişkisi, PDF s. 72.', book: '5. sınıf Din Kültürü ve Ahlak Bilgisi, 2026, ünite 1; s. 12 ve konu başlangıcı s. 14.' },
      sceneIds: Array.from({length:7},(_,i)=>'gozlem-kulubu-'+String(i+1).padStart(2,'0')),
      intro: 'Doğa dedektifi ol! Üç olayın doğru bağlantısını bul. Ardından beş soruyla öğrendiklerini dene. İstersen soruları ve seçenekleri dinleyebilirsin.',
      quizIntro: 'Üç bağlantıyı inceledin. Şimdi beş soru var. Her soruda bir cevap seç ve cevabını kontrol et. Her doğru cevap yirmi puan. Açıklamayı dinleyebilir, ilgili sahneye dönebilirsin.',
      game: [
        { id:'isik', title:'Güneş ışığının izinde', image:'assets/scenes/gozlem-kulubu/02.png', scene:1,
          prompt:'Karttaki olay: Bitkiye ulaşan güneş ışığı. Bu olayla hangi bağlantıyı kurarsın?',
          options:['Arı, çiçekler arasında polen taşıyabilir.','Bitki, besin üretirken ışık enerjisinden yararlanır.','Yağış, toprağa su ulaştırabilir.'], answer:1,
          explanation:'Bitkiler, besin üretirken ışık enerjisinden yararlanır. Bu, güneş ile bitki arasındaki bağlantılardan biridir.',
          hint:'Bu seçenek başka bir doğa olayını anlatıyor. Işığın bitki için ne işe yaradığını düşün.' },
        { id:'ari', title:'Çiçeğin küçük ziyaretçisi', image:'assets/scenes/gozlem-kulubu/03.png', scene:2,
          prompt:'Karttaki olay: Bir arının çiçekten çiçeğe uçması. Bu olayla hangi bağlantıyı kurarsın?',
          options:['Yağış, toprağa su ulaştırabilir.','Bitki, besin üretirken ışık enerjisinden yararlanır.','Arı, nektar toplarken çiçekler arasında polen taşıyabilir.'], answer:2,
          explanation:'Arı, nektar toplarken çiçekler arasında polen taşıyabilir. Böylece bazı bitkilerin çoğalmasına katkı sağlar.',
          hint:'Bu seçenek başka bir doğa olayını anlatıyor. Arının çiçekler arasında ne taşıyabildiğini hatırla.' },
        { id:'yagmur', title:'Yağmurdan sonra', image:'assets/scenes/gozlem-kulubu/05.png', scene:4,
          prompt:'Karttaki olay: Bahçeye yağan yağmur. Bu olayla hangi bağlantıyı kurarsın?',
          options:['Yağış, toprağa su ulaştırır; bitkiler bu sudan yararlanabilir.','Arı, nektar toplarken çiçekler arasında polen taşıyabilir.','Bitki, besin üretirken ışık enerjisinden yararlanır.'], answer:0,
          explanation:'Yağmur, toprağa su ulaştırır. Bitkiler kökleriyle topraktaki sudan yararlanabilir. Bu olaylar birbiriyle ilişkilidir.',
          hint:'Bu seçenek başka bir doğa olayını anlatıyor. Yağmurun toprağa ne ulaştırdığını düşün.' }
      ],
      quiz: [
        { id:'gozlem', prompt:'Bir bitkinin yağmurla ilişkisini araştırmak isteyen Zehra, hangisini yaparsa gözleme dayalı bilgi toplar?', scene:4,
          options:['Bitkiyi incelemeden nasıl büyüdüğüne karar verir.','Yağmurdan önce ve sonra aynı bitkiyi inceleyip not alır.','İlk duyduğu açıklamayı araştırmadan doğru kabul eder.','Yalnız saksının rengine bakıp büyümeyi açıklamaya çalışır.'], answer:1,
          explanation:'Aynı bitkiyi farklı zamanlarda incelemek ve not almak, gözleme dayalı bilgi toplamaya yardımcı olur. Bir sonuca ulaşmadan önce gözlem ve karşılaştırma yaparız.' },
        { id:'iliskiler', prompt:'Ömer, arıların nektar toplarken polen taşıyabildiğini öğreniyor. Bu gözlem hangi düşünceyi destekler?', scene:2,
          options:['Bitkiler büyümek için yalnız arılara ihtiyaç duyar.','Arılar, çiçeklerin bütün ihtiyaçlarını tek başına karşılar.','Çiçekler ile onları ziyaret eden arılar birbirinden bağımsızdır.','Canlılar arasında birbirini etkileyen ilişkiler bulunabilir.'], answer:3,
          explanation:'Arı ile çiçek arasındaki ilişki, canlıların birbirini etkileyebildiğine bir örnektir. Bu, bitkinin su ve ışık gibi başka ihtiyaçları olmadığı anlamına gelmez.' },
        { id:'neden-sonuc', prompt:'Hikâyede yağmurun bitkilere katkısı hangi sırayla açıklanıyor?', scene:4,
          options:['Yağmur yağar; toprağa su ulaşır; bitki sudan yararlanır.','Bitki büyür; yağmuru oluşturur; toprağın suyu biter.','Yağmur yağar; topraktaki su biter; bitki susuz büyür.','Toprak kurur; yağmur durur; bitki suya ihtiyaç duymaz.'], answer:0,
          explanation:'Hikâyede yağmurun toprağa su ulaştırdığı ve bitkilerin bu sudan yararlandığı anlatılıyor. Olayların hangi sırayla birbirine bağlandığına dikkat ederiz.' },
        { id:'tefekkur', prompt:'Hikâyedeki öğretmene göre İslam, doğadaki düzen karşısında hangi davranışı teşvik eder?', scene:5,
          options:['Doğa hakkında soru sormadan ilk açıklamayla yetinmeyi.','Çevremizdeki olayları incelemeyi yalnız başkalarına bırakmayı.','Düzeni dikkatle gözlemleyip Allah’ın yaratışı üzerine düşünmeyi.','Gözlem yapmak yerine yalnız gördüklerimizin adlarını ezberlemeyi.'], answer:2,
          explanation:'Öğretmen, İslam’ın evrendeki düzen üzerine düşünmeyi teşvik ettiğini anlatıyor. Dikkatli gözlem ve düşünme, hikâyemizin birlikte ele aldığı iki adımdır.' },
        { id:'ozen', prompt:'Doğadaki canlılar arasındaki bağlantıları fark eden Ömer, gözlem yaparken nasıl davranmalı?', scene:6,
          options:['Bitkileri tanımak için bahçedeki çiçekleri koparmalı.','Canlıları rahatsız etmeden gözlemleyip bahçeyi korumalı.','Arıları daha yakından görmek için yuvalarını bozmalı.','Gözlem alanı açmak için küçük bitkileri söküp atmalı.'], answer:1,
          explanation:'Doğayı gözlemlerken canlıları rahatsız etmemek ve yaşam alanlarını korumak gerekir. Öğrendiklerimizi özenli davranışlara dönüştürebiliriz.' }
      ]
    }
  }
};
