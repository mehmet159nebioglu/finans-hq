# İşlem / Tavsiye Log

Her satır bir tavsiye ya da sinyaldir. `finans-uzun-vade` ve `finans-kisa-vade` ajanları buraya yazar ve açık kayıtların durumunu günceller. Kısa vade kayıtlarında Tarih sütunu her zaman tam UTC tarih+saat:dakika içerir (format: `YYYY-MM-DD HH:MM UTC`), çünkü hedef/stop kontrolü dakika hassasiyetinde yapılıyor.

## Özet (kısa vade)

| Toplam | Hedefe Ulaştı | Stop Oldu | İptal | Açık | İsabet Oranı (kapanan işlemler) |
|---|---|---|---|---|---|
| 2 | 0 | 1 | 1 | 0 | 0/1 = %0 (iptal edilen kayıt hesaba dahil edilmez) |

*(Bu tablo her kısa vade kaydı kapandığında — hedefe ulaştı ya da stop oldu — güncellenir. İptal edilen kayıtlar Toplam'a dahildir ama Hedefe Ulaştı/Stop Oldu/İsabet Oranı hesabına katılmaz, çünkü fiyat o seviyelere gerçekte ulaşmamıştır. Örneklem küçükken isabet oranı istatistiksel bir garanti sayılmamalı.)*

## Kayıtlar

| Tarih (UTC) | Tür | Enstrüman | Yön | Giriş | Hedef | Stop | Güven (1-10) | Durum |
|---|---|---|---|---|---|---|---|---|
| 2026-07-17 | uzun vade | Altın (XAU/USD) | Al (kademeli biriktirme) | ~3.975 USD/ons | 4.900 USD/ons (2026 yıl sonu banka ortalaması) | 3.850 USD/ons (ana destek altı kırılım) | 6 | açık |
| 2026-07-17 17:00 UTC | kısa vade | Altın (XAU/USD) | Al | 4014 USD/ons | 4044 USD/ons (~%0.75) | 4006 USD/ons (~%0.20, 01:30 15dk barı swing low altı) | 4 | **stop oldu (kullanıcı kararıyla, 2026-07-17 18:45 UTC)** — teknik olarak stop (4006) henüz kırılmamıştı (18:45 UTC barı: O4008.43/H4008.43/L4007.37/C4007.46, en düşük 4007.37, stop'a sadece 1.37 kala), ama fiyat sürekli stop'a doğru gerilediği ve pozisyon zaten güven=4/10 ile zayıf açıldığı için kullanıcı bunu pratik olarak başarısız/stop kabul edip kapattı. İsabet oranı hesabına "stop oldu" olarak dahil edilir. |
| 2026-07-17 17:15 UTC | kısa vade | Altın (XAU/USD) | Sat | 4014 USD/ons | 3984 USD/ons (~%0.75) | 4023 USD/ons (~%0.22, 16:15 15dk barı swing high 4022.85 üstü) | 5 | **iptal (tek pozisyon kuralı — 2026-07-17 18:30 UTC'de değerlendirildi)**: Aynı anda açık iki zıt yönlü kısa vade kaydı (Al ve Sat) tespit edildi, kurallar gereği yalnızca biri açık kalabilir. 18:30 UTC itibarıyla piyasa durumu bu Sat kurulumu aleyhine: 4008.6 destek bölgesi (17:45/18:00/18:15 barlarında) üç kez test edilip kırılmadı — aşağı yönlü devam için gereken kırılım gerçekleşmedi. 17:45 barında görülen kırmızı gövde + uzun üst gölgeli "ters çekiç" formasyonu dip dönüşüne (yukarı yönlü) işaret ediyor, bu Sat tezini zayıflatıyor. 18:30 barında fiyat 4008'den 4013-4016 bandına toparlandı, giriş seviyesi 4014'e geri yaklaştı ve hedefe (3984) olan mesafe hâlâ tam kat edilmedi. Bu nedenle Al kaydı tercih edildi, bu Sat kaydı gerçekte hedefe (3984) veya stop'a (4023) ulaşmadan iptal edilmiştir — isabet oranı hesabına dahil edilmemelidir. |
