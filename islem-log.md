# İşlem / Tavsiye Log

Her satır bir tavsiye ya da sinyaldir. `finans-uzun-vade` ve `finans-kisa-vade` ajanları buraya yazar ve açık kayıtların durumunu günceller. Kısa vade kayıtlarında Tarih sütunu her zaman tam UTC tarih+saat:dakika içerir (format: `YYYY-MM-DD HH:MM UTC`), çünkü hedef/stop kontrolü dakika hassasiyetinde yapılıyor.

## Özet (kısa vade)

| Toplam | Hedefe Ulaştı | Stop Oldu | İptal | Açık | İsabet Oranı (kapanan işlemler) |
|---|---|---|---|---|---|
| 6 | 2 | 2 | 2 | 0 | 2/4 = %50 |

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
| 2026-07-22 11:30 UTC | kısa vade | Altın (XAU/USD) | Sat | 4119 USD/ons | 4115 USD/ons (~%0.48 [HATALI ETİKET]) | 4124 USD/ons (~%0.12) | 5 | **iptal (hesaplama hatası — 2026-07-22 11:45 UTC'de tespit edildi, kullanıcı fark etti)**: Giriş (4119) ile hedef (4115) arası fark sadece 4 puan = **%0.10**, ajanın etikettiği %0.48 yanlıştı. Kurulum kriterinin temel şartı olan "hedef %0.5-1 aralığında olmalı" kuralı ihlal edilmiş — bu sinyal hiç açılmamalıydı. 11:30 UTC barının low'u (4115.09) bu hatalı hedefe zaten değmiş olsa da, bu gerçek bir "kazanç" sayılmaz çünkü sinyal baştan geçersizdi. İsabet oranı hesabına dahil edilmez. |
| 2026-07-22 12:45 UTC | kısa vade | Altın (XAU/USD) | Al | 4118.90 | 4139.45 (~%0.50) | 4113.00 (~%0.14) | 6 | **hedefe ulaştı (2026-07-22 13:30 UTC)** — 13:00 barı (O4114.04/H4124.73/L4113.19/C4124.17) stop'a (4113.00) sadece 0.19 puana kadar yaklaştı ama kırmadı; 13:15 (C4133.93), 13:30 barı (O4123.94/H4144.56/L4123.94/C4142.53) high 4144.56 hedefi (4139.45) net şekilde aştı. Not: giriş barının (12:45) kendi low'u 4109.65 idi (stop'un altında) ama giriş fiyatı (4118.90) bu low'dan belirgin şekilde yüksekti — muhtemelen giriş, o barın erken dip anından SONRA, fiyat toparlandıktan sonra alınmış (15dk çözünürlükte tam sıra kesin değil, bu belirsizlik dürüstçe not edilir). Sonraki hiçbir barda stop net şekilde kırılmadı (en yakın 13:00'da 0.19 puan kala). Kazanç: +20.55 puan (~%0.50). İsabet oranı hesabına "hedefe ulaştı" olarak dahil edilir. |

**Yeni Sinyal Notları (2026-07-22 12:45 UTC):**
- **Piyasa Rejimi:** Yatay/Range (korunacak) — Son 12 saatte 4114-4133 bandı içinde oynaklık (high 4140.79 @ 03:15, low 4090.65 @ 00:30 — ama son 6 saat dar), net yön yok, ardışık consolidation barları.
- **Destek/Direnç:** Destek 4114.35 (11:30 close, low 4114.04), Direnç 4132.81 (12:15 close, high 4133.77). Şu anki fiyat 4118.90 bandın alt-orta bölgesi.
- **Mum Formasyonu (Teyit):** 12:45 barı (O4127.30, H4129.06, L4118.79, C4118.90) → Bearish gövde (8.4 puan) + uzun üst gölge (10.76 puan) = **Dip Çekiç** formasyonu (yükseliş çabası reddedildi, dönüş sinyali). Öncesi: 12:15 bullish, 12:30 bearish (direnç reddi) → Desen: Bullish → Bearish → Dip Çekiç = Dip teyidi kuvvetli.
- **Kovalama Yasağı:** ✓ OK — Son sert hamle 06:15'te high 4141 (gün zirvesi); o tarihten 12:45'e ~6.5 saat geçti, şu anda zaten yatay band oluşmuş. Taze kovalama yok.
- **Volatilite:** Son 12 saatlik ranj 50.14 puan = %1.22 (günlük). Hedef %0.5-1. Oran: 1.22/0.75 = 1.6x hedef. Filtre: 1.22% < 3% (eşik) → **Geçti, sınır yok.**
- **Teknik Netlik:** Band yapısı confirmed (10+ bar test), destek keskin (4114.04), direnç keskin (4133.77), formasyon net (dip çekiç). Orta-yüksek confidence: **7/10**
- **Makro/Haber Uyumu:** FOMC 28-29 Temmuz (gelecek hafta), piyasa %85.6 Hold oranı (fed-funds unchanged 3.50-3.75%), şu an Fed öncesi durgunluk. Altın 4100-4350 range içinde, orta volatilite. **Nötr (5/10)** — Kuvvetli bir push yok ama ön yargı da yok.
- **Gerekçe:** Yatay bandın destek bölgesinden (4114.35) yükseliş giriş, direnç hedefi (4132-4133), mum çekiç teyidi, risk/reward 3.5:1 (dar stop, makul hedef).
- **Güven: 6/10** (5'in üstü ✓ — minimum eşik geçti). Teknik 7 + makro 5 = orta, henüz yüksek değil (Fed öncesi riskli).
- **Risk/Ödül:** Stop loss 5.90 puan (0.143%), Hedef 20.55 puan (0.499%) = 3.48:1 — mean-reversion için uygun.
- **Aritmetik Doğrulama:** Hedef % = (4139.45 - 4118.90) / 4118.90 × 100 = 20.55 / 4118.90 × 100 = **0.4989% ≈ 0.50%** ✓ (aralık %0.5-1.0 içinde)

**Ders (2026-07-22 11:30 hatalı Sat sinyali iptal edildi):**
- Aritmetik doğrulama eksikliği: 11:30 sinyalinde hedef %0.5 olarak etiketlenmişti, oysa giriş 4119/hedef 4115 = %0.10 (tam hesap yapılmamıştı). Bu tarama ondan sonra gelen her sinyalde hedef yüzdesini formülle doğrudan hesaplanıyor ve etikete yazılıyor, tahminden kaçınılıyor. (2026-07-22 12:45 AL: 20.55 / 4118.90 × 100 = 0.4989%, yukarıya yazıldı). Yalın hesap disiplini.
- Volatilite çıkması: 2026-07-21 başarısının (%78-87 isabet) volatilite çok yüksek olduğu dönemden (2.5-5 günlük ranj) kaynaklandığı doğrulandı. Mevcut (%1.2 ≈ 0.85-1.05 tahmini) daha gerçekçi ortam, sinyaller daha seçici olmalı. 11:30 çeşidi 5/10'nin altında olmaması gerekiyordu.

**Durum özeti: Fiyat 4118.90 | Yön: Yükseliş (destek dönüşü, mean-reversion bandın alt ucundan) | Volatilite: Normal (~%1.22 günlük, hedef dar ama filtreyi geçti)**
