# Pozitif Marin Elektrik: yeni site

Çok sayfalı statik site. Tailwind CSS 4 (`@tailwindcss/browser@4.3.5`, CDN) ve vanilla JS; bileşen kütüphanesi yok. Fotoğraf büyütme penceresi için PhotoSwipe 5.4.4 (MIT, CDN). Sitede form yok.

## Logo ve tema

- **Logo:** Öneri C (amblem + "POZİ✚İF / MARİN ELEKTRİK"). Üst menüde ve alt bilgide satır içi SVG olarak; kutucuk ve yazı rengi `currentColor` (açık temada lacivert, koyu temada beyaz), artı her iki temada kırmızı. Kaynağı `../kaynak/logo.py`, ayrıntılar `../logo/README.md`.
- **Favicon:** `favicon.ico` (16/32/48), `assets/img/favicon.svg`, `assets/img/apple-touch-icon.png` (180). Yapısal verideki logo: `assets/img/logo.png`.
- **Açık / koyu tema:** Üst menüdeki ay/güneş düğmesi. Ziyaretçi seçim yapana kadar cihazın ayarı izlenir; seçim `localStorage`'da (`tema`) saklanır ve açık sekmeler arasında eşitlenir. Tema `<html data-tema="acik|koyu">` ile belirlenir; `<head>` içindeki kısa betik bunu sayfa çizilmeden önce yapar (yanıp sönme olmaz).
- **Renkler:** `kaynak/build.py` içindeki `RENKLER` tablosu (açık, koyu). Tailwind'de `bg-zemin`, `bg-zemin-2`, `bg-yuzey`, `border-cizgi`, `text-metin`, `bg-koyu`, `bg-ters`, `bg-kirmizi`, `text-kirmizi-metin` gibi sınıflar olarak kullanılır; koyu temada değerleri kendiliğinden değişir, bu yüzden çoğu yerde `dark:` gerekmez. Düğmeler `dugme()` yardımcısıyla üretilir.

## Sayfalar

| Dosya | İçerik |
|---|---|
| `index.html` | Hero, rakamlar, kısa tanıtım, 6 hizmet, öne çıkan projeler, çalışma adımları, tekne yazıları, iş ortakları ve referanslar özeti |
| `hakkimizda.html` | Hikaye, ilkeler, çizimden teslimata altı adım, çalışılan tekne tipleri |
| `hizmetler.html` | 6 hizmetin her biri için açıklama, kapsam ve fotoğraflar. Üstte yapışkan alt menü |
| `projeler.html` | 81 fotoğraf, 6 kategori grubunda; fotoğraflar kırpılmadan, satırları iki kenara yaslanmış düzende. Üstte yapışkan kategori filtresi. Kategoriye doğrudan link verilebilir: `projeler.html?kategori=tekne-yazilari` |
| `urunler.html` | 17 ürün, 4 grupta |
| `is-ortaklarimiz.html` | Ürün markaları ve tersaneler |
| `referanslar.html` | 32 firma, 3 sektör grubunda |
| `iletisim.html` | Telefon, cep, e-posta, adres, harita, fatura bilgileri ve IBAN kopyalama |
| `404.html` | Bulunamayan sayfalar için hata sayfası |

## Düzenleme

HTML sayfaları `../kaynak/build.py` tarafından üretiliyor:

- Ortak üst menü, alt bilgi ve `<head>` kısmı bu dosyada tek yerde tanımlı.
- Galeri ve ürün listesi `../kaynak/veri.json` dosyasından geliyor.

Metin değiştirmek için `build.py` dosyasını düzenleyip şunu çalıştırın:

```bash
python3 kaynak/build.py      # proje kökünden
```

Logo değişirse önce `python3 kaynak/logo.py` (logo dosyalarını ve sitedeki favicon/logo dosyalarını yeniler), sonra `build.py`.

HTML dosyalarını doğrudan da düzenleyebilirsiniz, ama bir sonraki üretimde bu değişiklikler silinir.

## Fotoğraf galerisi

- **Büyütme penceresi:** `assets/js/galeri.js` (ES modülü) PhotoSwipe'ı jsDelivr'den yükler; ana sayfa, hizmetler ve projeler sayfalarında `[data-lightbox]` içindeki `<a data-pswp-width data-pswp-height>` bağlantıları açar. Kaydırarak gezinme, iki parmakla yakınlaştırma, aşağı kaydırıp kapatma, klavye; telefonda "geri" tuşu pencereyi kapatır. Kütüphane yüklenemezse bağlantı büyük fotoğrafı doğrudan açar.
- **Projeler düzeni:** kütüphanesiz, düz CSS. Her fotoğrafın `flex-grow` ve `flex-basis` değeri en-boy oranıyla (`--o`) orantılı olduğu için bir satırdaki fotoğraflar aynı yüksekliğe gelir (`--rh`: satır yüksekliği).
- **Fotoğraf boyutları:** `build.py` JPEG başlığından okur (Pillow gerekmez).

## Görseller

Her görsel, kullanıldığı kutunun oranında kırpıldı.

- `assets/img/bolum/hero-*.jpg`: Ana sayfa hero görseli, ekran genişliğine göre `<picture>` ile seçiliyor.
  - mobil: 9:16
  - tablet: 4:3
  - dizüstü: 16:10
  - geniş ekran: 2.74:1
- `assets/img/sayfa/`: Sayfa başlıkları ve tekne tipi kartları, 4:3.
- `assets/img/urunler/`: Kenar boşlukları kırpılmış, beyaz kare zemine ortalanmış ürün görselleri, 640×640.
- `assets/img/galeri/`: Proje fotoğrafları (en fazla 1100px).
  - `galeri/kucuk/`: 480px kare küçükler (ana sayfa, hizmetler).
  - `galeri/onizleme/`: oranı korunmuş önizlemeler, yükseklik en fazla 540px (projeler). Yeniden üretmek için `python3 kaynak/onizleme.py`.

## Yayın

Test yayını: https://pozitif-elektrik.github.io/ — `main` dalına gönderilen her değişiklik `.github/workflows/pages.yml` ile otomatik yayınlanır. İş akışı yalnızca yayınlanan kopyaya `noindex` etiketi ve kapalı `robots.txt` ekler; bu klasördeki dosyalar gerçek alan adına olduğu gibi taşınabilir.

`_headers` dosyası Cloudflare Pages/Netlify gibi barındırmalarda `noindex` başlığı içindir; gerçek alan adına geçerken silin.

## Bilinen eksikler

- **Fotoğraflar:** Proje fotoğraflarında eski filigran var.
- **Tailwind:** Canlıya almadan önce CDN yerine Tailwind CLI ile statik CSS'e geçmek performansı artırır.
