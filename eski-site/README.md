# Pozitif Marin Elektrik: eski site arşivi

Kaynak: http://pozitifelektrik.org/
İndirilme tarihi: 9 Kasım 2026
Amaç: yeni site tasarımı için referans

## Klasörler

| Klasör | İçerik |
|---|---|
| `site/` | Sitenin çevrimdışı açılabilen tam kopyası (wget mirror). HTML, CSS, JS, fontlar ve tüm görseller. |
| `site/pozitifelektrik.org/wp-content/uploads/2014/03/` | Sunucudaki medya klasörünün tamamı: 860 dosya (112 orijinal ve WordPress'in ürettiği küçük boyutlar). |
| `site/pozitifelektrik.org/portfolio/` | 98 ürün/proje öğesinin açılır pencere (modal) içerikleri. |
| `medya/orijinaller/` | Sadece tam boyutlu orijinal görseller (112 adet, 96 MB). **Yeni sitede bunları kullanın.** |
| `icerik/sayfalar/*.md` | Her sayfanın metni ve kullandığı görsellerin listesi. |
| `icerik/portfolyo.md` / `.json` | 98 ürün/proje öğesi: kategori, başlık ve orijinal görsel eşleşmesi. |
| `icerik/json/` | WordPress REST API'den alınan ham veriler (sayfalar, yazılar, medya, site bilgisi). |
| `ekran-goruntuleri/` | Canlı sitenin tam sayfa ekran görüntüleri: masaüstü (1440px) ve mobil (390px), 6 sayfa. |
| `wget-*.log` | İndirme kayıtları. |

`*.orig` dosyaları, wget bağlantıları yerel dosyalara çevirmeden önceki sunucu HTML'leridir.

### Yerel kopyayı açmak

```bash
cd site/pozitifelektrik.org && python3 -m http.server 8000
# Tarayıcıda: http://localhost:8000/
```

`index.html` dosyasını doğrudan çift tıklayarak da açabilirsiniz. Ancak Google Haritalar, Facebook ve iletişim formu çevrimdışı çalışmaz.

## Site yapısı

Tek sayfa olarak kaydırılan bir site. Her menü öğesinin ayrıca kendi sayfası da var.

| Menü | Eski URL | Yerel dosya |
|---|---|---|
| Ana Sayfa | `/` | `index.html` |
| Hakkımızda | `/?page_id=7` | `index.html@page_id=7.html` |
| Ürünler ve Hizmetlerimiz | `/?page_id=27` | `index.html@page_id=27.html` |
| İş Ortaklarımız | `/?page_id=12` | `index.html@page_id=12.html` |
| Referanslar | `/?page_id=20` | `index.html@page_id=20.html` |
| İletişim | `/?page_id=24` | `index.html@page_id=24.html` |

## Firma bilgileri (eski siteden)

- **Unvan:** Pozitif Marin Elektrik Turz. Ltd. Şti.
- **Adres:** Aydıntepe Mah. Emek Sok. No: 13/A D.1 Tuzla - İstanbul
- **Tel & Faks:** +90 216 395 99 44
- **Cep:** +90 532 706 44 06
- **E-posta:** info@pozitifelektrik.org
- **Vergi:** Tuzla V.D. 733 036 0072
- **IBAN:** TR-40 0004 6002 3888 8000 0842 29
- **Harita koordinatı:** 40.841085, 29.296073
- **Facebook:** https://www.facebook.com/pozitifmarinelektrik

**Hakkımızda:** 2005'te kuruldu (öncesinde 15 yıllık tecrübe). Denizcilik sektöründe elektrik ve elektronik proje, donatım, bakım-onarım ve servis hizmetleri veriyor. Tam metin: `icerik/sayfalar/01-hakkimizda.md`.

## Ürünler ve hizmetler (98 öğe, 7 kategori)

| Kategori | Adet |
|---|---|
| Kumanda Panelleri | 23 |
| Sigorta ve Alarm Panelleri | 18 |
| Teslim Edilen Projeler | 18 |
| Ürünler | 17 |
| Tekne Yazıları | 9 |
| Alt Yapı Hizmetleri | 7 |
| Projeler | 6 |

"Ürünler" kategorisinde ürün adları var (AC/DC otomatik sigortalar, akü şalterleri, inverterler, baş pervaneler, su yapıcılar, marin uydu sistemleri vb.). Diğer kategorilerdeki öğelerin başlıkları sadece kod (`tk016`, `kp020`, `kksap005`...) ve hiçbir öğede açıklama metni yok. Ayrıntı: `icerik/portfolyo.md`.

## Referanslar (32 firma)

Kale Kilit ve Kalıp Sanayi A.Ş., Kale Endüstri Holding, Enka İnşaat ve San. A.Ş., Sanovel İlaç Sanayi, Depar Motor, Artı Marin Elektrik, Sanset Gıda Sanayi, Numarine Denizcilik, Balsu Gıda ve Sanayi A.Ş., Teknomar Denizcilik, Harman Turizm, Akdeniz İnşaat, Özel Kadıoğlu Hastanesi, Ogem Group, Manas Denizcilik, Labranda Denizcilik, Budo Otelcilik, Güney Yıldızı Petrol, Trio Deniz Araçları, Marina Deniz Araçları, Fibromar Deniz Hizmetleri, Aquamotor Deniz Hizmetleri, Çıpa Marina, Elektromarin Turizm, Şentürk Denizcilik, Ses Yacht, Yuka Yacht, Acar Yacht, Mert Yacht, Edim Mimarlık, Can Makine Denizcilik, Uludağ Yatçılık.

**İş ortakları:** Logolar tek bir görselde birleşik: `medya/orijinaller/IsOrtaklarimiz.jpg`. Görselde Mastervolt, Intellian, Tecma (by Thetford), Atlas Marine Systems, Mert Yacht, Marine Air Systems, Horizon Reverse Osmosis, Cruisair, Marina Deniz Araçları, Rodriquez, Ses Yachts, Artı Marin ve Max var.

## Tasarım

- **Tema:** WordPress "Aether" (Bootstrap 2, jQuery, skrollr parallax, queryLoader2 açılış ekranı)
- **Fontlar:** Sanchez (başlıklar), Andika (metin), Google Fonts'tan
- **Renkler:** beyaz zemin, açık mavi vurgu (`#66adf7`, `#75bcff`, `#1373dc`), koyu gri bantlar (`#333`), metin `#5c5c5c`
- **Logo:** `medya/orijinaller/Mlogo1.jpg` (sadece 150×70 px)
- **Ana görseller:** `home-bg1.jpg` ve `Ana001.jpg` – `Ana007.jpg`

## Yeni site için dikkat edilecekler

1. **Fotoğraflarda filigran var.** Orijinallerin içine bile kırmızı "Pozitif Elektrik" yazısı gömülü. Müşteriden filigransız fotoğrafları istemek lazım.
2. **Logo çok küçük ve düşük çözünürlüklü.** Müşteriden vektör (SVG/AI/PDF) veya yüksek çözünürlüklü logo istenmeli.
3. **HTTPS yok.** Site yalnızca `http://` ile açılıyor. Yeni sitede SSL şart.
4. **Altyapı çok eski.** PHP 5.6.40 ve 2014'ten kalma WordPress kurulumu kullanılıyor.
5. **Google Haritalar çalışmıyor.** API anahtarı olmadığı için harita yerine koordinat yazısı görünüyor.
6. **Footer'da tema yazısı kalmış:** "Pozitif Marin Elektrik template. All Rights Reserved"
7. **Ürün/proje öğeleri dağınık.** Başlıklar kod gibi (`tk016`), açıklama yok. Yeni sitede adlandırma ve kısa açıklamalar müşteriyle birlikte hazırlanmalı.
8. **Varsayılan içerik kalmış.** WordPress'in "Hello world!" yazısı hâlâ duruyor. Blog bölümü kullanılmamış.
9. **SEO eksik.** Sitemap ve robots.txt yok. Sayfa adresleri `?page_id=` biçiminde.

## Bu arşivde olmayanlar

Web üzerinden yalnızca ziyaretçinin gördüğü çıktı indirilebilir. Aşağıdakiler bu arşivde yok:

- WordPress veritabanı (MySQL)
- PHP tema kaynak kodu
- İletişim formuna gelmiş mesajlar
- Yönetici ayarları

Bunlara ihtiyaç olursa hosting panelinden (cPanel/FTP) tam yedek alınması gerekir.
