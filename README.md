# Pozitif Marin Elektrik — web sitesi

Pozitif Marin Elektrik (Tuzla/İstanbul, yat ve tekne elektrik-elektronik sistemleri) için hazırlanan yeni web sitesi.

| Klasör | İçerik |
|---|---|
| `yeni-site/` | Yayına giden statik site (Tailwind CSS 4 CDN + vanilla JS, açık/koyu tema). Ayrıntılar: `yeni-site/README.md` |
| `kaynak/` | Sayfaları üreten `build.py`, galeri/ürün verisi `veri.json`, logoları üreten `logo.py` |
| `logo/` | Vektörel logo çalışması (3 öneri; sitede C kullanılıyor): SVG, PDF, PNG ve `sunum.html` |
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
