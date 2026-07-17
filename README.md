# Finans İleri Aşama (Hedef 4)

İki ayrı çalışma modu var. İkisi de yalnızca **analiz, tavsiye ve bildirim** üretir — hiçbiri gerçek bir borsa/forex/kripto hesabına bağlı değildir ve otomatik emir girmez. Çıktılar kişisel bilgilendirme amaçlıdır, yatırım danışmanlığı değildir; nihai karar ve işlem her zaman kullanıcıya aittir.

## 1. Uzun vadeli analist — `finans-uzun-vade` subagent
Hisse senedi, ana kripto coinler, altın/gümüş gibi varlıklarda geçmiş fiyat hareketi, güncel haberler ve makroekonomik gidişat (küresel/ABD/Türkiye) üzerinden yatırım tavsiyesi üretir. **On-demand** çalışır — kullanıcı bir enstrüman sorduğunda veya "genel piyasayı tara" dediğinde devreye girer.

## 2. Kısa vadeli forex/altın robotu — `finans-kisa-vade` subagent
Genel olarak altın (XAU/USD) üzerinde, %0.5-1 hedefli ve dar stop'lu kısa vadeli işlem fırsatlarını değerlendirir. Hem on-demand sorulabilir hem de **15 dakikada bir** çalışan bir bulut rutini üzerinden arka planda tarama yapıp fırsat gördüğünde bildirim (`PushNotification`) atar.

## Veri kaynağı ve sınırlama
Fiyat, haber ve ekonomik veriler ücretsiz/genel kaynaklardan (WebSearch/WebFetch) toplanır — gerçek zamanlı bir broker beslemesi yoktur, birkaç dakika gecikme olabilir. Bu, özellikle kısa vadeli %0.5-1 hedefli sinyallerde önemli bir sınırlamadır ve kullanıcı bunu bilerek onayladı.

## Güven skoru
Her tavsiye/sinyal 1-10 arası bir güven skoru taşır.

## Kayıt / tutarlılık takibi
Her iki robot da tavsiyelerini `islem-log.md` dosyasına yazar. Kullanıcı "tutarlılığın nasıl" diye sorduğunda ilgili ajan bu logdan isabet oranını özetler.
