# Finans İleri Aşama (Hedef 4)

İki ayrı çalışma modu var. İkisi de yalnızca **analiz, tavsiye ve bildirim** üretir — hiçbiri gerçek bir borsa/forex/kripto hesabına bağlı değildir ve otomatik emir girmez. Çıktılar kişisel bilgilendirme amaçlıdır, yatırım danışmanlığı değildir; nihai karar ve işlem her zaman kullanıcıya aittir.

## 1. Uzun vadeli analist — `finans-uzun-vade` subagent
Hisse senedi, ana kripto coinler, altın/gümüş gibi varlıklarda geçmiş fiyat hareketi, güncel haberler ve makroekonomik gidişat (küresel/ABD/Türkiye) üzerinden yatırım tavsiyesi üretir. **On-demand** çalışır — kullanıcı bir enstrüman sorduğunda veya "genel piyasayı tara" dediğinde devreye girer.

## 2. Kısa vadeli forex/altın robotu — `finans-kisa-vade` (+ komite) sistemi
Genel olarak altın (XAU/USD) üzerinde, en az %0.3 hedefli (üst sınır yok) ve dar stop'lu kısa vadeli işlem fırsatlarını değerlendirir.

- **On-demand:** Kullanıcı doğrudan sorduğunda `finans-kisa-vade` subagent'ı tek başına, uçtan uca çalışır.
- **Zamanlanmış tarama (15 dakikada bir, yerel; saatlik, bulut):** `finans-kisa-vade` subagent'ı ARTIK bu modda çağrılmıyor — gecikmeyi (analiz 30-90dk sürüp piyasayı geride bırakma riski) azaltmak için üst seviye orkestratör (ana oturum) deterministik işleri (piyasa açık/kapalı testi, açık pozisyon/hedef-stop kontrolü, tek pozisyon kuralı, aritmetik doğrulama, volatilite hesabı, tazelik doğrulaması, sentez) doğrudan kendisi yapar; sadece açık pozisyon yokken iki dar kapsamlı alt-ajanı (`finans-kisa-vade-teknik`, `finans-kisa-vade-makro`) — makro en fazla saatte bir — paralel çağırır. Bildirimi de (`ntfy.sh`, çünkü `PushNotification` arka plan/bulut ortamlarında güvenilir çalışmıyor) orkestratör kendisi atar.

## Mimari (zamanlanmış kısa vade taraması)

Her 15dk'lık (yerel) / saatlik (bulut) tetiklemede:
1. Orkestratör güncel fiyatı çeker, nabız bildirimi atar, `islem-log.md`'yi okur.
2. Açık bir kısa vade pozisyonu varsa: orkestratör hedef/stop tetiklenmiş mi kendisi kontrol eder (deterministik, LLM yok), kapandıysa log'u günceller ve bildirim atar — **hiçbir alt-ajan çağrılmaz** (en büyük token/gecikme tasarrufu, pozisyonlar saatlerce açık kalabiliyor).
3. Açık pozisyon yoksa: `finans-kisa-vade-teknik` (rejim/mum/kovalama/giriş-hedef-stop önerisi) ve gerekirse `finans-kisa-vade-makro` (son makro değerlendirmenin üzerinden ~1 saatten fazla geçtiyse; geçmediyse önbellekten kullanılır) paralel çağrılır.
4. Orkestratör iki alt-skoru birleştirir (`güven = round((teknik+makro)/2)`), volatilite tavanını ve minimum eşiği (≥5) uygular, hedef yüzdesini kendisi hesaplayıp doğrular, log'a yazmadan hemen önce fiyatı tekrar çekip tazelik doğrulaması yapar.
5. Sinyal varsa log'a yazar ve bildirim atar; yoksa nabız yeterlidir, ek bildirim yok.

## Veri kaynağı ve sınırlama
Fiyat, haber ve ekonomik veriler ücretsiz/genel kaynaklardan (WebSearch/WebFetch) toplanır — gerçek zamanlı bir broker beslemesi yoktur, birkaç dakika gecikme olabilir. Bu, özellikle kısa vadeli (en az %0.3 hedefli) sinyallerde önemli bir sınırlamadır ve kullanıcı bunu bilerek onayladı.

## Güven skoru
Her tavsiye/sinyal 1-10 arası bir güven skoru taşır.

## Kayıt / tutarlılık takibi
Her iki robot da tavsiyelerini `islem-log.md` dosyasına yazar. Kullanıcı "tutarlılığın nasıl" diye sorduğunda ilgili ajan bu logdan isabet oranını özetler.
