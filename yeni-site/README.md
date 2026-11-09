# Pozitif Marin Elektrik: yeni site

Çok sayfalı statik site. Tailwind CSS 4 (`@tailwindcss/browser@4.3.5`) ve daisyUI 5 (`daisyui@5.7.50`) CDN'den yükleniyor, davranışlar vanilla JS ile yazıldı. Sitede form yok.

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

`_headers` dosyası önizleme adresinde `noindex` gönderiyor. **Gerçek alan adına geçerken bu dosyayı silin.**

Cloudflare Pages'e yüklemek için bu klasörü zipleyin (README hariç) ve Pages projesinde "Create deployment" ile yükleyin.

## Bilinen eksikler

- **Logo:** Sadece 150×70 JPG var, vektör logo bekleniyor.
- **Fotoğraflar:** Proje fotoğraflarında eski filigran var.
- **Tailwind:** Canlıya almadan önce CDN yerine Tailwind CLI ile statik CSS'e geçmek performansı artırır.
