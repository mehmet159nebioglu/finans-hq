# İşlem / Tavsiye Log

Her satır bir tavsiye ya da sinyaldir. `finans-uzun-vade` ve `finans-kisa-vade` ajanları buraya yazar ve açık kayıtların durumunu günceller. Kısa vade kayıtlarında Tarih sütunu her zaman tam UTC tarih+saat:dakika içerir (format: `YYYY-MM-DD HH:MM UTC`), çünkü hedef/stop kontrolü dakika hassasiyetinde yapılıyor.

## Özet (kısa vade)

| Toplam | Hedefe Ulaştı | Stop Oldu | Açık | İsabet Oranı (kapanan işlemler) |
|---|---|---|---|---|
| 1 | 0 | 0 | 1 | henüz kapanan işlem yok |

*(Bu tablo her kısa vade kaydı kapandığında — hedefe ulaştı ya da stop oldu — güncellenir. Örneklem küçükken isabet oranı istatistiksel bir garanti sayılmamalı.)*

## Kayıtlar

| Tarih (UTC) | Tür | Enstrüman | Yön | Giriş | Hedef | Stop | Güven (1-10) | Durum |
|---|---|---|---|---|---|---|---|---|
| 2026-07-17 | uzun vade | Altın (XAU/USD) | Al (kademeli biriktirme) | ~3.975 USD/ons | 4.900 USD/ons (2026 yıl sonu banka ortalaması) | 3.850 USD/ons (ana destek altı kırılım) | 6 | açık |
| 2026-07-17 17:00 UTC | kısa vade | Altın (XAU/USD) | Al | 4014 USD/ons | 4044 USD/ons (~%0.75) | 4006 USD/ons (~%0.20, 01:30 15dk barı swing low altı) | 4 | açık (kontrol: 2026-07-17 17:00 UTC barı — giriş barının kendisi — high 4018.32, low 4014.62, close 4016.95; ne hedef ne stop tetiklendi, izlemeye devam) |
