#!/usr/bin/env python3
"""Projeler galerisi için kırpılmamış önizleme görselleri.

Kullanım (proje kökünde):  python3 kaynak/onizleme.py
Girdi:  yeni-site/assets/img/galeri/*.jpg          (büyük boy, uzun kenar ≤1100 px)
Çıktı:  yeni-site/assets/img/galeri/onizleme/*.jpg (yükseklik ≤540 px, oran korunur)

Projeler sayfasındaki galeri fotoğrafları kare kırpmadan, kendi oranlarıyla
gösterir. Ana sayfa ve hizmetler sayfasındaki kare küçükler (galeri/kucuk/)
ayrıdır ve bu betikle değişmez. Pillow gerekir.
"""
import glob
import os

from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GALERI = os.path.join(KOK, "yeni-site", "assets", "img", "galeri")
CIKTI = os.path.join(GALERI, "onizleme")
YUKSEKLIK = 540   # galeri satırları masaüstünde ~250-330 px; 2x ekranda keskin kalsın

os.makedirs(CIKTI, exist_ok=True)
toplam = 0
for yol in sorted(glob.glob(os.path.join(GALERI, "*.jpg"))):
    im = Image.open(yol).convert("RGB")
    w, h = im.size
    if h > YUKSEKLIK:
        im = im.resize((round(w * YUKSEKLIK / h), YUKSEKLIK), Image.LANCZOS)
    hedef = os.path.join(CIKTI, os.path.basename(yol))
    im.save(hedef, "JPEG", quality=78, optimize=True, progressive=True)
    toplam += os.path.getsize(hedef)
print(f"{len(os.listdir(CIKTI))} önizleme, toplam {toplam // 1024} KB → {CIKTI}")
