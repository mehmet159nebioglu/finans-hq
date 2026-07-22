# İşlem / Tavsiye Log

Her satır bir tavsiye ya da sinyaldir. `finans-uzun-vade` ve `finans-kisa-vade` ajanları buraya yazar ve açık kayıtların durumunu günceller. Kısa vade kayıtlarında Tarih sütunu her zaman tam UTC tarih+saat:dakika içerir (format: `YYYY-MM-DD HH:MM UTC`), çünkü hedef/stop kontrolü dakika hassasiyetinde yapılıyor.

## Özet (kısa vade)

| Toplam | Hedefe Ulaştı | Stop Oldu | İptal | Açık | İsabet Oranı (kapanan işlemler) |
|---|---|---|---|---|---|
| 4 | 1 | 2 | 1 | 0 | 1/3 = %33 (iptal edilen kayıt hesaba dahil edilmez) |

*(Bu tablo her kısa vade kaydı kapandığında — hedefe ulaştı ya da stop oldu — güncellenir. İptal edilen kayıtlar Toplam'a dahildir ama Hedefe Ulaştı/Stop Oldu/İsabet Oranı hesabına katılmaz, çünkü fiyat o seviyelere gerçekte ulaşmamıştır. Örneklem küçükken isabet oranı istatistiksel bir garanti sayılmamalı.)*

## Özet (simülasyon — geriye dönük, hindsight'sız)

**Bu, yukarıdaki gerçek işlem oranından AYRI bir ölçüttür.** Sistemin gerçek zamanlı çalışmadığı dönemlerde (teknik kesinti/tasarım hatası nedeniyle), "eğer o an çalışıyor olsaydı ne yapardı" diye adım adım (ileriye bakmadan, sadece o ana kadarki barlarla karar vererek) simüle edilen sanal işlemlerin toplamıdır. Gerçek para/gerçek kayıt değildir, sadece stratejinin tutarlılığını ek olarak test etmek için tutulur.

| Toplam | Hedefe Ulaştı | Stop Oldu | İsabet Oranı |
|---|---|---|---|
| 4 | 3 | 1 | 3/4 = %75 |

Simüle edilen işlemler:
| Tarih/Saat (UTC) | Yön | Giriş | Hedef | Stop | Güven | Sonuç | Kaynak simülasyon |
|---|---|---|---|---|---|---|---|
| 2026-07-20 23:00 | Al | 4003.34 | 4033.34 | 3997.34 | 6/10 | Hedefe ulaştı (01:15) | 18.5 saatlik boşluk simülasyonu |
| 2026-07-21 02:30 | Al | 4037.02 | 4067.02 | 4031.02 | 5/10 | Hedefe ulaştı (05:45) | 18.5 saatlik boşluk simülasyonu |
| 2026-07-22 03:45 | Sat | 4131.36 | 4126.29 | 4140.79 | 6/10 | Hedefe ulaştı (04:00) | 10 saatlik boşluk simülasyonu |
| 2026-07-22 08:15 | Al | 4116.97 | 4123.22 | 4114.04 | 6/10 | Stop oldu (09:45) | 10 saatlik boşluk simülasyonu |

## Kayıtlar

| Tarih (UTC) | Tür | Enstrüman | Yön | Giriş | Hedef | Stop | Güven (1-10) | Durum |
|---|---|---|---|---|---|---|---|---|
| 2026-07-17 | uzun vade | Altın (XAU/USD) | Al (kademeli biriktirme) | ~3.975 USD/ons | 4.900 USD/ons (2026 yıl sonu banka ortalaması) | 3.850 USD/ons (ana destek altı kırılım) | 6 | açık |
| 2026-07-17 17:00 UTC | kısa vade | Altın (XAU/USD) | Al | 4014 USD/ons | 4044 USD/ons (~%0.75) | 4006 USD/ons (~%0.20, 01:30 15dk barı swing low altı) | 4 | **stop oldu (kullanıcı kararıyla, 2026-07-17 18:45 UTC)** — teknik olarak stop (4006) henüz kırılmamıştı (18:45 UTC barı: O4008.43/H4008.43/L4007.37/C4007.46, en düşük 4007.37, stop'a sadece 1.37 kala), ama fiyat sürekli stop'a doğru gerilediği ve pozisyon zaten güven=4/10 ile zayıf açıldığı için kullanıcı bunu pratik olarak başarısız/stop kabul edip kapattı. İsabet oranı hesabına "stop oldu" olarak dahil edilir. |
| 2026-07-17 17:15 UTC | kısa vade | Altın (XAU/USD) | Sat | 4014 USD/ons | 3984 USD/ons (~%0.75) | 4023 USD/ons (~%0.22, 16:15 15dk barı swing high 4022.85 üstü) | 5 | **iptal (tek pozisyon kuralı — 2026-07-17 18:30 UTC'de değerlendirildi)**: Aynı anda açık iki zıt yönlü kısa vade kaydı (Al ve Sat) tespit edildi, kurallar gereği yalnızca biri açık kalabilir. 18:30 UTC itibarıyla piyasa durumu bu Sat kurulumu aleyhine: 4008.6 destek bölgesi (17:45/18:00/18:15 barlarında) üç kez test edilip kırılmadı — aşağı yönlü devam için gereken kırılım gerçekleşmedi. 17:45 barında görülen kırmızı gövde + uzun üst gölgeli "ters çekiç" formasyonu dip dönüşüne (yukarı yönlü) işaret ediyor, bu Sat tezini zayıflatıyor. 18:30 barında fiyat 4008'den 4013-4016 bandına toparlandı, giriş seviyesi 4014'e geri yaklaştı ve hedefe (3984) olan mesafe hâlâ tam kat edilmedi. Bu nedenle Al kaydı tercih edildi, bu Sat kaydı gerçekte hedefe (3984) veya stop'a (4023) ulaşmadan iptal edilmiştir — isabet oranı hesabına dahil edilmemelidir. |
| 2026-07-20 01:00 UTC | kısa vade | Altın (XAU/USD) | Al | 4008 USD/ons | 4025 USD/ons (~%0.42, revize) | 4002 USD/ons (~%0.15, revize) | 7 | **stop oldu (2026-07-20 22:45 UTC)** — 1 kez revize edilmiş kayıt (bkz. 18:45 UTC revizyon notu). 22:45 UTC barı: O4004.20/H4005.13/L3999.74/C4001.40 — düşük 3999.74, revize stop (4002) net şekilde kırıldı (18:45'ten 22:30'a kadarki tüm barlarda stop hiç kırılmamıştı, ilk kırılım bu barda oldu). Not: 23:00 UTC barında fiyat 4009'a toparlandı ama stop zaten bu toparlanmadan önce tetiklenmiş sayılır — gerçek işlemde emir burada kapanırdı. İsabet oranı hesabına "stop oldu" olarak dahil edilir. |
| 2026-07-21 18:15 UTC | kısa vade | Altın (XAU/USD) | Al | 4085.29 USD/ons | 4105.50 USD/ons (~%0.5) | 4066.00 USD/ons (~%0.47, 16:00-17:30 pullback dibinin altı) | 7 | **hedefe ulaştı (2026-07-22 01:00 UTC)** — 01:00 UTC barı: O4095.64/H4119.45/L4095.64/C4118.69, high 4119.45 hedefi (4105.50) net şekilde aştı (muhtemelen haber odaklı ani sıçrama, bar içinde +24 puan). Stop (4066) girişten kapanışa kadar hiçbir barda test edilmedi (en düşük low 4075.31 @ 22:00 UTC). Kazanç: +20.21 puan (~%0.49), açık kalma süresi ~6.75 saat. Önceki tarama bağlantı kesintisi yüzünden yarım kalmıştı, üst seviye tarafından kurtarılıp doğru şekilde kapatıldı. İsabet oranı hesabına "hedefe ulaştı" olarak dahil edilir — ilk gerçek kazanan işlemimiz. |

**Yeni Sinyal Notları (2026-07-20 01:00 UTC):**
- **Formasyon:** Ters çekiç dip (2026-07-20 00:00 barı: L=3983.42 uzun alt gölgesi, C=3996.72 yüksek kapanış) + yeşil bar teyidi (00:15 barı C=4004.67 güçlü toparlanma, 01:00 barı C=4007.88 devam).
- **Piyasa Rejimi:** Trend rejimi — düşüş (4010→3983) + dip + yükseliş başlangıcı. Konsolidasyon teyidi var (00:30-00:45 barları ~4001 bölgesinde).
- **Kovalama Yasağı:** Sert hamle sonrası konsolidasyon teyidi mevcuttur, kabul edilebilir.
- **Volatilite:** Günlük ranj tahmini %1-1.5 (3 saat verisi), hedefin (%1) 3 katından az — sınırlama yok.
- **Haber/Makro:** Jeopolitik risk (Orta Doğu gerginliği) altını destekliyor; Fed nötr (enflasyon düşüş, faiz muhtemelen sabit).
- **Risk/Ödül:** 13:40 puan fark (1:3+ uygun).

**Revizyon Sonrası (2026-07-20 18:45 UTC):**
- **Sebep:** Volatilite %1-1.5'den %0.39'a düştü, piyasa yatay hale geldi, orijinal hedef çok uzak kaldı. Stop riski arttı (3995, 18:00'da 4002.12'ye indi).
- **Yeni Hedef:** 4025 USD/ons (%0.42) — gerçekçi ve yakın, güncel volatiliteye uygun.
- **Yeni Stop:** 4002 USD/ons (%0.15) — teknik destek ve risk koruma.
