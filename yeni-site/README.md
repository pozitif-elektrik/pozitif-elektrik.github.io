# Pozitif Marin Elektrik: yeni site

Çok sayfalı statik site. Yalnızca Tailwind CSS 4 (`@tailwindcss/browser@4.3.5`, CDN) ve vanilla JS; bileşen kütüphanesi yok. Sitede form yok.

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
| `projeler.html` | 81 fotoğraflık filtreli galeri. Kategoriye doğrudan link verilebilir: `projeler.html?kategori=tekne-yazilari` |
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

## Görseller

Her görsel, kullanıldığı kutunun oranında kırpıldı.

- `assets/img/bolum/hero-*.jpg`: Ana sayfa hero görseli, ekran genişliğine göre `<picture>` ile seçiliyor.
  - mobil: 9:16
  - tablet: 4:3
  - dizüstü: 16:10
  - geniş ekran: 2.74:1
- `assets/img/sayfa/`: Sayfa başlıkları ve tekne tipi kartları, 4:3.
- `assets/img/urunler/`: Kenar boşlukları kırpılmış, beyaz kare zemine ortalanmış ürün görselleri, 640×640.
- `assets/img/galeri/`: Proje fotoğrafları (en fazla 1100px), `galeri/kucuk/` altında 480px kare küçük boyları.

## Yayın

Test yayını: https://pozitif-elektrik.github.io/ — `main` dalına gönderilen her değişiklik `.github/workflows/pages.yml` ile otomatik yayınlanır. İş akışı yalnızca yayınlanan kopyaya `noindex` etiketi ve kapalı `robots.txt` ekler; bu klasördeki dosyalar gerçek alan adına olduğu gibi taşınabilir.

`_headers` dosyası Cloudflare Pages/Netlify gibi barındırmalarda `noindex` başlığı içindir; gerçek alan adına geçerken silin.

## Bilinen eksikler

- **Fotoğraflar:** Proje fotoğraflarında eski filigran var.
- **Tailwind:** Canlıya almadan önce CDN yerine Tailwind CLI ile statik CSS'e geçmek performansı artırır.
