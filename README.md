# Petek Ustası 🐝

Arılarla renkli petekleri dıştan içe toplayıp resmi tamamladığın bir bulmaca oyunu (hibrit-casual, mobil öncelikli).
*A hexagon colour puzzle: send swarms of bees to collect a picture from the outside in.*

**Oyna / Play:** https://mehmetustattsc.github.io/puzzle-game/
(Telefonda "Ana ekrana ekle" ile uygulama gibi kurulur, internetsiz de çalışır.)

## Durum
Web prototipi, test aşaması. Sonraki adımlar: oyuncu testleri ve D1/D7 ölçümü → Android (Capacitor) + AdMob + Google Play Billing → Impressum / gizlilik → soft launch.

## Özellikler
- 450+ resim: 80 çizilmiş tasarım + 373 Fluent Emoji resmi (hayvanlar, çiçekler, yiyecekler, taşıtlar…), 21 albüm
- Prosedürel bölüm üretici: her bölüm sanal oyuncularla test edilir (akıllı oyuncu kazanmalı; dikkatsiz oyuncu ve soldan sağa sırayla basan oyuncu kaybetmeli)
- Mekanikler: bağlı sürüler, mühürlü petekler, anahtar ve kilit, merkez tuzağı, renk kutusu, kepenkli kapı, sürpriz tüp, benzer tonlar ve gürültü
- Bal ekonomisi, güçlendiriciler, can sistemi, günlük ödül takvimi, rozetler, dükkan (test modu)
- Türkçe, İngilizce, Almanca; sentezlenmiş ses efektleri ve müzik
- İlerleme cihazda saklanır; kayıt koduyla başka cihaza taşınır

## Proje yapısı
| Yol | İçerik |
|---|---|
| `index.html` | Oyunun tamamı (tek dosya: HTML, CSS, JS, resim verisi) |
| `manifest.webmanifest`, `sw.js`, `icons/` | Ana ekrana ekleme ve çevrimdışı çalışma |
| `tests/` | Bölüm üretici testleri ve tarayıcı duman testi |
| `tools/emoji/` | Emoji → petek resmi dönüştürme hattı |
| `.github/workflows/ci.yml` | Her gönderimde testler, geçerse GitHub Pages'e yayın |

## Geliştirme
```bash
npm install
npx playwright install chromium
npm test             # bölüm üretici kontrolleri
npm run test:smoke   # tarayıcıda menüler + 1. bölüm + kayıt
npm run serve        # http://localhost:8080
```
Bölüm üreticisi değiştiğinde `index.html` içindeki `LV_VER` artırılmalı (cihazlardaki hazır bölümler yenilenir).

## Ölçüm (isteğe bağlı)
Çerezsiz [GoatCounter](https://www.goatcounter.com) desteği hazır: hesap açıp kodu `index.html` içindeki `GC_CODE` alanına yaz.
Olaylar: açılış günü (D0, D1, D2-3, D4-7…), bölüm başlangıç/kazanma/kaybetme/bırakma, dükkan açılışı ve satın alma dokunuşları.

## Geri bildirim
Hata ve test geri bildirimi için **Issues → New issue** altındaki formları kullan.

## Lisanslar
Kod © Mehmet. Üçüncü taraf içerik için bkz. [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
