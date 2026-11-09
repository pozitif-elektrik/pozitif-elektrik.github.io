# Pozitif Marin Elektrik — logo dosyaları

Sunum: `sunum.html` (tarayıcıda açın).

**Seçilen: C (amblem + yatay logo).** Sitede kullanılıyor: üst menü ve alt bilgide satır içi SVG,
favicon ve dokunmatik simge (bkz. aşağıda "Web sitesi").

## Öneriler

| Dosya adı | Öneri |
|---|---|
| `pozitif-a-restorasyon-*` | **A.** Eski logonun (2014, 150×70 JPG) temizlenmiş birebir vektörü. Siyah kutucuklar, daktilo tipi ayaklı harfler, noktasız I (eski logodaki gibi). |
| `pozitif-b-yenilenmis-*` | **B.** Aynı yerleşim; lacivert kutucuklar, gravür tipi tek çizgi harfler, Türkçe noktalı İ, yuvarlak uçlu artı. |
| `pozitif-c-amblem-*` | **C.** Sembol: dört kutucuğu bölen kırmızı artı. Favicon, sosyal medya profili, etiket. |
| `pozitif-c-yatay-*` | **C.** Amblem + "POZİ✚İF" + "MARİN ELEKTRİK". Site başlığı, antetli kağıt, kartvizit. |
| `favicon.svg` | Beyaz yuvarlak zeminde amblem (tarayıcı sekmesi, telefon ana ekranı). |

Her öneri dört renk sürümüyle: `renkli` (açık zemin), `negatif` (koyu zemin),
`siyah` ve `beyaz` (tek renk; harfler kutucuktan oyulmuştur).

## Biçimler

- `svg/` — ana dosyalar; web ve düzenleme için.
- `pdf/` — baskı, tabela, araç giydirme; vektör (resim içermez).
- `png/` — şeffaf zemin; logolar 2400 px, amblem 1024 px; favicon 32/180/512 px.

Bütün harfler dolgulu şekildir (anahatta dönüştürülmüş): dosyalarda yazı tipi,
çizgi ya da maske yoktur; doğrudan folyo kesim ve lazer gravüre verilebilir.

## Renkler

| Ad | HEX | RGB |
|---|---|---|
| Pozitif Kırmızı | `#E30613` | 227 6 19 |
| Gece Laciverti (B, C) | `#0F172A` | 15 23 42 |
| Pano Siyahı (A, tek renk) | `#111111` | 17 17 17 |

Baskı için CMYK/Pantone karşılığı matbaa provasıyla kesinleştirilmeli.

## Web sitesi

`kaynak/logo.py` her çalıştığında sitenin logo dosyalarını da yeniler:

- `kaynak/logo-site.svg`, `kaynak/amblem-site.svg`: `build.py` bunları sayfalara gömer. Renk
  `currentColor` (temaya göre lacivert/beyaz), artı kırmızı. Harfler burada dolgulu anahat yerine
  aynı iskeletin çizgisi olarak durur: ekranda piksel piksel aynı, dosya 60 KB yerine 3 KB.
- `yeni-site/favicon.ico`, `yeni-site/assets/img/favicon.svg`, `apple-touch-icon.png`, `logo.png`.

## Yeniden üretme

Dosyalar `kaynak/logo.py` ile üretilir (proje kökünde `python3 kaynak/logo.py`;
`rsvg-convert` ve Pillow gerekir). Harfler bir yazı tipinden alınmadı, bu çalışma
için çizildi; yazı tipi lisansı gerekmez. Harf iskeleti değiştirilirse dolgulu
şekiller kendiliğinden yeniden hesaplanır (`kaynak/logo-anahat.json`).
