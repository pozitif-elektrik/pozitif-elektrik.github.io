#!/usr/bin/env python3
"""Pozitif Marin Elektrik — çok sayfalı statik site üreticisi.

Kullanım:  python3 kaynak/build.py
Çıktı:     yeni-site/*.html, yeni-site/sitemap.xml

Ortak üst menü, alt bilgi ve <head> burada tek yerde tanımlıdır; her sayfa
kendi içeriğiyle bu iskeletten üretilir. Görseller yeni-site/assets/img altındadır.
Galeri ve ürün listesi kaynak/veri.json dosyasından gelir.
"""
import html
import json
import os
import struct
from collections import Counter

KOK = os.path.dirname(os.path.abspath(__file__))
CIKTI = os.path.join(os.path.dirname(KOK), "yeni-site")
SITE = "https://pozitifelektrik.org"
VERI = json.load(open(os.path.join(KOK, "veri.json"), encoding="utf-8"))
e = html.escape

TEL, TEL_HREF = "+90 216 395 99 44", "tel:+902163959944"
CEP, CEP_HREF = "+90 532 706 44 06", "tel:+905327064406"
EPOSTA = "info@pozitifelektrik.org"
ADRES1, ADRES2 = "Aydıntepe Mah. Emek Sok. No: 13/A D.1", "Tuzla / İstanbul"
FACEBOOK = "https://www.facebook.com/pozitifmarinelektrik"
HARITA = "40.841085,29.296073"

# Tema renkleri: (açık, koyu). Tailwind'de bg-zemin, text-metin, border-cizgi... olarak kullanılır.
RENKLER = {
    "zemin": ("#ffffff", "#0b1220"),          # sayfa zemini
    "zemin-2": ("#f4f6f9", "#101a2e"),        # ara bölümler
    "yuzey": ("#ffffff", "#141f35"),          # kartlar
    "cizgi": ("#e3e8ef", "#253149"),          # kenarlıklar
    "metin": ("#111827", "#e5e9f0"),
    "koyu": ("#0f172a", "#060b16"),           # koyu bantlar: hero, sayfa başlığı, alt bilgi
    "koyu-metin": ("#f1f5f9", "#f1f5f9"),
    "ters": ("#0f172a", "#f1f5f9"),           # dolu düğme ve simge kutusu (logodaki kutucuk rengi)
    "ters-metin": ("#ffffff", "#0f172a"),
    "kirmizi": ("#e30613", "#e30613"),        # logodaki artı
    "kirmizi-koyu": ("#c8050f", "#c8050f"),   # kırmızı düğmenin üzerine gelince
    "kirmizi-metin": ("#c8050f", "#ff6b70"),  # kırmızı yazı (iki zeminde de okunur kontrast)
    "kirmizi-acik": ("#ff6b70", "#ff6b70"),   # koyu bantlardaki kırmızı yazı
    "mavi-metin": ("#1d6fb8", "#7cb4f5"),
}

MENU = [
    ("index.html", "Ana Sayfa"),
    ("hakkimizda.html", "Hakkımızda"),
    ("hizmetler.html", "Hizmetler"),
    ("projeler.html", "Projeler"),
    ("urunler.html", "Ürünler"),
    ("is-ortaklarimiz.html", "İş Ortaklarımız"),
    ("referanslar.html", "Referanslar"),
    ("iletisim.html", "İletişim"),
]

# Eski sitenin galeri kategorileri → yeni slug ve görünen ad
KATEGORI = [
    ("teslim-edilen-projeler", "Teslim Edilen Projeler", "Teslim Edilen Projeler"),
    ("kumanda-panelleri", "Kumanda Panelleri", "Kumanda Panelleri"),
    ("sigorta-alarm-panelleri", "Sigorta ve Alarm Panelleri", "Sigorta Ve Alarm Panelleri"),
    ("alt-yapi", "Kablolama ve Altyapı", "Alt Yapı Hizmetleri"),
    ("tekne-yazilari", "Tekne Yazıları", "Tekne Yazıları"),
    ("proje-cizimleri", "Proje Çizimleri", "Projeler"),
]
ESKI2YENI = {eski: (slug, ad) for slug, ad, eski in KATEGORI}
GALERI = {g["img"].split("/")[-1][:-4]: g for g in VERI["galeri"]}


def ikon(yol, cls="size-6"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="{cls}" aria-hidden="true">{yol}</svg>')


IKON = {
    "tel": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.79 19.79 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.58 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "cep": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>',
    "posta": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "konum": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "proje": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "kumanda": '<rect x="3" y="4" width="18" height="14" rx="2"/><circle cx="8" cy="11" r="2"/><path d="M14 9h4M14 13h4M7 21h10"/>',
    "sigorta": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "altyapi": '<path d="M4 7h16M4 12h16M4 17h16"/><circle cx="8" cy="7" r="1.5"/><circle cx="15" cy="12" r="1.5"/><circle cx="10" cy="17" r="1.5"/>',
    "yazi": '<path d="M4 7V5h16v2M9 19h6M12 5v14"/>',
    "servis": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
    "ok": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "tik": '<path d="M20 6 9 17l-5-5"/>',
    "ay": '<path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5a8.5 8.5 0 1 0 11 11Z"/>',
    "gunes": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "kapat": '<path d="M18 6 6 18M6 6l12 12"/>',
    "sag": '<path d="m9 6 6 6-6 6"/>',
    "buyut": '<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>',
}

# ---------------------------------------------------------------- LOGO (öneri C)
# kaynak/logo.py üretir. Kutucuklar ve yazı currentColor: açık temada lacivert,
# koyu temada beyaz. Artı her iki temada kırmızı.
LOGO_SVG = open(os.path.join(KOK, "logo-site.svg"), encoding="utf-8").read().strip()
AMBLEM_SVG = open(os.path.join(KOK, "amblem-site.svg"), encoding="utf-8").read().strip()
LOGO_ORAN = "aspect-[2288/488]"


def logo(cls, etiket=None, kaynak=LOGO_SVG):
    """Satır içi logo. etiket verilirse ekran okuyucuya ad olarak okunur;
    verilmezse (ör. etiketli bir bağlantının içinde) gizlenir."""
    a = f'role="img" aria-label="{e(etiket)}"' if etiket else 'aria-hidden="true"'
    return kaynak.replace("<svg ", f'<svg class="{cls}" {a} ', 1)


def arti(cls="size-2.5"):
    """Logodaki kırmızı artının küçük hali: madde imi ve üst başlık işareti."""
    return (f'<svg viewBox="0 0 10 10" class="shrink-0 text-kirmizi {cls}" aria-hidden="true">'
            '<path d="M5 1.2v7.6M1.2 5h7.6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>')


# ---------------------------------------------------------------- DÜĞMELER
# Yalnızca Tailwind sınıfları (bileşen kütüphanesi yok). Renkler <head> içindeki tema
# değişkenlerinden gelir; koyu temada kendiliğinden değişir.
_DUGME = ("cursor-pointer items-center justify-center gap-2 whitespace-nowrap rounded-lg font-semibold "
          "transition-colors duration-150 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kirmizi")
_BOY = {"xs": "h-7 px-2.5 text-xs", "sm": "h-9 px-3.5 text-sm", "md": "h-11 px-5", "lg": "h-13 px-6 text-lg"}
_TUR = {
    "ana": "bg-kirmizi text-white hover:bg-kirmizi-koyu",
    "ters": "bg-ters text-ters-metin hover:bg-ters/85",
    "ikincil": "border border-cizgi bg-yuzey text-metin shadow-xs hover:border-metin/30 hover:bg-zemin-2",
    "kenar": "border border-metin/30 text-metin hover:border-metin hover:bg-metin hover:text-zemin",
    "acik-kenar": "border border-white/40 text-white hover:border-white hover:bg-white hover:text-koyu",
    "hayalet": "text-metin hover:bg-metin/5",
}
SIMGE_DUGME = ("grid size-10 cursor-pointer place-items-center rounded-lg text-metin/80 transition-colors "
               "hover:bg-metin/8 hover:text-metin focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kirmizi")


def dugme(tur="ikincil", boy="md", ek=""):
    # ek "hidden sm:inline-flex" gibi bir görünürlük içeriyorsa inline-flex eklenmez
    # (ikisi birlikte olursa hangisinin geçerli olacağı CSS sırasına kalır)
    gorunum = "" if "hidden" in ek.split() else "inline-flex "
    return f"{gorunum}{_DUGME} {_BOY[boy]} {_TUR[tur]} {ek}".strip()
FB_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-5" aria-hidden="true">'
          '<path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0 0 22 12Z"/></svg>')

# ---------------------------------------------------------------- HİZMETLER
HIZMETLER = [
    dict(id="projelendirme", ikon="proje", kategori="proje-cizimleri", baslik="Elektrik projelendirme",
         kisa="Teknenin AC ve DC elektrik şemalarını, yük dağılımını ve pano yerleşimlerini ihtiyaca göre çiziyoruz.",
         metin=["Her teknenin elektrik ihtiyacı farklıdır: sahil elektriği ve jeneratör girişleri, akü grupları, 12/24V DC ve 230V AC tüketiciler, seyir ve haberleşme cihazları. Projelendirme aşamasında bütün bu sistemleri tek bir plan üzerinde bir araya getiriyoruz.",
                "Hazırladığımız tek hat şemaları ve pano yerleşim çizimleri, imalat ve montajın yol haritası olur; teslimden sonra da bakım ve arıza tespitinde teknenin elektrik kimliği olarak kalır."],
         kapsam=["Tek hat şemaları ve dağıtım planları", "AC ve DC pano ön yüz tasarımları", "Akü grupları, şarj ve invertör kurgusu", "Kablo güzergâhı ve bağlantı planları"],
         gorseller=["pj001", "pj002", "pj003", "pj006"]),
    dict(id="kumanda-panelleri", ikon="kumanda", kategori="kumanda-panelleri", baslik="Kumanda panelleri",
         kisa="Kaptan köşkü konsollarını seyir cihazları ve göstergelerle birlikte, tekneye özel olarak imal ediyoruz.",
         metin=["Kaptan köşkü, teknenin bütün sistemlerinin yönetildiği yerdir. Seyir ekranlarını, motor göstergelerini, kumanda anahtarlarını ve haberleşme cihazlarını konsola, kullanımı kolay ve düzenli bir yerleşimle yerleştiriyoruz.",
                "Paneller teknenin iç tasarımıyla uyumlu malzemelerde imal edilir; aydınlatma, sintine ve güverte ekipmanlarının kumandaları etiketli anahtar gruplarında toplanır."],
         kapsam=["Konsol ve dümen paneli yerleşimleri", "Seyir ekranı ve plotter entegrasyonu", "Motor göstergeleri ve alarm grupları", "Aydınlatma, sintine ve güverte kumandaları"],
         gorseller=["kp015", "kp004", "kp011", "kp001"]),
    dict(id="sigorta-alarm-panolari", ikon="sigorta", kategori="sigorta-alarm-panelleri", baslik="Sigorta ve alarm panoları",
         kisa="Tekne silüeti işlenmiş 12V/24V DC ve 230V AC dağıtım, sigorta ve alarm panolarını tasarlayıp üretiyoruz.",
         metin=["Teknenin elektrik dağıtımı bu panolardan yönetilir. 12V/24V DC ve 230V AC devreleri, her biri etiketli sigorta ve anahtarlarla gruplanmış, ön yüzüne teknenin silüeti işlenmiş panolar halinde tasarlayıp üretiyoruz.",
                "Akü ve jeneratör gerilimleri, tank seviyeleri ve sistem uyarıları aynı pano üzerinden izlenir; kaptan, tek bakışta teknenin elektrik durumunu görür."],
         kapsam=["AC ve DC dağıtım panoları", "Akü ve jeneratör gerilim/akım göstergeleri", "Sahil elektriği, jeneratör ve akü seçim anahtarları", "Pis su, gri su tank seviyesi ve alarm göstergeleri"],
         gorseller=["kksap002", "kksap012", "kksap016", "kksap019"]),
    dict(id="kablolama-altyapi", ikon="altyapi", kategori="alt-yapi", baslik="Kablolama ve altyapı",
         kisa="Kablo kanalları, bağlantı kutuları, akü bağlantıları ve güç dağıtımıyla teknenin elektrik altyapısını kuruyoruz.",
         metin=["Görünmeyen ama en kritik kısım altyapıdır. Kablo kanallarını, bağlantı kutularını, sigorta ve akü bağlantılarını düzenli, etiketli ve bakımı kolay olacak şekilde kuruyoruz.",
                "İyi kurulmuş bir altyapı, yıllar sonra yapılacak bir arıza tespitini dakikalara indirir; yeni bir cihaz eklemek de sistemin geri kalanını bozmadan mümkün olur."],
         kapsam=["Kablo kanalı ve güzergâh montajı", "Bağlantı kutuları ve klemens düzenleri", "Akü bağlantıları ve ana sigortalar", "Güç dağıtım modüllerinin montajı"],
         gorseller=["aykmdp001", "aykmdp002", "aykmdp004", "aykmdp006"]),
    dict(id="tekne-yazilari", ikon="yazi", kategori="tekne-yazilari", baslik="Işıklı tekne yazıları",
         kisa="LED arka aydınlatmalı ve paslanmaz harf tekne isim yazılarını tasarlıyor, elektrik sistemine bağlıyoruz.",
         metin=["Teknenin adı, kimliğidir. LED arka aydınlatmalı ya da paslanmaz harf isim yazılarını teknenin formuna ve rengine uygun olarak hazırlıyoruz.",
                "Aydınlatmalı yazılar teknenin elektrik sistemine bağlanır ve kumanda panelinden kontrol edilir; beyaz, mavi ya da kırmızı ışıkla gece de görünür."],
         kapsam=["LED arka aydınlatmalı isim yazıları", "Paslanmaz çelik harfler", "Beyaz, mavi ve kırmızı ışık seçenekleri", "Elektrik sistemine bağlantı ve kumanda"],
         gorseller=["tk0091", "tk0051", "tk0081", "tk0061"]),
    dict(id="urun-servis", ikon="servis", kategori=None, baslik="Ürün satışı, bakım ve servis",
         kisa="Temsil ettiğimiz markaların ürünlerini temin ediyor, montajını, bakım-onarımını ve servisini yapıyoruz.",
         metin=["Dünyaca ünlü markaların satış ve servis hizmetlerini veriyoruz. Teknenin ihtiyacına uygun ürünü seçmekten montajına, devreye almadan bakım ve onarıma kadar aynı ekip yanınızda.",
                "Mevcut bir teknenin elektrik sistemine yeni cihaz eklemek, eskiyen bileşenleri yenilemek ya da arızayı tespit etmek için de bize ulaşabilirsiniz."],
         kapsam=["Ürün seçimi ve temini", "Montaj ve devreye alma", "Bakım ve arıza onarımı", "Mevcut sistemlerde yenileme ve ekleme"],
         gorseller=[]),
]

# ---------------------------------------------------------------- ÜRÜNLER
URUN_ACIKLAMA = {
    "Switch'ler": "Pano ve konsollar için marin tip, ışıklı anahtarlar.",
    "Su Yapıcılar": "Deniz suyundan tatlı su üreten ters ozmoz sistemleri.",
    "Marin Uydu Sistemleri": "Seyir halinde uydu TV ve iletişim için stabilize antenler.",
    "Jel, AGM ve Stasyoner Aküler": "Servis ve marş grupları için bakım gerektirmeyen aküler.",
    "Dümen Açı Göstergeleri ve Müşürleri": "Dümen konumunu kaptan köşküne ileten gösterge ve sensörler.",
    "DC Otomatik Sigortalar": "12/24V DC devreler için marin tip otomatik sigortalar.",
    "Compact Retract Baş Pervaneler": "Kullanılmadığında gövde içine çekilen baş pervaneleri.",
    "Akü Şalterleri": "Akü gruplarını devreye alan ve ayıran ana şalterler.",
    "AC Otomatik Sigortalar": "230V AC devreler için otomatik sigortalar.",
    "Seyir Fenerleri": "Farklı tekne boylarına uygun seyir fenerleri.",
    "Uzaktan Kumandalı Projektörler": "Kaptan köşkünden yönetilen arama projektörleri.",
    "İnvertörler": "Akü gücünü 230V AC'ye çeviren invertörler.",
    "Gazlı Sistem Klimalar": "Tekne içi iklimlendirme için marin klimalar.",
    "Acil Stop (Emergency Stop) Butonları": "Motor ve sistemler için acil durdurma butonları.",
    "Kompakt Şalterler": "Dağıtım panoları için kompakt şalterler.",
    "Combi (Akü Şarj & İnvertör)": "Akü şarj cihazı ve invertör tek ünitede.",
    "Akü Şarj Üniteleri": "Sahil elektriği veya jeneratörden akü şarjı.",
}
URUN_GRUPLARI = [
    ("enerji", "Enerji ve şarj sistemleri",
     "Teknenin enerji kaynağı aküler, şarj cihazları ve invertörlerdir. Servis ve marş akü gruplarını sahil elektriği ve jeneratörle birlikte çalışacak şekilde kurguluyoruz.",
     ["Jel, AGM ve Stasyoner Aküler", "Akü Şarj Üniteleri", "İnvertörler", "Combi (Akü Şarj & İnvertör)"]),
    ("dagitim", "Dağıtım ve koruma",
     "Devreleri koruyan sigortalar, akü gruplarını yöneten şalterler ve panolarda kullanılan anahtarlar.",
     ["Akü Şalterleri", "AC Otomatik Sigortalar", "DC Otomatik Sigortalar", "Kompakt Şalterler", "Switch'ler", "Acil Stop (Emergency Stop) Butonları"]),
    ("seyir", "Seyir ve güverte",
     "Seyir güvenliği ve manevra için fenerler, projektörler, dümen göstergeleri ve baş pervaneleri.",
     ["Seyir Fenerleri", "Uzaktan Kumandalı Projektörler", "Dümen Açı Göstergeleri ve Müşürleri", "Compact Retract Baş Pervaneler"]),
    ("konfor", "Konfor ve iletişim",
     "Uzun seyirlerde hayatı kolaylaştıran uydu, su yapıcı ve iklimlendirme sistemleri.",
     ["Marin Uydu Sistemleri", "Su Yapıcılar", "Gazlı Sistem Klimalar"]),
]
URUN = {u["ad"]: u for u in VERI["urunler"]}
assert set(URUN) == set(URUN_ACIKLAMA) == {a for g in URUN_GRUPLARI for a in g[3]}

# ---------------------------------------------------------------- ORTAKLAR & REFERANSLAR
MARKALAR = [
    ("Mastervolt", "Akü, şarj cihazı, invertör ve güç dağıtım sistemleri"),
    ("Intellian", "Marin uydu TV ve iletişim antenleri"),
    ("Tecma by Thetford", "Tekne tuvalet sistemleri"),
    ("Atlas Marine Systems", "Sahil elektriği dönüştürücüleri"),
    ("Marine Air Systems", "Marin klima sistemleri"),
    ("Cruisair", "Marin klima sistemleri"),
    ("Horizon Reverse Osmosis", "Ters ozmoz su yapıcılar"),
    ("Max", ""),
]
TERSANELER = [
    ("Rodriquez", "Yat üreticisi"),
    ("Mert Yacht", "Yat üreticisi"),
    ("Ses Yachts", "Motor ve yelkenli yat tasarım ve inşa"),
    ("Marina Deniz Araçları Tic. ve San. A.Ş.", "Deniz araçları"),
    ("Artı Marin", "Denizcilik"),
]
REFERANS_GRUPLARI = [
    ("Denizcilik ve yat", ["Numarine Denizcilik", "Teknomar Denizcilik", "Manas Denizcilik", "Labranda Denizcilik", "Şentürk Denizcilik",
                           "Can Makine Denizcilik", "Trio Deniz Araçları", "Marina Deniz Araçları", "Fibromar Deniz Hizmetleri",
                           "Aquamotor Deniz Hizmetleri", "Çıpa Marina", "Elektromarin Turizm", "Artı Marin Elektrik", "Ses Yacht",
                           "Yuka Yacht", "Acar Yacht", "Mert Yacht", "Uludağ Yatçılık"]),
    ("Sanayi, inşaat ve holding", ["Kale Kilit ve Kalıp Sanayi A.Ş.", "Kale Endüstri Holding", "Enka İnşaat ve San. A.Ş.", "Sanovel İlaç Sanayi",
                                   "Sanset Gıda Sanayi", "Balsu Gıda ve Sanayi A.Ş.", "Ogem Group", "Güney Yıldızı Petrol", "Depar Motor",
                                   "Akdeniz İnşaat", "Edim Mimarlık"]),
    ("Turizm ve hizmet", ["Harman Turizm", "Budo Otelcilik", "Özel Kadıoğlu Hastanesi"]),
]
assert sum(len(g[1]) for g in REFERANS_GRUPLARI) == 32


# ================================================================ ORTAK PARÇALAR
def head(sayfa, baslik, aciklama, ek=""):
    url = f"{SITE}/" if sayfa == "index.html" else f"{SITE}/{sayfa[:-5]}"
    acik = "\n".join(f"      --color-{k}: {v[0]};" for k, v in RENKLER.items())
    koyu = "\n".join(f"      --color-{k}: {v[1]};" for k, v in RENKLER.items() if v[1] != v[0])
    return f"""<!doctype html>
<html lang="tr" class="scroll-smooth">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(baslik)}</title>
  <meta name="description" content="{e(aciklama)}">
  <meta name="theme-color" content="{RENKLER['zemin'][0]}">
  <script>
    // Tema, sayfa çizilmeden önce seçilir (beyaz/koyu yanıp sönme olmasın).
    // Ziyaretçinin seçimi yoksa cihazın ayarı geçerlidir. Düğme: assets/js/main.js
    (function () {{
      var t;
      try {{ t = localStorage.getItem('tema'); }} catch (e) {{}}
      if (t !== 'koyu' && t !== 'acik') t = matchMedia('(prefers-color-scheme: dark)').matches ? 'koyu' : 'acik';
      document.documentElement.setAttribute('data-tema', t);
    }})();
  </script>
  <style>
    :root {{ color-scheme: light; background: {RENKLER['zemin'][0]}; }}
    :root[data-tema="koyu"] {{
      color-scheme: dark;
      background: {RENKLER['zemin'][1]};
{koyu}
    }}
    html:has(dialog[open]) {{ overflow: hidden; }}
    section[id] {{ scroll-margin-top: 8rem; }}
  </style>
  <link rel="canonical" href="{url}">
  <link rel="icon" href="favicon.ico" sizes="32x32">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="tr_TR">
  <meta property="og:site_name" content="Pozitif Marin Elektrik">
  <meta property="og:title" content="{e(baslik)}">
  <meta property="og:description" content="{e(aciklama)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/bolum/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.3.5"></script>
  <style type="text/tailwindcss">
    /* dark: sınıfları ziyaretçinin seçtiği temaya bağlı (cihaz ayarına değil) */
    @custom-variant dark (&:where([data-tema=koyu], [data-tema=koyu] *));
    /* Açık tema renkleri. Koyu tema karşılıkları yukarıdaki <style> içinde aynı
       değişkenleri ezer; bg-zemin, text-metin/70 gibi sınıflar iki temada da çalışır. */
    @theme {{
      --font-sans: "Barlow", ui-sans-serif, system-ui, sans-serif;
{acik}
    }}
  </style>{ek}
</head>"""


def ust_menu(aktif):
    def li(href, ad, cls):
        a = ' aria-current="page"' if href == aktif else ""
        return f'<li><a href="{href}" class="{cls}"{a}>{e(ad)}</a></li>'
    # Etkin sayfa aria-current ile işaretlenir; görünümü de aynı öznitelikten gelir
    m_cls = ("block rounded-lg px-3 py-2 text-metin/80 transition-colors hover:bg-metin/5 hover:text-metin "
             "aria-[current=page]:bg-metin/8 aria-[current=page]:text-metin")
    k_cls = ("block rounded-lg px-4 py-3 text-lg font-medium hover:bg-metin/5 "
             "aria-[current=page]:bg-metin/8 aria-[current=page]:text-kirmizi-metin")
    masaustu = "\n          ".join(li(h, a, m_cls) for h, a in MENU[1:])
    mobil = "\n          ".join(li(h, a, k_cls) for h, a in MENU)
    return f"""<body class="bg-zemin font-sans text-metin antialiased">
<a href="#icerik" class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100] {dugme('ters', 'sm')}">İçeriğe geç</a>

<header id="ust" class="sticky top-0 z-50 border-b border-transparent bg-zemin/95 backdrop-blur transition-shadow dark:border-cizgi/70">
  <div class="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 lg:px-6">
    <a href="index.html" class="shrink-0 rounded-md focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-kirmizi" aria-label="Pozitif Marin Elektrik - Ana sayfa">
      {logo(f"h-8 w-auto {LOGO_ORAN} text-[#0f172a] sm:h-9 dark:text-white")}
    </a>
    <nav class="hidden xl:block" aria-label="Ana menü">
      <ul class="flex items-center gap-1 text-[0.95rem] font-medium">
          {masaustu}
      </ul>
    </nav>
    <div class="flex items-center gap-2">
      <button type="button" class="{SIMGE_DUGME}" data-tema-dugme aria-label="Koyu tema" aria-pressed="false" title="Koyu temaya geç">
        {ikon(IKON['ay'], 'size-5 dark:hidden')}{ikon(IKON['gunes'], 'hidden size-5 dark:block')}
      </button>
      <a href="{TEL_HREF}" class="{dugme('ters', 'md', 'hidden sm:inline-flex')}">{ikon(IKON['tel'], 'size-4')} 0216 395 99 44</a>
      <details class="group relative xl:hidden" data-mobil-menu>
        <summary class="{SIMGE_DUGME} list-none [&::-webkit-details-marker]:hidden" aria-label="Menü">
          {ikon(IKON['menu'], 'size-6 group-open:hidden')}{ikon(IKON['kapat'], 'hidden size-6 group-open:block')}
        </summary>
        <nav class="absolute right-0 top-full z-50 mt-3 w-72 rounded-xl border border-cizgi bg-yuzey p-2 shadow-xl" aria-label="Ana menü">
          <ul>
          {mobil}
          </ul>
          <a href="{TEL_HREF}" class="{dugme('ters', 'md', 'mt-2 w-full')}">{ikon(IKON['tel'], 'size-4')} 0216 395 99 44</a>
        </nav>
      </details>
    </div>
  </div>
</header>

<main id="icerik">"""


def cta_bandi():
    return f"""
<section aria-label="İletişime geçin" class="bg-zemin-2">
  <div class="mx-auto flex max-w-7xl flex-col items-start gap-6 px-4 py-14 lg:flex-row lg:items-center lg:justify-between lg:px-6">
    <div class="max-w-2xl">
      <h2 class="text-2xl font-extrabold tracking-tight sm:text-3xl">Teknenizin elektrik sistemi için bize ulaşın</h2>
      <p class="mt-2 text-lg text-metin/70">Yeni bir proje, bir yenileme ya da bir arıza: ilk görüşmeyi telefonda yapalım.</p>
    </div>
    <div class="flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
      <a href="{TEL_HREF}" class="{dugme('ters', 'lg')}">{ikon(IKON['tel'], 'size-5')} {TEL}</a>
      <a href="mailto:{EPOSTA}" class="{dugme('kenar', 'lg')}">{ikon(IKON['posta'], 'size-5')} E-posta gönderin</a>
    </div>
  </div>
</section>"""


def alt_bilgi(pencere=False, bildirim=False):
    bag = "w-fit text-koyu-metin/85 hover:text-white hover:underline underline-offset-4"
    site = "\n      ".join(f'<a class="{bag}" href="{h}">{e(a)}</a>' for h, a in MENU[1:5])
    kurumsal = "\n      ".join(f'<a class="{bag}" href="{h}">{e(a)}</a>' for h, a in MENU[5:])
    baslik = "mb-1 text-sm font-semibold uppercase tracking-[0.15em] text-koyu-metin/50"
    # Fotoğraf büyütme: PhotoSwipe 5 (MIT), assets/js/galeri.js içinde CDN'den modül olarak yüklenir
    p = '\n<script type="module" src="assets/js/galeri.js"></script>' if pencere else ""
    b = f"""
<div class="fixed bottom-4 right-4 z-[60] flex items-center gap-2 rounded-lg bg-emerald-700 px-4 py-3 text-sm font-medium text-white shadow-lg" role="status" data-bildirim hidden>
  {ikon(IKON['tik'], 'size-4')}<span data-bildirim-metin>IBAN kopyalandı</span>
</div>""" if bildirim else ""
    return f"""
</main>

<footer class="bg-koyu text-koyu-metin dark:border-t dark:border-white/5">
  <div class="mx-auto grid max-w-7xl gap-10 px-4 py-14 sm:grid-cols-2 lg:grid-cols-[1.4fr_1fr_1fr_1.2fr] lg:px-6">
    <div class="max-w-xs">
      {logo(f"h-10 w-auto {LOGO_ORAN} text-white", "Pozitif Marin Elektrik")}
      <p class="mt-5 leading-relaxed text-koyu-metin/70">Denizcilik sektöründe elektrik ve elektronik proje, donatım, bakım-onarım ve servis. 2005'ten bu yana Tuzla, İstanbul.</p>
      <a href="{FACEBOOK}" target="_blank" rel="noopener" class="mt-3 inline-flex items-center gap-2 text-koyu-metin/80 underline-offset-4 hover:text-white hover:underline">{FB_SVG} Facebook</a>
    </div>
    <nav aria-label="Hizmetler ve projeler" class="flex flex-col gap-2">
      <h2 class="{baslik}">Neler yapıyoruz</h2>
      {site}
    </nav>
    <nav aria-label="Kurumsal" class="flex flex-col gap-2">
      <h2 class="{baslik}">Kurumsal</h2>
      {kurumsal}
    </nav>
    <nav aria-label="İletişim bilgileri" class="flex flex-col gap-2">
      <h2 class="{baslik}">İletişim</h2>
      <a class="{bag}" href="{TEL_HREF}">{TEL}</a>
      <a class="{bag}" href="{CEP_HREF}">{CEP}</a>
      <a class="{bag}" href="mailto:{EPOSTA}">{EPOSTA}</a>
      <span class="text-koyu-metin/70">{ADRES1}<br>{ADRES2}</span>
    </nav>
  </div>
  <div class="border-t border-white/10">
    <div class="mx-auto flex max-w-7xl flex-col gap-2 px-4 py-6 text-sm text-koyu-metin/60 sm:flex-row sm:justify-between lg:px-6">
      <p>© <span data-yil>2026</span> Pozitif Marin Elektrik Turz. Ltd. Şti. Tüm hakları saklıdır.</p>
      <a href="#icerik" class="hover:underline underline-offset-4">Başa dön ↑</a>
    </div>
  </div>
</footer>
{b}
<script src="assets/js/main.js" defer></script>{p}
</body>
</html>
"""


# Kart: açık temada hafif gölge, koyu temada (gölge görünmediği için) yalnızca kenarlık
KART = "flex flex-col rounded-xl border border-cizgi bg-yuzey shadow-sm dark:shadow-none"


def sayfa_basligi(aktif_ad, ust, baslik, aciklama, gorsel, alt, w, h):
    return f"""
<section class="bg-koyu text-koyu-metin">
  <div class="mx-auto grid max-w-7xl items-center gap-10 px-4 py-12 lg:grid-cols-2 lg:gap-16 lg:px-6 lg:py-16">
    <div>
      <nav aria-label="Konum" class="text-sm text-koyu-metin/60">
        <ol class="flex flex-wrap items-center gap-1.5">
          <li><a href="index.html" class="underline-offset-4 hover:text-white hover:underline">Ana Sayfa</a></li>
          <li class="flex items-center gap-1.5">{ikon(IKON['sag'], 'size-3.5 opacity-60')}<span aria-current="page" class="text-koyu-metin/85">{e(aktif_ad)}</span></li>
        </ol>
      </nav>
      <p class="mt-6 inline-flex items-center gap-2.5 text-sm font-semibold uppercase tracking-[0.2em] text-white/70">{arti()} {e(ust)}</p>
      <h1 class="mt-3 text-4xl font-extrabold leading-tight tracking-tight text-white sm:text-5xl">{e(baslik)}</h1>
      <p class="mt-5 max-w-xl text-lg text-white/75">{aciklama}</p>
    </div>
    <img src="{gorsel}" alt="{e(alt)}" width="{w}" height="{h}" fetchpriority="high" class="aspect-[4/3] w-full rounded-xl object-cover shadow-2xl">
  </div>
</section>"""


def bolum_basligi(ust, baslik, aciklama="", ortali=False):
    hiza = "mx-auto text-center" if ortali else ""
    a = f'\n      <p class="mt-4 text-lg text-metin/70">{aciklama}</p>' if aciklama else ""
    return f"""<div class="max-w-2xl {hiza}">
      <p class="text-sm font-semibold uppercase tracking-[0.2em] text-kirmizi-metin">{e(ust)}</p>
      <h2 class="mt-3 text-3xl font-extrabold tracking-tight sm:text-4xl">{e(baslik)}</h2>{a}
    </div>"""


def jpeg_boyut(yol, _onbellek={}):
    """JPEG'in piksel boyutu (genişlik, yükseklik); Pillow gerektirmez."""
    if yol not in _onbellek:
        with open(os.path.join(CIKTI, yol), "rb") as f:
            v = f.read()
        i = 2
        while i < len(v):
            if v[i] != 0xFF or v[i + 1] == 0xFF:
                i += 1
                continue
            m = v[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", v[i + 5:i + 9])
                _onbellek[yol] = (w, h)
                break
            if m == 0x01 or 0xD0 <= m <= 0xD8:
                i += 2
                continue
            i += 2 + struct.unpack(">H", v[i + 2:i + 4])[0]
        else:
            raise ValueError(f"JPEG boyutu okunamadı: {yol}")
    return _onbellek[yol]


ODAK = "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kirmizi"


def galeri_ogesi(kod, etiket=True):
    """Kare küçük resimli fotoğraf (ana sayfa, hizmetler). Tıklayınca büyütme penceresi açılır;
    JavaScript yoksa bağlantı büyük fotoğrafı doğrudan açar."""
    g = GALERI[kod]
    slug, ad = ESKI2YENI[g["kategori"]]
    w, h = jpeg_boyut(g["img"])
    yazi = (f'<span class="pointer-events-none absolute inset-x-0 bottom-0 bg-linear-to-t from-black/75 to-transparent p-3 pt-10 text-left text-sm font-semibold text-white opacity-0 transition group-hover:opacity-100 group-focus-visible:opacity-100">{e(ad)}</span>'
            if etiket else "")
    return (f'<a href="{g["img"]}" data-pswp-width="{w}" data-pswp-height="{h}" data-cropped="true" data-baslik="{e(ad)}" '
            f'class="group relative block aspect-square overflow-hidden rounded-xl bg-zemin-2 {ODAK}">'
            f'<img src="{g["kucuk"]}" alt="{e(ad)} - Pozitif Marin Elektrik" loading="lazy" decoding="async" width="480" height="480" class="h-full w-full object-cover transition duration-500 group-hover:scale-105">'
            f'{yazi}</a>')


def yasli_oge(g):
    """Projeler galerisi: fotoğraf kendi oranıyla (kırpılmadan). Satırdaki fotoğraflar
    aynı yükseklikte olacak şekilde genişler: flex-grow ve flex-basis en-boy oranıyla
    orantılı (--o), satır yüksekliği kapsayıcıdaki --rh. Kütüphane gerekmez."""
    kod = g["img"].split("/")[-1][:-4]
    _, ad = ESKI2YENI[g["kategori"]]
    w, h = jpeg_boyut(g["img"])
    kucuk = f"assets/img/galeri/onizleme/{kod}.jpg"
    kw, kh = jpeg_boyut(kucuk)
    return (f'<a href="{g["img"]}" data-pswp-width="{w}" data-pswp-height="{h}" data-baslik="{e(ad)}" style="--o:{w / h:.4f}" '
            f'class="group relative block max-w-full overflow-hidden rounded-lg bg-zemin-2 [flex:var(--o)_1_calc(var(--o)*var(--rh))] aspect-(--o) {ODAK}">'
            f'<img src="{kucuk}" alt="{e(ad)} - Pozitif Marin Elektrik" loading="lazy" decoding="async" width="{kw}" height="{kh}" '
            f'class="size-full object-cover transition duration-500 group-hover:scale-[1.03]">'
            f'<span class="pointer-events-none absolute right-2 top-2 grid size-8 place-items-center rounded-full bg-black/55 text-white opacity-0 transition group-hover:opacity-100 group-focus-visible:opacity-100">'
            f'{ikon(IKON["buyut"], "size-4")}</span></a>')


def urun_karti(ad):
    u = URUN[ad]
    return f"""<article class="{KART} overflow-hidden">
          <figure class="aspect-square bg-white p-2"><img src="{u['img']}" alt="{e(ad)}" loading="lazy" decoding="async" width="640" height="640" class="h-full w-full object-contain"></figure>
          <div class="flex flex-col gap-1 p-4">
            <h3 class="text-base font-bold leading-snug">{e(ad)}</h3>
            <p class="text-sm text-metin/65">{e(URUN_ACIKLAMA[ad])}</p>
          </div>
        </article>"""


def madde(metin, koyu=False):
    renk = "text-kirmizi-metin"
    return f'<li class="flex items-start gap-3">{ikon(IKON["tik"], "mt-0.5 size-5 shrink-0 " + renk)}<span>{e(metin)}</span></li>'


SUREC = [
    ("İhtiyaç analizi", "Teknenin kullanım amacını, tüketicilerini ve enerji kaynaklarını birlikte belirliyoruz."),
    ("Projelendirme", "Tek hat şemalarını, pano yerleşimlerini ve kablo güzergâhlarını çiziyoruz."),
    ("Pano imalatı", "Kumanda, sigorta ve alarm panolarını tekneye özel olarak üretiyoruz."),
    ("Montaj ve kablolama", "Altyapıyı kuruyor, cihazları ve panoları yerine bağlıyoruz."),
    ("Test ve devreye alma", "Bütün devreleri tek tek deniyor, sistemi çalışır halde teslim ediyoruz."),
    ("Bakım ve servis", "Teslimden sonra da bakım, onarım ve yenilemelerde yanınızdayız."),
]


def surec_listesi(koyu=False):
    kutu = "border-white/10 bg-white/5" if koyu else "border-cizgi bg-yuzey"
    acik = "text-white/70" if koyu else "text-metin/70"
    out = []
    for i, (b, m) in enumerate(SUREC, 1):
        out.append(f"""<li class="rounded-xl border {kutu} p-6">
          <span class="text-sm font-bold {'text-kirmizi-acik' if koyu else 'text-kirmizi-metin'}">{i:02d}</span>
          <h3 class="mt-2 text-lg font-bold">{e(b)}</h3>
          <p class="mt-1 {acik}">{e(m)}</p>
        </li>""")
    return "\n        ".join(out)


JSONLD = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Electrician",
    "name": "Pozitif Marin Elektrik",
    "legalName": "Pozitif Marin Elektrik Turz. Ltd. Şti.",
    "description": "Denizcilik sektöründe yat ve teknelere elektrik ve elektronik proje, donatım, bakım-onarım ve servis hizmetleri.",
    "foundingDate": "2005",
    "url": "{SITE}/",
    "logo": "{SITE}/assets/img/logo.png",
    "image": "{SITE}/assets/img/bolum/og.jpg",
    "telephone": "{TEL}",
    "faxNumber": "{TEL}",
    "email": "{EPOSTA}",
    "address": {{"@type": "PostalAddress", "streetAddress": "{ADRES1}", "addressLocality": "Tuzla", "addressRegion": "İstanbul", "addressCountry": "TR"}},
    "geo": {{"@type": "GeoCoordinates", "latitude": 40.841085, "longitude": 29.296073}},
    "areaServed": "TR",
    "sameAs": ["{FACEBOOK}"]
  }}
  </script>"""


# ================================================================ SAYFALAR
def sayfa_ana():
    hizmet_kartlari = "\n".join(f"""      <a href="hizmetler.html#{h['id']}" class="group {KART} gap-3 p-7 transition hover:-translate-y-0.5 hover:shadow-md focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kirmizi dark:hover:border-metin/25">
          <span class="grid size-12 place-items-center rounded-lg bg-ters text-ters-metin">{ikon(IKON[h['ikon']])}</span>
          <h3 class="mt-2 text-xl font-bold">{e(h['baslik'])}</h3>
          <p class="text-metin/70">{e(h['kisa'])}</p>
          <span class="mt-auto inline-flex items-center gap-1 pt-3 text-sm font-semibold">Ayrıntılar {ikon(IKON['ok'], 'size-4 transition-transform group-hover:translate-x-0.5')}</span>
      </a>""" for h in HIZMETLER)
    one_cikan = "\n      ".join(galeri_ogesi(k) for k in ["tk013", "kp015", "kksap019", "tk0091", "tk011", "kp004", "aykmdp001", "pj006"])
    markalar = "\n        ".join(f'<li class="inline-flex items-center rounded-full border border-cizgi px-3.5 py-1.5 text-[0.95rem] font-medium">{e(m)}</li>' for m, _ in MARKALAR)
    ornek_ref = ["Numarine Denizcilik", "Kale Endüstri Holding", "Enka İnşaat ve San. A.Ş.", "Teknomar Denizcilik",
                 "Çıpa Marina", "Sanovel İlaç Sanayi", "Labranda Denizcilik", "Ses Yacht"]
    referanslar = "\n          ".join(f'<li class="flex items-center gap-3 border-b border-cizgi py-2.5">{arti("size-2")}{e(r)}</li>' for r in ornek_ref)
    govde = f"""
<section class="relative flex min-h-[82svh] items-center overflow-hidden bg-koyu sm:min-h-[560px] lg:min-h-[600px] xl:min-h-0 xl:aspect-[1920/700]">
  <!-- Her ekran aralığı için kutunun oranına uygun kırpım: mobil 9:16, tablet 4:3, dizüstü 16:10, geniş ekran 2.74:1 -->
  <picture class="absolute inset-0">
    <source media="(min-width: 1280px)" srcset="assets/img/bolum/hero-genis.jpg" width="1920" height="700">
    <source media="(min-width: 1024px)" srcset="assets/img/bolum/hero-orta.jpg" width="1600" height="1000">
    <source media="(min-width: 640px)" srcset="assets/img/bolum/hero-tablet.jpg" width="1200" height="900">
    <img src="assets/img/bolum/hero-mobil.jpg" width="628" height="1117" alt="Pozitif Marin Elektrik: yat elektrik ve elektronik sistemleri" class="h-full w-full object-cover" fetchpriority="high">
  </picture>
  <div class="absolute inset-0 bg-linear-to-t from-koyu via-koyu/75 to-koyu/40 lg:bg-linear-to-r lg:from-koyu lg:via-koyu/85 lg:to-koyu/30"></div>
  <div class="relative z-10 mx-auto w-full max-w-7xl px-4 py-20 lg:px-6 xl:py-14">
    <div class="max-w-2xl text-koyu-metin">
      <p class="mb-5 inline-flex items-center gap-2.5 text-sm font-semibold uppercase tracking-[0.2em] text-white/80">
        {arti()} 2005'ten bu yana · Tuzla, İstanbul
      </p>
      <h1 class="text-4xl font-extrabold leading-[1.1] tracking-tight text-white sm:text-5xl lg:text-6xl">Yatlar için elektrik ve elektronik çözümler</h1>
      <p class="mt-6 max-w-xl text-lg text-white/80 sm:text-xl">Projelendirmeden pano imalatına, kablolama ve donatımdan bakım-onarıma kadar teknenizin tüm elektrik sistemleri tek elden.</p>
      <div class="mt-9 flex flex-col gap-3 sm:flex-row">
        <a href="iletisim.html" class="{dugme('ana', 'lg')}">Bize Ulaşın</a>
        <a href="projeler.html" class="{dugme('acik-kenar', 'lg')}">Projelerimizi İnceleyin</a>
      </div>
    </div>
  </div>
</section>

<section aria-label="Kısaca Pozitif Marin Elektrik" class="border-b border-cizgi bg-zemin">
  <dl class="mx-auto grid max-w-7xl grid-cols-2 gap-px bg-cizgi lg:grid-cols-4">
    <div class="bg-zemin px-6 py-8 text-center"><dt class="text-sm text-metin/60">Kuruluş</dt><dd class="mt-1 text-3xl font-extrabold">2005</dd></div>
    <div class="bg-zemin px-6 py-8 text-center"><dt class="text-sm text-metin/60">Kuruluş öncesi tecrübe</dt><dd class="mt-1 text-3xl font-extrabold">15 yıl</dd></div>
    <div class="bg-zemin px-6 py-8 text-center"><dt class="text-sm text-metin/60">Referans firma</dt><dd class="mt-1 text-3xl font-extrabold">32</dd></div>
    <div class="bg-zemin px-6 py-8 text-center"><dt class="text-sm text-metin/60">İş ortağı &amp; marka</dt><dd class="mt-1 text-3xl font-extrabold">13</dd></div>
  </dl>
</section>

<section class="bg-zemin py-20 lg:py-28">
  <div class="mx-auto grid max-w-7xl items-center gap-12 px-4 lg:grid-cols-2 lg:gap-16 lg:px-6">
    <div>
      {bolum_basligi("Hakkımızda", "Teknolojiyi takip eden, projeye özel çözümler")}
      <div class="mt-6 space-y-4 text-lg leading-relaxed text-metin/75">
        <p>Şirketimiz 15 yıllık tecrübenin ardından, 2005 yılında kuruldu. Denizcilik sektöründe elektrik ve elektronik proje, donatım, bakım-onarım ve servis hizmetleri veriyoruz.</p>
        <p>İlk hedefimiz, kaliteli hizmeti ilke edinip teknolojiyi takip ederek yat elektrik donanımında projeye özel, hızlı ve güvenli çözümler sunmak.</p>
      </div>
      <a href="hakkimizda.html" class="{dugme('ikincil', 'md', 'mt-8')}">Hikayemiz ve çalışma şeklimiz {ikon(IKON['ok'], 'size-4')}</a>
    </div>
    <div class="relative">
      <img src="assets/img/bolum/kokpit.jpg" alt="Donatılan bir yelkenli yatın kokpiti" loading="lazy" width="1024" height="683" class="aspect-[3/2] w-full rounded-xl object-cover shadow-xl">
      <img src="assets/img/bolum/pano.jpg" alt="Tekne silüeti işlenmiş 230V AC ve 24V DC dağıtım panosu" loading="lazy" width="600" height="450" class="absolute -bottom-8 -left-4 hidden aspect-[4/3] w-56 rounded-xl border-4 border-zemin object-cover shadow-xl sm:block lg:-left-10 lg:w-64">
    </div>
  </div>
</section>

<section class="bg-zemin-2 py-20 lg:py-28">
  <div class="mx-auto max-w-7xl px-4 lg:px-6">
    {bolum_basligi("Hizmetlerimiz", "Teknenin elektrik sistemi, baştan sona", "Çizim masasından denize iniş gününe kadar, her aşamada aynı ekip.")}
    <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
{hizmet_kartlari}
    </div>
  </div>
</section>

<section class="bg-zemin py-20 lg:py-28">
  <div class="mx-auto max-w-7xl px-4 lg:px-6">
    <div class="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
      {bolum_basligi("Projelerimiz", "Sahadan kareler", "Teslim ettiğimiz teknelerden, imal ettiğimiz panolardan ve altyapı işlerimizden seçmeler.")}
      <a href="projeler.html" class="{dugme('ikincil', 'md', 'shrink-0')}">Tüm projeler (81 fotoğraf) {ikon(IKON['ok'], 'size-4')}</a>
    </div>
    <div class="mt-10 grid grid-cols-2 gap-3 sm:grid-cols-4 lg:gap-4" data-lightbox>
      {one_cikan}
    </div>
  </div>
</section>

<section class="bg-koyu py-20 text-koyu-metin lg:py-28">
  <div class="mx-auto max-w-7xl px-4 lg:px-6">
    <div class="max-w-2xl">
      <p class="inline-flex items-center gap-2.5 text-sm font-semibold uppercase tracking-[0.2em] text-white/70">{arti()} Çalışma şeklimiz</p>
      <h2 class="mt-3 text-3xl font-extrabold tracking-tight text-white sm:text-4xl">Çizimden teslimata altı adım</h2>
    </div>
    <ol class="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {surec_listesi(koyu=True)}
    </ol>
  </div>
</section>

<section aria-label="Işıklı tekne yazıları" class="bg-zemin">
  <div class="mx-auto grid max-w-7xl items-center gap-10 px-4 py-20 lg:grid-cols-2 lg:gap-16 lg:px-6 lg:py-28">
    <img src="assets/img/bolum/isikli-yazi.jpg" alt="LED arka aydınlatmalı tekne isim yazısı" loading="lazy" width="1200" height="900" class="aspect-[4/3] w-full rounded-xl object-cover shadow-xl lg:order-2">
    <div class="max-w-xl">
      {bolum_basligi("Tekne yazıları", "Teknenizin adı, gece de görünsün")}
      <p class="mt-4 text-lg text-metin/70">LED arka aydınlatmalı ve paslanmaz harf tekne isim yazılarını, teknenin elektrik sistemine uygun şekilde tasarlayıp montajını yapıyoruz.</p>
      <a href="hizmetler.html#tekne-yazilari" class="{dugme('ikincil', 'md', 'mt-8')}">Tekne yazıları {ikon(IKON['ok'], 'size-4')}</a>
    </div>
  </div>
</section>

<section class="border-t border-cizgi bg-zemin py-20 lg:py-28">
  <div class="mx-auto grid max-w-7xl gap-14 px-4 lg:grid-cols-2 lg:gap-20 lg:px-6">
    <div>
      {bolum_basligi("İş ortaklarımız", "Dünya markalarıyla çalışıyoruz", "Satışını ve servisini yaptığımız markalar ile birlikte çalıştığımız tersaneler.")}
      <ul class="mt-8 flex flex-wrap gap-2">
        {markalar}
      </ul>
      <a href="is-ortaklarimiz.html" class="{dugme('ikincil', 'md', 'mt-8')}">Tüm iş ortaklarımız {ikon(IKON['ok'], 'size-4')}</a>
    </div>
    <div>
      {bolum_basligi("Referanslar", "Bize güvenen 32 firma")}
      <ul class="mt-8 grid gap-x-8 sm:grid-cols-2">
          {referanslar}
      </ul>
      <a href="referanslar.html" class="{dugme('ikincil', 'md', 'mt-8')}">Tüm referanslar {ikon(IKON['ok'], 'size-4')}</a>
    </div>
  </div>
</section>
{cta_bandi()}"""
    return (head("index.html", "Pozitif Marin Elektrik | Yat ve Tekne Elektrik-Elektronik Sistemleri · Tuzla, İstanbul",
                 "Pozitif Marin Elektrik, 2005'ten bu yana Tuzla'da yat ve teknelere elektrik-elektronik proje, pano imalatı, donatım, bakım-onarım ve servis hizmeti veriyor.", JSONLD)
            + ust_menu("index.html") + govde + alt_bilgi(pencere=True))


def sayfa_hakkimizda():
    ilkeler = [
        ("Kalite bir ilke", "Kaliteli hizmeti bir hedef değil, işin ön koşulu olarak görüyoruz. Her pano, her bağlantı aynı özenle yapılır."),
        ("Teknolojiyi takip", "Marin elektrik ve elektronik teknolojisi hızla değişiyor; yeni ürünleri ve yöntemleri yakından izliyoruz."),
        ("Projeye özel çözüm", "Hazır kalıplar yerine her teknenin kullanımına ve tüketicilerine göre tasarlanmış sistemler kuruyoruz."),
        ("Hızlı ve güvenli", "Tekne denizde geçirdiği zaman için var. İşi zamanında, güvenlikten taviz vermeden teslim ediyoruz."),
    ]
    ilke_html = "\n        ".join(f"""<div class="rounded-xl border border-cizgi bg-yuzey p-6">
          <h3 class="text-lg font-bold">{e(b)}</h3>
          <p class="mt-2 text-metin/70">{e(m)}</p>
        </div>""" for b, m in ilkeler)
    tekneler = [
        ("assets/img/sayfa/tekne-motor-yat.jpg", 933, 700, "Motor yatlar", "Kaptan köşkü konsolları, seyir ekranları, jeneratör ve sahil elektriği sistemleri."),
        ("assets/img/sayfa/tekne-yelkenli.jpg", 711, 533, "Yelkenli yatlar", "Enerji verimliliğinin öne çıktığı akü, şarj ve dağıtım sistemleri; kokpit panelleri."),
        ("assets/img/sayfa/tekne-klasik.jpg", 1024, 768, "Klasik ve ahşap tekneler", "Teknenin karakterine uygun malzemelerde panolar ve yenilenen elektrik altyapısı."),
    ]
    tekne_html = "\n        ".join(f"""<article class="{KART} overflow-hidden">
          <figure><img src="{s}" alt="{e(b)}" loading="lazy" width="{w}" height="{h}" class="aspect-[4/3] w-full object-cover"></figure>
          <div class="p-6"><h3 class="text-xl font-bold">{e(b)}</h3><p class="mt-2 text-metin/70">{e(m)}</p></div>
        </article>""" for s, w, h, b, m in tekneler)
    govde = sayfa_basligi("Hakkımızda", "2005'ten bu yana", "Hakkımızda",
                          "15 yıllık tecrübenin ardından 2005'te kurulan Pozitif Marin Elektrik, Tuzla'da yat ve teknelerin elektrik ve elektronik sistemleri üzerine çalışıyor.",
                          "assets/img/sayfa/tekne-kusbakisi.jpg", "Kuşbakışı bir yelkenli yat", 800, 600) + f"""

<section class="bg-zemin py-20 lg:py-28">
  <div class="mx-auto grid max-w-7xl gap-12 px-4 lg:grid-cols-5 lg:gap-16 lg:px-6">
    <div class="lg:col-span-3">
      {bolum_basligi("Hikayemiz", "Genç bir firma, köklü bir tecrübe")}
      <div class="mt-6 space-y-4 text-lg leading-relaxed text-metin/75">
        <p>Şirketimiz 15 yıllık tecrübenin ardından, 2005 yılında kurulmuş genç bir firmadır. Denizcilik sektöründe elektrik ve elektronik proje, donatım, bakım-onarım ve servis hizmetleri vermektedir.</p>
        <p>Kurulduğumuz günden bu yana ilk hedefimiz, kaliteli hizmeti ilke edinip teknolojiyi takip ederek yat elektrik donanımında projeye özel, hızlı ve güvenli çözümler sunmaktır.</p>
        <p>Dünyaca ünlü markaların satış ve servis hizmetlerinde gösterdiğimiz performansla sektörde sağlam ve emin adımlarla ilerliyoruz.</p>
        <p>Tuzla'da, Türkiye'nin tersanelerinin yoğunlaştığı bölgede çalışıyoruz. Bir teknenin elektrik sistemini çizim aşamasında planlıyor, panolarını tekneye özel olarak imal ediyor, montajını yapıyor ve teslimden sonra da servisini sürdürüyoruz.</p>
      </div>
    </div>
    <aside class="lg:col-span-2">
      <dl class="grid grid-cols-2 gap-px overflow-hidden rounded-xl border border-cizgi bg-cizgi">
        <div class="bg-yuzey p-6"><dt class="text-sm text-metin/60">Kuruluş</dt><dd class="mt-1 text-3xl font-extrabold">2005</dd></div>
        <div class="bg-yuzey p-6"><dt class="text-sm text-metin/60">Kuruluş öncesi tecrübe</dt><dd class="mt-1 text-3xl font-extrabold">15 yıl</dd></div>
        <div class="bg-yuzey p-6"><dt class="text-sm text-metin/60">Referans firma</dt><dd class="mt-1 text-3xl font-extrabold">32</dd></div>
        <div class="bg-yuzey p-6"><dt class="text-sm text-metin/60">İş ortağı &amp; marka</dt><dd class="mt-1 text-3xl font-extrabold">13</dd></div>
      </dl>
      <div class="mt-6 rounded-xl bg-zemin-2 p-6">
        <h3 class="font-bold">Pozitif Marin Elektrik Turz. Ltd. Şti.</h3>
        <p class="mt-2 text-metin/70">{ADRES1}<br>{ADRES2}</p>
        <a href="iletisim.html" class="hover:underline underline-offset-4 mt-3 inline-flex items-center gap-1 text-sm font-semibold">İletişim bilgileri {ikon(IKON['ok'], 'size-4')}</a>
      </div>
    </aside>
  </div>
</section>

<section class="bg-zemin-2 py-20 lg:py-28">
  <div class="mx-auto max-w-7xl px-4 lg:px-6">
    {bolum_basligi("İlkelerimiz", "Neye önem veriyoruz")}
    <div class="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {ilke_html}
    </div>
  </div>
</section>

<section class="bg-zemin py-20 lg:py-28">
  <div class="mx-auto max-w-7xl px-4 lg:px-6">
    {bolum_basligi("Çalışma şeklimiz", "Çizimden teslimata altı adım", "Bir teknenin elektrik sistemini baştan sona aynı ekip üstlenir; her aşama bir öncekinin üzerine kurulur.")}
    <ol class="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {surec_listesi()}
    </ol>
  </div>
</section>

<section class="bg-zemin-2 py-20 lg:py-28">
  <div class="mx-auto max-w-7xl px-4 lg:px-6">
    {bolum_basligi("Çalıştığımız tekneler", "Motor yattan klasik tekneye")}
    <div class="mt-12 grid gap-6 md:grid-cols-3">
        {tekne_html}
    </div>
  </div>
</section>
{cta_bandi()}"""
    return (head("hakkimizda.html", "Hakkımızda | Pozitif Marin Elektrik",
                 "2005'te 15 yıllık tecrübenin ardından kurulan Pozitif Marin Elektrik'in hikayesi, ilkeleri ve çalışma şekli.")
            + ust_menu("hakkimizda.html") + govde + alt_bilgi())


def sayfa_hizmetler():
    gezinme = "\n        ".join(f'<li><a href="#{h["id"]}" class="{dugme("ikincil", "sm")}">{e(h["baslik"])}</a></li>' for h in HIZMETLER)
    bolumler = []
    for i, h in enumerate(HIZMETLER):
        arka = "bg-zemin" if i % 2 == 0 else "bg-zemin-2"
        sira = "" if i % 2 == 0 else "lg:order-2"
        paragraflar = "\n          ".join(f"<p>{e(p)}</p>" for p in h["metin"])
        kapsam = "\n          ".join(madde(k) for k in h["kapsam"])
        if h["gorseller"]:
            gorsel = f'<div class="grid grid-cols-2 gap-3 {sira}" data-lightbox>\n        ' + "\n        ".join(galeri_ogesi(k, etiket=False) for k in h["gorseller"]) + "\n      </div>"
            link = f'<a href="projeler.html?kategori={h["kategori"]}" class="{dugme("ikincil", "md", "mt-8")}">Bu alandaki tüm projeler {ikon(IKON["ok"], "size-4")}</a>'
        else:
            urunler = ["Jel, AGM ve Stasyoner Aküler", "Marin Uydu Sistemleri", "Akü Şalterleri", "Seyir Fenerleri"]
            gorsel = f'<div class="grid grid-cols-2 gap-3 {sira}">\n        ' + "\n        ".join(
                f'<figure class="aspect-square overflow-hidden rounded-xl border border-cizgi bg-white p-2"><img src="{URUN[u]["img"]}" alt="{e(u)}" loading="lazy" width="640" height="640" class="h-full w-full object-contain"></figure>' for u in urunler) + "\n      </div>"
            link = f'<a href="urunler.html" class="{dugme("ikincil", "md", "mt-8")}">Ürünlerimiz {ikon(IKON["ok"], "size-4")}</a>'
        bolumler.append(f"""
<section id="{h['id']}" class="{arka} py-20 lg:py-24">
  <div class="mx-auto grid max-w-7xl items-center gap-12 px-4 lg:grid-cols-2 lg:gap-16 lg:px-6">
    <div>
      <span class="grid size-12 place-items-center rounded-lg bg-ters text-ters-metin">{ikon(IKON[h['ikon']])}</span>
      <h2 class="mt-5 text-3xl font-extrabold tracking-tight sm:text-4xl">{e(h['baslik'])}</h2>
      <div class="mt-5 space-y-4 text-lg leading-relaxed text-metin/75">
          {paragraflar}
      </div>
      <h3 class="mt-8 text-sm font-semibold uppercase tracking-[0.15em] text-metin/60">Kapsam</h3>
      <ul class="mt-4 grid gap-3 sm:grid-cols-2">
          {kapsam}
      </ul>
      {link}
    </div>
      {gorsel}
  </div>
</section>""")
    govde = sayfa_basligi("Hizmetler", "Hizmetlerimiz", "Teknenin elektrik sistemi, baştan sona",
                          "Projelendirme, pano imalatı, kablolama, ışıklı yazılar, ürün temini ve servis: hepsi aynı ekipten.",
                          "assets/img/sayfa/hizmetler.jpg", "Tekne silüeti işlenmiş AC ve DC dağıtım panosu", 1200, 900) + f"""
<nav aria-label="Hizmetler" class="sticky top-16 z-40 border-b border-cizgi bg-zemin/95 backdrop-blur">
  <ul class="mx-auto flex max-w-7xl gap-2 overflow-x-auto px-4 py-3 lg:px-6">
        {gezinme}
  </ul>
</nav>
{''.join(bolumler)}
{cta_bandi()}"""
    return (head("hizmetler.html", "Hizmetler | Pozitif Marin Elektrik",
                 "Yat ve teknelere elektrik projelendirme, kumanda panelleri, sigorta ve alarm panoları, kablolama, ışıklı tekne yazıları, ürün satışı ve servis.")
            + ust_menu("hizmetler.html") + govde + alt_bilgi(pencere=True))


FILTRE = ("inline-flex cursor-pointer items-center gap-1.5 whitespace-nowrap rounded-full border border-cizgi bg-yuzey px-4 py-2 "
          "text-sm font-medium text-metin/75 transition-colors hover:border-metin/30 hover:text-metin " + ODAK + " "
          "aria-pressed:border-ters aria-pressed:bg-ters aria-pressed:text-ters-metin")

# Galeri gruplarının kısa açıklaması ve ilgili hizmet bölümü (hizmetler.html#...)
GRUP_ACIKLAMA = {"teslim-edilen-projeler": ("Elektrik ve elektronik sistemlerini kurup teslim ettiğimiz teknelerden.", None)}
GRUP_ACIKLAMA.update({h["kategori"]: (h["kisa"], h["id"]) for h in HIZMETLER if h["kategori"]})


def sayfa_projeler():
    by = {eski: [g for g in VERI["galeri"] if g["kategori"] == eski] for _, _, eski in KATEGORI}
    toplam = len(VERI["galeri"])
    filtreler = [f'<button type="button" class="{FILTRE}" aria-pressed="true" data-filtre="hepsi">Tümü <span class="text-xs opacity-60">{toplam}</span></button>']
    filtreler += [f'<button type="button" class="{FILTRE}" aria-pressed="false" data-filtre="{slug}">{e(ad)} <span class="text-xs opacity-60">{len(by[eski])}</span></button>'
                  for slug, ad, eski in KATEGORI]
    gruplar = []
    for slug, ad, eski in KATEGORI:
        aciklama, hizmet = GRUP_ACIKLAMA[slug]
        bag = (f'<a href="hizmetler.html#{hizmet}" class="inline-flex items-center gap-1 font-semibold text-kirmizi-metin underline-offset-4 hover:underline">'
               f'Hizmet ayrıntıları {ikon(IKON["ok"], "size-4")}</a>') if hizmet else ""
        ogeler = "\n        ".join(yasli_oge(g) for g in by[eski])
        gruplar.append(f"""
    <section data-grup="{slug}" aria-labelledby="grup-{slug}" class="pt-10 first:pt-0">
      <div class="mb-5 flex flex-col gap-3 border-b border-cizgi pb-4 sm:flex-row sm:items-end sm:justify-between sm:gap-8">
        <div class="max-w-2xl">
          <h2 id="grup-{slug}" class="flex items-baseline gap-3 text-2xl font-extrabold tracking-tight">{e(ad)} <span class="text-sm font-medium text-metin/60">{len(by[eski])} fotoğraf</span></h2>
          <p class="mt-1 text-metin/70">{e(aciklama)}</p>
        </div>
        {bag}
      </div>
      <div class="flex flex-wrap items-start gap-2 [--rh:8.5rem] after:grow-[999] after:content-[''] sm:[--rh:11rem] lg:[--rh:14rem]">
        {ogeler}
      </div>
    </section>""")
    govde = sayfa_basligi("Projeler", "Projelerimiz", "Sahadan kareler",
                          "Teslim ettiğimiz teknelerden, imal ettiğimiz kumanda ve dağıtım panolarından, altyapı işlerimizden ve proje çizimlerimizden 81 fotoğraf.",
                          "assets/img/sayfa/projeler.jpg", "Seyir halinde bir yelkenli yat", 711, 533) + f"""

<div class="sticky top-16 z-40 border-b border-cizgi bg-zemin/95 backdrop-blur">
  <div class="mx-auto max-w-7xl overflow-x-auto px-4 [scrollbar-width:none] lg:px-6 [&::-webkit-scrollbar]:hidden" data-filtre-kaydir>
    <div role="group" aria-label="Proje kategorileri" class="flex w-max gap-2 py-3">
      {chr(10).join('      ' + f for f in filtreler).strip()}
    </div>
  </div>
</div>

<section aria-label="Proje fotoğrafları" class="bg-zemin py-10 lg:py-14">
  <div class="mx-auto max-w-7xl scroll-mt-36 px-4 lg:px-6" data-lightbox data-galeri>
    <p class="mb-8 flex items-center gap-2 text-sm text-metin/60">{ikon(IKON["buyut"], "size-4 shrink-0")} Fotoğrafa dokunarak büyütün; büyük görünümde kaydırarak gezinebilir, iki parmakla yakınlaştırabilirsiniz.</p>
    {"".join(gruplar)}
  </div>
</section>
{cta_bandi()}"""
    return (head("projeler.html", "Projeler | Pozitif Marin Elektrik",
                 "Teslim edilen tekneler, kumanda panelleri, sigorta ve alarm panoları, altyapı işleri, ışıklı tekne yazıları ve proje çizimlerinden 81 fotoğraf.")
            + ust_menu("projeler.html") + govde + alt_bilgi(pencere=True))


def sayfa_urunler():
    gezinme = "\n        ".join(f'<li><a href="#{gid}" class="{dugme("ikincil", "sm")}">{e(ad)}</a></li>' for gid, ad, _, _ in URUN_GRUPLARI)
    gruplar = []
    for i, (gid, ad, aciklama, liste) in enumerate(URUN_GRUPLARI):
        arka = "bg-zemin-2" if i % 2 == 0 else "bg-zemin"
        kartlar = "\n        ".join(urun_karti(u) for u in liste)
        gruplar.append(f"""
<section id="{gid}" class="{arka} py-16 lg:py-20">
  <div class="mx-auto max-w-7xl px-4 lg:px-6">
    <div class="max-w-2xl">
      <h2 class="text-2xl font-extrabold tracking-tight sm:text-3xl">{e(ad)}</h2>
      <p class="mt-3 text-lg text-metin/70">{e(aciklama)}</p>
    </div>
    <div class="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
        {kartlar}
    </div>
  </div>
</section>""")
    govde = sayfa_basligi("Ürünler", "Ürünlerimiz", "Satışını ve servisini yaptığımız ürünler",
                          "Enerji, dağıtım, seyir ve konfor ekipmanları. Ürün seçimi, montajı ve devreye alınması bizden.",
                          "assets/img/sayfa/urunler.jpg", "Bir yelkenli yatın dümen konsolu ve seyir cihazları", 911, 683) + f"""
<nav aria-label="Ürün grupları" class="border-b border-cizgi bg-zemin">
  <ul class="mx-auto flex max-w-7xl gap-2 overflow-x-auto px-4 py-3 lg:px-6">
        {gezinme}
  </ul>
</nav>
{''.join(gruplar)}

<section class="bg-zemin py-16">
  <div class="mx-auto max-w-7xl px-4 lg:px-6">
    <div class="rounded-xl border border-cizgi p-8 lg:flex lg:items-center lg:justify-between lg:gap-10">
      <div class="max-w-2xl">
        <h2 class="text-2xl font-extrabold tracking-tight">Doğru ürünü birlikte seçelim</h2>
        <p class="mt-2 text-lg text-metin/70">Mastervolt, Intellian, Marine Air Systems, Cruisair ve Horizon Reverse Osmosis gibi iş ortaklarımızın ürünlerini teknenizin sistemine uygun şekilde öneriyor, montajını ve servisini yapıyoruz.</p>
      </div>
      <a href="is-ortaklarimiz.html" class="{dugme('ikincil', 'md', 'mt-6 shrink-0 lg:mt-0')}">İş ortaklarımız {ikon(IKON['ok'], 'size-4')}</a>
    </div>
  </div>
</section>
{cta_bandi()}"""
    return (head("urunler.html", "Ürünler | Pozitif Marin Elektrik",
                 "Aküler, şarj cihazları, invertörler, sigortalar, şalterler, seyir fenerleri, baş pervaneleri, uydu sistemleri, su yapıcılar ve marin klimalar.")
            + ust_menu("urunler.html") + govde + alt_bilgi())


def sayfa_is_ortaklari():
    def liste(veri):
        return "\n          ".join(f"""<li class="flex flex-col gap-0.5 border-b border-cizgi py-4 sm:flex-row sm:items-baseline sm:justify-between sm:gap-6">
            <span class="text-lg font-bold">{e(a)}</span>{f'<span class="text-metin/65 sm:text-right">{e(d)}</span>' if d else ''}
          </li>""" for a, d in veri)
    govde = sayfa_basligi("İş Ortaklarımız", "İş ortaklarımız", "Birlikte çalıştığımız markalar ve tersaneler",
                          "Satışını ve servisini yaptığımız dünya markaları ile projelerinde yer aldığımız tekne üreticileri.",
                          "assets/img/sayfa/is-ortaklarimiz.jpg", "Rüzgârla yatan bir yelkenli yat", 709, 532) + f"""

<section class="bg-zemin py-20 lg:py-24">
  <div class="mx-auto max-w-7xl px-4 lg:px-6">
    <figure class="mx-auto max-w-5xl rounded-xl border border-cizgi bg-white p-4 sm:p-8">
      <img src="assets/img/is-ortaklari.jpg" alt="İş ortaklarımızın logoları: Mastervolt, Intellian, Tecma by Thetford, Atlas Marine Systems, Mert Yacht, Marine Air Systems, Horizon Reverse Osmosis, Cruisair, Marina Deniz Araçları, Rodriquez, Ses Yachts, Artı Marin ve Max" loading="lazy" width="1158" height="458" class="mx-auto w-full">
    </figure>
    <div class="mt-16 grid gap-14 lg:grid-cols-2 lg:gap-20">
      <div>
        <h2 class="text-2xl font-extrabold tracking-tight sm:text-3xl">Ürün markaları</h2>
        <p class="mt-3 text-lg text-metin/70">Satışını, montajını ve servisini yaptığımız markalar.</p>
        <ul class="mt-6">
          {liste(MARKALAR)}
        </ul>
      </div>
      <div>
        <h2 class="text-2xl font-extrabold tracking-tight sm:text-3xl">Tersaneler ve üreticiler</h2>
        <p class="mt-3 text-lg text-metin/70">Teknelerinin elektrik sistemlerinde birlikte çalıştığımız üreticiler.</p>
        <ul class="mt-6">
          {liste(TERSANELER)}
        </ul>
        <a href="urunler.html" class="{dugme('ikincil', 'md', 'mt-10')}">Ürünlerimiz {ikon(IKON['ok'], 'size-4')}</a>
      </div>
    </div>
  </div>
</section>
{cta_bandi()}"""
    return (head("is-ortaklarimiz.html", "İş Ortaklarımız | Pozitif Marin Elektrik",
                 "Mastervolt, Intellian, Tecma, Atlas Marine Systems, Marine Air Systems, Cruisair, Horizon Reverse Osmosis ve birlikte çalıştığımız tersaneler.")
            + ust_menu("is-ortaklarimiz.html") + govde + alt_bilgi())


def sayfa_referanslar():
    gruplar = "\n      ".join(f"""<div>
        <h2 class="flex items-baseline gap-3 text-xl font-extrabold tracking-tight">{e(ad)} <span class="text-sm font-medium text-metin/60">{len(l)} firma</span></h2>
        <ul class="mt-4">
          {chr(10).join('          <li class="flex items-center gap-3 border-b border-cizgi py-2.5">' + arti("size-2") + e(r) + '</li>' for r in l)}
        </ul>
      </div>""" for ad, l in REFERANS_GRUPLARI)
    govde = sayfa_basligi("Referanslar", "Referanslarımız", "Bize güvenen firmalar",
                          "Denizcilikten sanayiye, turizmden sağlığa farklı alanlardan 32 firmayla çalıştık.",
                          "assets/img/sayfa/referanslar.jpg", "Callista adlı yelkenli yat seyir halinde", 933, 700) + f"""

<section class="bg-zemin py-20 lg:py-24">
  <div class="mx-auto grid max-w-7xl gap-12 px-4 md:grid-cols-2 lg:grid-cols-3 lg:px-6">
      {gruplar}
  </div>
</section>

<section class="bg-koyu text-koyu-metin">
  <div class="mx-auto grid max-w-7xl items-center gap-10 px-4 py-16 lg:grid-cols-2 lg:gap-16 lg:px-6 lg:py-20">
    <img src="assets/img/bolum/callista-genis.jpg" alt="Callista adlı yelkenli yat" loading="lazy" width="1050" height="700" class="aspect-[3/2] w-full rounded-xl object-cover shadow-2xl lg:order-2">
    <div class="max-w-2xl">
      <h2 class="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">Yaptığımız işleri görün</h2>
      <p class="mt-4 text-lg text-white/75">Teslim ettiğimiz teknelerden ve imal ettiğimiz panolardan fotoğraflar.</p>
      <a href="projeler.html" class="{dugme('acik-kenar', 'md', 'mt-8')}">Projelerimiz {ikon(IKON['ok'], 'size-4')}</a>
    </div>
  </div>
</section>
{cta_bandi()}"""
    return (head("referanslar.html", "Referanslar | Pozitif Marin Elektrik",
                 "Denizcilik, sanayi, inşaat, turizm ve sağlık alanlarından Pozitif Marin Elektrik'e güvenen 32 firma.")
            + ust_menu("referanslar.html") + govde + alt_bilgi())


def sayfa_iletisim():
    def kart(href, ik, ust, deger, ek=""):
        etiket = "a" if href else "div"
        h = f' href="{href}"' if href else ""
        hover = " transition hover:border-metin/30" if href else ""
        return f"""<{etiket}{h} class="flex rounded-xl border border-cizgi bg-yuzey{hover}">
          <div class="flex items-start gap-4 p-5">
            <span class="grid size-12 shrink-0 place-items-center rounded-full bg-zemin-2">{ikon(IKON[ik], 'size-5')}</span>
            <span><span class="block text-sm text-metin/60">{ust}</span><span class="block text-lg font-semibold">{deger}</span>{ek}</span>
          </div>
        </{etiket}>"""
    yol = f'<a href="https://www.google.com/maps/dir/?api=1&amp;destination={HARITA}" target="_blank" rel="noopener" class="hover:underline underline-offset-4 mt-1 inline-block text-sm font-medium text-mavi-metin">Yol tarifi al →</a>'
    govde = sayfa_basligi("İletişim", "İletişim", "Projenizi konuşalım",
                          "Arayın, e-posta gönderin ya da Tuzla'daki adresimize uğrayın.",
                          "assets/img/sayfa/iletisim.jpg", "Bir yatın kaptan köşkündeki seyir ekranları", 933, 700) + f"""

<section class="bg-zemin py-20 lg:py-24">
  <div class="mx-auto max-w-7xl px-4 lg:px-6">
    <div class="grid gap-8 lg:grid-cols-5">
      <div class="space-y-4 lg:col-span-2">
        {kart(TEL_HREF, "tel", "Telefon &amp; Faks", TEL)}
        {kart(CEP_HREF, "cep", "Cep", CEP)}
        {kart("mailto:" + EPOSTA, "posta", "E-posta", EPOSTA)}
        {kart("", "konum", "Adres", f'<address class="not-italic">{ADRES1}<br>{ADRES2}</address>', yol)}
        <a href="{FACEBOOK}" target="_blank" rel="noopener" class="{dugme('hayalet', 'md', 'justify-start gap-3')}">{FB_SVG} Facebook'ta takip edin</a>
      </div>
      <div class="flex flex-col gap-6 lg:col-span-3">
        <div class="overflow-hidden rounded-xl border border-cizgi bg-zemin-2">
          <iframe title="Pozitif Marin Elektrik konumu - Tuzla, İstanbul" src="https://maps.google.com/maps?q={HARITA}&amp;hl=tr&amp;z=16&amp;output=embed" class="block aspect-[4/3] w-full sm:aspect-[16/10]" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        </div>
        <div class="rounded-xl border border-cizgi bg-zemin-2">
          <div class="p-6">
            <h2 class="text-lg font-bold">Fatura bilgileri</h2>
            <dl class="mt-2 grid gap-x-6 gap-y-3 text-sm sm:grid-cols-[auto_1fr]">
              <dt class="text-metin/60">Unvan</dt><dd class="font-medium">Pozitif Marin Elektrik Turz. Ltd. Şti.</dd>
              <dt class="text-metin/60">Adres</dt><dd class="font-medium">{ADRES1} Tuzla - İstanbul</dd>
              <dt class="text-metin/60">Vergi dairesi / No</dt><dd class="font-medium">Tuzla V.D. · 733 036 0072</dd>
              <dt class="text-metin/60">IBAN</dt>
              <dd class="flex flex-wrap items-center gap-3 font-medium">
                <span class="font-mono tracking-wide" data-iban>TR40 0004 6002 3888 8000 0842 29</span>
                <button type="button" class="{dugme('ikincil', 'xs')}" data-kopyala="TR400004600238888000084229">Kopyala</button>
              </dd>
            </dl>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""
    return (head("iletisim.html", "İletişim | Pozitif Marin Elektrik",
                 "Pozitif Marin Elektrik iletişim bilgileri: +90 216 395 99 44, info@pozitifelektrik.org, Aydıntepe Mah. Emek Sok. No: 13/A Tuzla / İstanbul.", JSONLD)
            + ust_menu("iletisim.html") + govde + alt_bilgi(bildirim=True))


def sayfa_404():
    govde = f"""
<section class="bg-zemin py-28">
  <div class="mx-auto max-w-2xl px-4 text-center">
    {logo("mx-auto size-16 text-[#0f172a] dark:text-white", kaynak=AMBLEM_SVG)}
    <p class="mt-8 text-sm font-semibold uppercase tracking-[0.2em] text-kirmizi-metin">404</p>
    <h1 class="mt-3 text-4xl font-extrabold tracking-tight sm:text-5xl">Aradığınız sayfa bulunamadı</h1>
    <p class="mt-5 text-lg text-metin/70">Adres değişmiş ya da sayfa kaldırılmış olabilir.</p>
    <div class="mt-9 flex flex-col justify-center gap-3 sm:flex-row">
      <a href="index.html" class="{dugme('ters')}">Ana sayfaya dön</a>
      <a href="iletisim.html" class="{dugme('ikincil')}">İletişim</a>
    </div>
  </div>
</section>"""
    return (head("404.html", "Sayfa bulunamadı | Pozitif Marin Elektrik", "Aradığınız sayfa bulunamadı.")
            .replace('<meta name="theme-color"', '<meta name="robots" content="noindex">\n  <meta name="theme-color"')
            + ust_menu("") + govde + alt_bilgi())


SAYFALAR = {
    "index.html": sayfa_ana, "hakkimizda.html": sayfa_hakkimizda, "hizmetler.html": sayfa_hizmetler,
    "projeler.html": sayfa_projeler, "urunler.html": sayfa_urunler, "is-ortaklarimiz.html": sayfa_is_ortaklari,
    "referanslar.html": sayfa_referanslar, "iletisim.html": sayfa_iletisim, "404.html": sayfa_404,
}

if __name__ == "__main__":
    for ad, f in SAYFALAR.items():
        with open(os.path.join(CIKTI, ad), "w", encoding="utf-8") as fh:
            fh.write(f())
        print(f"yazıldı: {ad}")
    harita = "\n".join(f"  <url><loc>{SITE}/{'' if s == 'index.html' else s[:-5]}</loc><lastmod>2026-11-09</lastmod></url>"
                       for s in SAYFALAR if s != "404.html")
    with open(os.path.join(CIKTI, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{harita}\n</urlset>\n')
    print("yazıldı: sitemap.xml")
