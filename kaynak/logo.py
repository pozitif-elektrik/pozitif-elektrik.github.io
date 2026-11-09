#!/usr/bin/env python3
"""Pozitif Marin Elektrik — vektörel logo üretici.

Proje kökünde çalıştırın:   python3 kaynak/logo.py
Çıktı:  logo/svg  (ana dosyalar)   logo/png  logo/pdf  (rsvg-convert ile)

Harfler bir yazı tipi dosyasından gelmez; aşağıdaki çizgi iskeletlerinden
çizilir. Bu yüzden lisans sorunu yoktur ve logo her yerde aynı görünür.
Çıktıdaki harfler çizgi değil, dolgulu şekildir (anahatta dönüştürülmüş):
iskelet bir kez yüksek çözünürlükte çizilip kenarı vektör çokgene çevrilir
ve kaynak/logo-anahat.json'da saklanır. İskelet değişirse kendiliğinden
yeniden hesaplanır. Tek renk sürümlerde harfler kutucuktan aynı yol içinde
oyulur (maske yok), bu yüzden PDF'ler saf vektördür.

Logonun fikri eski logodan gelir: her harf koyu bir kutucukta, kırmızı artı
hem pozitif kutbu (+) hem de POZİ✚İF / ELEK✚RİK'teki T harflerini taşır.
"""
import hashlib
import io
import json
import os
import shutil
import subprocess
from collections import defaultdict

from PIL import Image, ImageChops, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIKTI = os.path.join(KOK, "logo")
ANAHAT_DOSYA = os.path.join(KOK, "kaynak", "logo-anahat.json")
RSVG = shutil.which("rsvg-convert")

KIRMIZI = "#E30613"   # eski logodaki saf kırmızının (#FA0203) baskıya uygun hali
SIYAH = "#111111"
LACIVERT = "#0F172A"  # sitenin koyu rengi
BEYAZ = "#FFFFFF"


# ---------------------------------------------------------------- harfler
# Her harf 100 x 120 birimlik kutuda çizilir (yükseklik = büyük harf boyu).
# Değer: (çizgi yolu, nokta)  nokta = (cx, cy, r) yalnızca İ için.

def _o_harfi(i):
    """Oval O: iki yarım daire + düz kenarlar. i = çizgi yarı kalınlığı."""
    r = 50 - i
    return (f"M50,{i} A{r},{r} 0 0 1 {100 - i},{i + r} V{120 - i - r} "
            f"A{r},{r} 0 0 1 50,{120 - i} A{r},{r} 0 0 1 {i},{120 - i - r} "
            f"V{i + r} A{r},{r} 0 0 1 50,{i} Z")


# A önerisi: eski logodaki daktilo harfinin (kalın, ayaklı) temiz çizimi
DAKTILO = {
    "ad": "daktilo",
    "cizgi": 19, "uc": "butt", "kose": "miter",
    "harfler": {
        "P": ("M25,9 V111 M9,111 H55 M9,9 H62 A28.5,28.5 0 0 1 62,66 H25", None),
        "O": (_o_harfi(9), None),
        "Z": ("M12,34 V9 H88 L12,111 H88 V86", None),
        "I": ("M20,9 H80 M50,9 V111 M20,111 H80", None),
        "F": ("M9,9 H88 V36 M30,9 V111 M9,111 H62 M30,58 H64 M64,42 V74", None),
        "E": ("M9,9 H88 V36 M30,9 V111 M9,111 H90 V84 M30,58 H64 M64,42 V74", None),
        "L": ("M9,9 H58 M30,9 V111 M9,111 H90 V80", None),
        "K": ("M9,9 H54 M30,9 V111 M9,111 H54 M30,72 L78,9 M62,9 H92 "
              "M46,51 L82,111 M66,111 H92", None),
        "R": ("M9,9 H60 A27,27 0 0 1 60,63 H30 M30,9 V111 M9,111 H54 "
              "M52,63 L80,111 M68,111 H92", None),
    },
}

# B ve C önerileri: pano etiketlerindeki gravür yazısını andıran tek çizgi harf
GRAVUR = {
    "ad": "gravur",
    "cizgi": 16.5, "uc": "round", "kose": "round",
    "harfler": {
        "P": ("M22,112 V8 H58 A27,27 0 0 1 58,62 H22", None),
        "O": (_o_harfi(8), None),
        "Z": ("M14,8 H86 L14,112 H86", None),
        "I": ("M30,8 H70 M50,8 V112 M30,112 H70", None),
        "İ": ("M30,8 H70 M50,8 V112 M30,112 H70", (50, -21, 10.5)),
        "F": ("M86,8 H22 V112 M22,58 H70", None),
        "E": ("M86,8 H22 V112 H86 M22,58 H72", None),
        "L": ("M22,8 V112 H86", None),
        "K": ("M22,8 V112 M82,8 L22,74 M45,49 L84,112", None),
        "R": ("M22,112 V8 H58 A27,27 0 0 1 58,62 H22 M50,62 L84,112", None),
        "T": ("M12,8 H88 M50,8 V112", None),
        "M": ("M14,112 V8 L50,78 L86,8 V112", None),
        "A": ("M10,112 L50,8 L90,112 M24,76 H76", None),
        "N": ("M18,112 V8 L82,112 V8", None),
        " ": ("", None),
    },
}


def _iskelet_svg(yazi, ch):
    """Harfin çizgi iskeleti (yalnızca anahat çıkarmak için)."""
    yol, nokta = yazi["harfler"][ch]
    out = ""
    if yol:
        out += (f'<path d="{yol}" fill="none" stroke="#000" stroke-width="{yazi["cizgi"]}" '
                f'stroke-linecap="{yazi["uc"]}" stroke-linejoin="{yazi["kose"]}" '
                f'stroke-miterlimit="2"/>')
    if nokta:
        cx, cy, r = nokta
        out += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#000"/>'
    return out


def _sadelestir(noktalar, eps):
    """Ramer–Douglas–Peucker (açık çizgi)."""
    if len(noktalar) < 3:
        return noktalar
    tut = [False] * len(noktalar)
    tut[0] = tut[-1] = True
    yigin = [(0, len(noktalar) - 1)]
    while yigin:
        a, b = yigin.pop()
        (x1, y1), (x2, y2) = noktalar[a], noktalar[b]
        dx, dy = x2 - x1, y2 - y1
        uz = (dx * dx + dy * dy) ** 0.5 or 1e-12
        en, idx = -1.0, -1
        for i in range(a + 1, b):
            px, py = noktalar[i]
            d = abs(dy * (px - x1) - dx * (py - y1)) / uz
            if d > en:
                en, idx = d, i
        if en > eps:
            tut[idx] = True
            yigin += [(a, idx), (idx, b)]
    return [p for p, t in zip(noktalar, tut) if t]


def _iz_cikar(yazi, ch, olcek=20, eps=0.012):
    """İskeleti yüksek çözünürlükte çizip kenarını (marching squares) çokgene çevirir.
    Dönüş: [[[x, y], ...], ...]  — 100 x 120 harf kutusu biriminde kapalı halkalar."""
    X0, Y0, GW, GH = -15, -45, 130, 180
    metin = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{X0} {Y0} {GW} {GH}" '
             f'width="{GW * olcek}" height="{GH * olcek}"><rect x="{X0}" y="{Y0}" '
             f'width="{GW}" height="{GH}" fill="#fff"/>{_iskelet_svg(yazi, ch)}</svg>')
    png = subprocess.run([RSVG], input=metin.encode(), capture_output=True, check=True).stdout
    img = Image.open(io.BytesIO(png)).convert("L")
    W, H = img.size
    px = img.tobytes()
    esik = img.point(lambda v: 255 if v < 128 else 0)
    kenar = ImageChops.difference(esik.filter(ImageFilter.MaxFilter(3)),
                                  esik.filter(ImageFilter.MinFilter(3))).tobytes()
    hucreler = set()
    i = kenar.find(b"\xff")
    while i != -1:
        y, x = divmod(i, W)
        hucreler.update(((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y)))
        i = kenar.find(b"\xff", i + 1)

    iso = 127.5
    komsu, nokta = defaultdict(list), {}

    def bagla(a, b):
        komsu[a].append(b)
        komsu[b].append(a)

    for x, y in hucreler:
        if x < 0 or y < 0 or x >= W - 1 or y >= H - 1:
            continue
        a, b = px[y * W + x], px[y * W + x + 1]
        c, d = px[(y + 1) * W + x + 1], px[(y + 1) * W + x]
        ia, ib, ic, id_ = a < iso, b < iso, c < iso, d < iso
        if ia == ib == ic == id_:
            continue
        k = {}
        if ia != ib:
            k["t"] = ("h", x, y); nokta[k["t"]] = (x + (iso - a) / (b - a), y)
        if ib != ic:
            k["r"] = ("v", x + 1, y); nokta[k["r"]] = (x + 1, y + (iso - b) / (c - b))
        if id_ != ic:
            k["b"] = ("h", x, y + 1); nokta[k["b"]] = (x + (iso - d) / (c - d), y + 1)
        if ia != id_:
            k["l"] = ("v", x, y); nokta[k["l"]] = (x, y + (iso - a) / (d - a))
        if len(k) == 2:
            bagla(*k.values())
        else:  # eyer noktası: merkezle aynı durumda olmayan köşeleri ayır
            orta = (a + b + c + d) / 4 < iso
            for kose, (p, q) in ((ia, "tl"), (ib, "tr"), (ic, "rb"), (id_, "bl")):
                if kose != orta:
                    bagla(k[p], k[q])

    halkalar, gorulen = [], set()
    for bas in komsu:
        if bas in gorulen:
            continue
        halka, onceki, simdi = [bas], None, bas
        gorulen.add(bas)
        while True:
            n0, n1 = komsu[simdi][0], komsu[simdi][-1]
            sonraki = n1 if n0 == onceki else n0
            if sonraki == bas or sonraki in gorulen:
                break
            halka.append(sonraki)
            gorulen.add(sonraki)
            onceki, simdi = simdi, sonraki
        if len(halka) < 8:
            continue
        pts = [(X0 + (nokta[k][0] + 0.5) / olcek, Y0 + (nokta[k][1] + 0.5) / olcek) for k in halka]
        # kapalı halkayı en uzak iki noktadan bölüp iki yarıyı sadeleştir
        uzak = max(range(len(pts)), key=lambda j: (pts[j][0] - pts[0][0]) ** 2 + (pts[j][1] - pts[0][1]) ** 2)
        s1 = _sadelestir(pts[: uzak + 1], eps)
        s2 = _sadelestir(pts[uzak:] + [pts[0]], eps)
        halkalar.append([[round(px_, 3), round(py_, 3)] for px_, py_ in s1[:-1] + s2[:-1]])
    return halkalar


_ANAHAT = None


def anahat(yazi, ch):
    """Harfin dolgulu dış hattı (önbellekli)."""
    global _ANAHAT
    if _ANAHAT is None:
        try:
            with open(ANAHAT_DOSYA, encoding="utf-8") as f:
                _ANAHAT = json.load(f)
        except FileNotFoundError:
            _ANAHAT = {}
    yol, nokta = yazi["harfler"][ch]
    if not yol and not nokta:
        return []
    imza = hashlib.sha1(repr((yol, nokta, yazi["cizgi"], yazi["uc"], yazi["kose"])).encode()).hexdigest()[:12]
    anahtar = f'{yazi["ad"]}:{ch}:{imza}'
    if anahtar not in _ANAHAT:
        _ANAHAT[anahtar] = _iz_cikar(yazi, ch)
    return _ANAHAT[anahtar]


def _anahat_kaydet():
    if _ANAHAT is not None:
        with open(ANAHAT_DOSYA, "w", encoding="utf-8") as f:
            json.dump(_ANAHAT, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def harf_yolu(yazi, ch, x, y, k):
    """Harfin, (x, y) konumuna k ölçeğiyle yerleştirilmiş SVG yol verisi."""
    return " ".join("M" + " ".join(f"{px * k + x:.2f},{py * k + y:.2f}" for px, py in h) + "Z"
                    for h in anahat(yazi, ch))


def harf(yazi, ch, x, y, k, renk):
    d = harf_yolu(yazi, ch, x, y, k)
    return f'<path d="{d}" fill="{renk}" fill-rule="evenodd"/>' if d else ""


def harf_cizgi(yazi, ch, x, y, k, renk):
    """Harfin çizgi hali (web sitesi için). Dolgulu anahat bu çizgiden çıkarıldığı
    için ekranda aynı görünür, dosya ise ~20 kat küçük olur. Çizgi kalınlığı ve
    uçlar, çağıran <g> öğesinden gelir."""
    yol, nokta = yazi["harfler"][ch]
    ic = f'<path d="{yol}"/>' if yol else ""
    if nokta:
        cx, cy, r = nokta
        ic += f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{renk}" stroke="none"/>'
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({k:g})">{ic}</g>' if ic else ""


def kutu(x, y, w, h, rx, renk):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" fill="{renk}"/>'


def kutu_yolu(x, y, w, h, r):
    """Yuvarlak köşeli dikdörtgen, yol verisi olarak (oyma için)."""
    return (f"M{x + r:g},{y:g}H{x + w - r:g}A{r:g},{r:g} 0 0 1 {x + w:g},{y + r:g}"
            f"V{y + h - r:g}A{r:g},{r:g} 0 0 1 {x + w - r:g},{y + h:g}H{x + r:g}"
            f"A{r:g},{r:g} 0 0 1 {x:g},{y + h - r:g}V{y + r:g}A{r:g},{r:g} 0 0 1 {x + r:g},{y:g}Z")


def svg(w, h, govde, baslik):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
            f'width="{w:g}" height="{h:g}">\n<title>{baslik}</title>\n{govde}\n</svg>\n')


# ---------------------------------------------------------------- kutucuklu logo (A, B)
def kutucuklu(yazi, satirlar, g, p):
    """satirlar: [(sol, sag), (sol, sag)] — artının solundaki ve sağındaki harfler.
    p: renkler {karo, harf, arti, oyuk}. oyuk=True ise harfler kutucuktan oyulur
    (tek renk baskı, kesim, gravür için)."""
    TW, TH, ARA, ACIK, ARTI = g["TW"], g["TH"], g["ARA"], g["ACIK"], g["ARTI"]
    nsol = max(len(s) for s, _ in satirlar)
    nsag = max(len(r) for _, r in satirlar)
    arti_x = nsol * TW + (nsol - 1) * ARA + ACIK
    sag_x = arti_x + ARTI + ACIK
    W = sag_x + nsag * TW + (nsag - 1) * ARA
    y2 = TH + ACIK + ARTI + ACIK
    H = y2 + TH
    arti_y = TH + ACIK

    karolar, harfler = [], []
    for r, (sol, sag) in enumerate(satirlar):
        y = 0 if r == 0 else y2
        konumlar = [(i * (TW + ARA), ch) for i, ch in enumerate(sol)]
        konumlar += [(sag_x + j * (TW + ARA), ch) for j, ch in enumerate(sag)]
        for x, ch in konumlar:
            karolar.append((x, y))
            harfler.append((ch, x + g["HX"], y + g["HY"]))

    if p.get("oyuk"):
        # Kutucuklar ve harfler tek yol: evenodd ile harfler kutucuktan delik olur
        d = " ".join([kutu_yolu(x, y, TW, TH, g["RX"]) for x, y in karolar]
                     + [harf_yolu(yazi, ch, x, y, g["HK"]) for ch, x, y in harfler])
        govde = f'<path d="{d}" fill="{p["karo"]}" fill-rule="evenodd"/>'
    else:
        k_svg = "".join(kutu(x, y, TW, TH, g["RX"], p["karo"]) for x, y in karolar)
        h_svg = "".join(harf(yazi, ch, x, y, g["HK"], p["harf"]) for ch, x, y in harfler)
        govde = f"<g>{k_svg}</g>\n<g>{h_svg}</g>"
    rx = ARTI / 2 if g["YUVARLAK"] else 0
    govde += ("\n<g>" + kutu(arti_x, 0, ARTI, H, rx, p["arti"])
              + kutu(0, arti_y, W, ARTI, rx, p["arti"]) + "</g>")
    return W, H, govde


GEO_A = dict(TW=160, TH=190, ARA=15, ACIK=85, ARTI=75, RX=20,
             HK=1.2, HX=20, HY=23, YUVARLAK=False)
GEO_B = dict(TW=160, TH=210, ARA=16, ACIK=64, ARTI=60, RX=26,
             HK=1.05, HX=27.5, HY=42, YUVARLAK=True)


# ---------------------------------------------------------------- amblem (C)
def amblem(p, S=170, ACIK=44, ARTI=60, RX=30, x0=0, y0=0):
    W = 2 * S + 2 * ACIK + ARTI
    ikinci = S + 2 * ACIK + ARTI
    g = "".join(kutu(x0 + x, y0 + y, S, S, RX, p["karo"])
                for x in (0, ikinci) for y in (0, ikinci))
    a = ARTI / 2
    g += kutu(x0 + S + ACIK, y0, ARTI, W, a, p["arti"])
    g += kutu(x0, y0 + S + ACIK, W, ARTI, a, p["arti"])
    return W, W, g


def arti_harfi(x, y, k, renk, t=21):
    """Yazı içinde T'nin yerine geçen artı: 100 x 120 kutuda."""
    return ("<g transform=\"translate({:g} {:g}) scale({:g})\">".format(x, y, k)
            + kutu(50 - t / 2, 0, t, 120, t / 2, renk)
            + kutu(4, 60 - t / 2, 92, t, t / 2, renk) + "</g>")


def yatay(p, cizgi=False):
    """cizgi=True: harfler dolgulu anahat yerine çizgi olarak (web sitesi için)."""
    E, _, g = amblem(p)
    ARA = 100
    k1, adim1 = 2.0, 125 * 2.0
    kelime = "POZİ+İF"
    gen1 = (len(kelime) - 1) * adim1 + 100 * k1
    ust = 86                       # büyük satırın harf üstü (İ noktası bunun üstünde)
    x0 = E + ARA
    alt = "MARİN ELEKTRİK"
    k2 = 0.7
    adim2 = (gen1 - 100 * k2) / (len(alt) - 1)
    y2 = ust + 120 * k1 + 54
    yerler = [(ch, x0 + i * adim1, ust, k1) for i, ch in enumerate(kelime)]
    yerler += [(ch, x0 + i * adim2, y2, k2) for i, ch in enumerate(alt)]
    cizgiler = ""
    for ch, x, y, k in yerler:
        if ch == "+":
            g += arti_harfi(x, y, k, p["arti"])
        elif cizgi:
            cizgiler += harf_cizgi(GRAVUR, ch, x, y, k, p["yazi"])
        else:
            g += harf(GRAVUR, ch, x, y, k, p["yazi"])
    if cizgiler:
        g += (f'<g fill="none" stroke="{p["yazi"]}" stroke-width="{GRAVUR["cizgi"]:g}" '
              f'stroke-linecap="{GRAVUR["uc"]}" stroke-linejoin="{GRAVUR["kose"]}">{cizgiler}</g>')
    return x0 + gen1, E, g


# ---------------------------------------------------------------- üretim
RENKLER = {
    "a": {
        "renkli": dict(karo=SIYAH, harf=BEYAZ, arti=KIRMIZI),
        "negatif": dict(karo=BEYAZ, harf=SIYAH, arti=KIRMIZI),
        "siyah": dict(karo=SIYAH, arti=SIYAH, oyuk=True),
        "beyaz": dict(karo=BEYAZ, arti=BEYAZ, oyuk=True),
    },
    "b": {
        "renkli": dict(karo=LACIVERT, harf=BEYAZ, arti=KIRMIZI),
        "negatif": dict(karo=BEYAZ, harf=LACIVERT, arti=KIRMIZI),
        "siyah": dict(karo=SIYAH, arti=SIYAH, oyuk=True),
        "beyaz": dict(karo=BEYAZ, arti=BEYAZ, oyuk=True),
    },
    "c": {
        "renkli": dict(karo=LACIVERT, yazi=LACIVERT, arti=KIRMIZI),
        "negatif": dict(karo=BEYAZ, yazi=BEYAZ, arti=KIRMIZI),
        "siyah": dict(karo=SIYAH, yazi=SIYAH, arti=SIYAH),
        "beyaz": dict(karo=BEYAZ, yazi=BEYAZ, arti=BEYAZ),
    },
}

AD = "Pozitif Marin Elektrik"


def uret():
    dosyalar = {}
    for mod in ("renkli", "negatif", "siyah", "beyaz"):
        dosyalar[f"pozitif-a-restorasyon-{mod}"] = kutucuklu(
            DAKTILO, [("POZI", "IF"), ("ELEK", "RIK")], GEO_A, RENKLER["a"][mod])
        dosyalar[f"pozitif-b-yenilenmis-{mod}"] = kutucuklu(
            GRAVUR, [("POZİ", "İF"), ("ELEK", "RİK")], GEO_B, RENKLER["b"][mod])
        dosyalar[f"pozitif-c-amblem-{mod}"] = amblem(RENKLER["c"][mod])
        dosyalar[f"pozitif-c-yatay-{mod}"] = yatay(RENKLER["c"][mod])
    _anahat_kaydet()

    os.makedirs(os.path.join(CIKTI, "svg"), exist_ok=True)
    for ad, (w, h, govde) in dosyalar.items():
        with open(os.path.join(CIKTI, "svg", ad + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg(w, h, govde, AD))

    # Favicon: beyaz yuvarlak zemin üzerinde amblem (koyu sekmelerde de görünür)
    E = 488
    pay = 64
    T = E + 2 * pay
    _, _, g = amblem(RENKLER["c"]["renkli"], x0=pay, y0=pay)
    with open(os.path.join(CIKTI, "svg", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(svg(T, T, kutu(0, 0, T, T, 120, BEYAZ) + g, AD))

    rsvg = RSVG
    if not rsvg:
        print("rsvg-convert bulunamadı: yalnızca SVG üretildi")
        return
    for klasor in ("png", "pdf"):
        os.makedirs(os.path.join(CIKTI, klasor), exist_ok=True)
    for ad in list(dosyalar) + ["favicon"]:
        kaynak = os.path.join(CIKTI, "svg", ad + ".svg")
        genislik = "1024" if ("amblem" in ad or ad == "favicon") else "2400"
        subprocess.run([rsvg, "-w", genislik, kaynak, "-o",
                        os.path.join(CIKTI, "png", ad + ".png")], check=True)
        if ad != "favicon":
            subprocess.run([rsvg, "-f", "pdf", kaynak, "-o",
                            os.path.join(CIKTI, "pdf", ad + ".pdf")], check=True)
    for boyut in (32, 180, 512):
        subprocess.run([rsvg, "-w", str(boyut), "-h", str(boyut),
                        os.path.join(CIKTI, "svg", "favicon.svg"), "-o",
                        os.path.join(CIKTI, "png", f"favicon-{boyut}.png")], check=True)
    print(f"{len(dosyalar) + 1} SVG, PNG ve PDF üretildi → {CIKTI}")
    site_dosyalari()


# ---------------------------------------------------------------- web sitesi (C seçildi)
SITE = os.path.join(KOK, "yeni-site")


def site_dosyalari():
    """Sitede kullanılan logo dosyaları.

    kaynak/logo-site.svg, kaynak/amblem-site.svg: kaynak/build.py bunları sayfalara
    gömer. Kutucuk ve yazı rengi currentColor'dır (açık temada lacivert, koyu temada
    beyaz); artı her iki temada kırmızıdır.
    yeni-site/: favicon.svg, favicon.ico, apple-touch-icon.png, logo.png (yapısal veri).
    """
    tema = dict(karo="currentColor", yazi="currentColor", arti=KIRMIZI)
    w, h, g = yatay(tema, cizgi=True)
    E, _, ga = amblem(tema)
    for ad, (gw, gh, govde) in {"logo-site.svg": (w, h, g), "amblem-site.svg": (E, E, ga)}.items():
        with open(os.path.join(KOK, "kaynak", ad), "w", encoding="utf-8") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {gw:g} {gh:g}">{govde}</svg>\n')

    img = os.path.join(SITE, "assets", "img")
    shutil.copyfile(os.path.join(CIKTI, "svg", "favicon.svg"), os.path.join(img, "favicon.svg"))
    # iOS köşeleri kendisi yuvarlar: zemin tam kare, amblem ortada
    pay = 104
    T = E + 2 * pay
    _, _, g = amblem(RENKLER["c"]["renkli"], x0=pay, y0=pay)
    dokunmatik = svg(T, T, kutu(0, 0, T, T, 0, BEYAZ) + g, AD).encode()
    subprocess.run([RSVG, "-w", "180", "-h", "180", "-o", os.path.join(img, "apple-touch-icon.png")],
                   input=dokunmatik, check=True)
    subprocess.run([RSVG, "-w", "1200", os.path.join(CIKTI, "svg", "pozitif-c-yatay-renkli.svg"),
                    "-o", os.path.join(img, "logo.png")], check=True)
    buyuk = subprocess.run([RSVG, "-w", "256", "-h", "256", os.path.join(CIKTI, "svg", "favicon.svg")],
                           capture_output=True, check=True).stdout
    Image.open(io.BytesIO(buyuk)).save(os.path.join(SITE, "favicon.ico"),
                                       sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"site logoları üretildi → kaynak/logo-site.svg, kaynak/amblem-site.svg, {SITE}")


if __name__ == "__main__":
    uret()
