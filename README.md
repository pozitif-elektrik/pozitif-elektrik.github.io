# Pozitif Marin Elektrik — web sitesi

Pozitif Marin Elektrik (Tuzla/İstanbul, yat ve tekne elektrik-elektronik sistemleri) için hazırlanan yeni web sitesi.

| Klasör | İçerik |
|---|---|
| `yeni-site/` | Yayına giden statik site (Tailwind CSS 4 + daisyUI 5 CDN, vanilla JS). Ayrıntılar: `yeni-site/README.md` |
| `kaynak/` | Sayfaları üreten `build.py` ve galeri/ürün verisi `veri.json` |
| `eski-site/` | Eski sitenin (pozitifelektrik.org) arşivi: ayna kopya, orijinal görseller, metinler, ekran görüntüleri |

## Düzenleme

HTML dosyaları elle düzenlenmez; `kaynak/build.py` değiştirilip proje kökünde çalıştırılır:

```sh
python3 kaynak/build.py
```

## Test yayını

https://pozitif-elektrik.github.io/

`main` dalına gönderilen her `yeni-site/` değişikliği GitHub Actions ile GitHub Pages'e yayınlanır
(`.github/workflows/pages.yml`). Test yayını arama motorlarına kapalıdır (noindex).
