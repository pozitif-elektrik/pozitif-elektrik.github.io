// Pozitif Marin Elektrik — site davranışları (vanilla JS, tüm sayfalar)
(() => {
  'use strict';
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  // Yıl
  $$('[data-yil]').forEach((el) => { el.textContent = new Date().getFullYear(); });

  // ---------------- Tema (açık / koyu) ----------------
  // İlk seçim <head> içindeki kısa betikte yapılır (sayfa çizilmeden önce).
  // Ziyaretçi düğmeye basana kadar cihazın ayarı izlenir; basınca seçim saklanır.
  const kok = document.documentElement;
  const kayitliTema = () => { try { return localStorage.getItem('tema'); } catch { return null; } };
  const temaUygula = (tema) => {
    kok.dataset.tema = tema;
    const meta = $('meta[name="theme-color"]');
    if (meta) meta.content = getComputedStyle(kok).backgroundColor;  // telefonda tarayıcı çubuğu = sayfa zemini
    $$('[data-tema-dugme]').forEach((d) => {
      d.setAttribute('aria-pressed', String(tema === 'koyu'));
      d.title = tema === 'koyu' ? 'Açık temaya geç' : 'Koyu temaya geç';
    });
  };
  temaUygula(kok.dataset.tema === 'koyu' ? 'koyu' : 'acik');
  $$('[data-tema-dugme]').forEach((d) => d.addEventListener('click', () => {
    const yeni = kok.dataset.tema === 'koyu' ? 'acik' : 'koyu';
    try { localStorage.setItem('tema', yeni); } catch { /* gizli pencere: yalnızca bu sayfada geçerli */ }
    temaUygula(yeni);
  }));
  const sistemKoyu = matchMedia('(prefers-color-scheme: dark)');
  sistemKoyu.addEventListener('change', (e) => { if (!kayitliTema()) temaUygula(e.matches ? 'koyu' : 'acik'); });
  // Başka bir sekmede değiştirilirse bu sekme de uysun
  window.addEventListener('storage', (e) => {
    if (e.key === 'tema') temaUygula(e.newValue === 'koyu' || (!e.newValue && sistemKoyu.matches) ? 'koyu' : 'acik');
  });

  // Kaydırınca üst menüye gölge
  const ust = $('#ust');
  if (ust) {
    const golge = () => ust.classList.toggle('shadow-md', window.scrollY > 8);
    golge();
    window.addEventListener('scroll', golge, { passive: true });
  }

  // Mobil menü: bağlantıya ya da dışarı tıklayınca, Esc'e basınca kapat
  const mobil = $('[data-mobil-menu]');
  if (mobil) {
    mobil.addEventListener('click', (e) => { if (e.target.closest('a')) mobil.removeAttribute('open'); });
    document.addEventListener('click', (e) => { if (!mobil.contains(e.target)) mobil.removeAttribute('open'); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobil.open) { mobil.removeAttribute('open'); $('summary', mobil).focus(); }
    });
  }

  // ---------------- Projeler galerisi: filtre + daha fazla göster ----------------
  const galeri = $('[data-galeri]');
  let filtre = 'hepsi';
  if (galeri) {
    const ogeler = $$('[data-kategori]', galeri);
    const sekmeler = $$('[data-filtre]');
    const dahaBtn = $('[data-galeri-daha]');
    const ADIM = 12;
    let limit = ADIM;

    const ciz = () => {
      const eslesen = ogeler.filter((o) => filtre === 'hepsi' || o.dataset.kategori === filtre);
      ogeler.forEach((o) => { o.hidden = true; o.dataset.disari = 'evet'; });
      eslesen.forEach((o, i) => { o.hidden = i >= limit; delete o.dataset.disari; });
      if (dahaBtn) dahaBtn.hidden = eslesen.length <= limit;
      // Seçili filtrenin görünümü aria-pressed'den gelir (aria-pressed:... sınıfları)
      sekmeler.forEach((s) => s.setAttribute('aria-pressed', String(s.dataset.filtre === filtre)));
    };
    const sec = (yeni, adresiGuncelle = true) => {
      filtre = sekmeler.some((s) => s.dataset.filtre === yeni) ? yeni : 'hepsi';
      limit = ADIM;
      ciz();
      if (adresiGuncelle) {
        const url = new URL(location.href);
        if (filtre === 'hepsi') url.searchParams.delete('kategori'); else url.searchParams.set('kategori', filtre);
        history.replaceState(null, '', url);
      }
    };
    sekmeler.forEach((s) => s.addEventListener('click', () => sec(s.dataset.filtre)));
    if (dahaBtn) dahaBtn.addEventListener('click', () => { limit += ADIM; ciz(); });
    sec(new URLSearchParams(location.search).get('kategori') || 'hepsi', false);
  }

  // ---------------- Büyütme penceresi (lightbox) ----------------
  const pencere = $('#galeri-pencere');
  if (pencere) {
    const pImg = $('[data-pencere-img]', pencere);
    const pBaslik = $('[data-pencere-baslik]', pencere);
    const pSayac = $('[data-pencere-sayac]', pencere);
    let liste = [];
    let sira = 0;

    const goster = (i) => {
      sira = (i + liste.length) % liste.length;
      const o = liste[sira];
      pImg.src = o.dataset.buyuk;
      pImg.alt = $('img', o).alt;
      pBaslik.textContent = o.dataset.baslik || '';
      pSayac.textContent = `${sira + 1} / ${liste.length}`;
      const sonraki = liste[(sira + 1) % liste.length];
      if (sonraki) { const on = new Image(); on.src = sonraki.dataset.buyuk; }
    };

    $$('[data-lightbox]').forEach((grup) => grup.addEventListener('click', (e) => {
      const o = e.target.closest('[data-buyuk]');
      if (!o) return;
      // Aynı gruptaki, filtre dışında kalmayan tüm fotoğraflar arasında gezin
      liste = $$('[data-buyuk]', grup).filter((x) => !x.dataset.disari);
      goster(liste.indexOf(o));
      pencere.showModal();
    }));

    $('[data-pencere-onceki]', pencere).addEventListener('click', () => goster(sira - 1));
    $('[data-pencere-sonraki]', pencere).addEventListener('click', () => goster(sira + 1));
    $('[data-pencere-kapat]', pencere).addEventListener('click', () => pencere.close());
    // Pencerenin dışına (karartılmış arka plana) tıklayınca kapat
    pencere.addEventListener('click', (e) => { if (e.target === pencere) pencere.close(); });
    pencere.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') goster(sira - 1);
      if (e.key === 'ArrowRight') goster(sira + 1);
    });
    pencere.addEventListener('close', () => { pImg.removeAttribute('src'); });

    let dokunX = null;
    pImg.addEventListener('touchstart', (e) => { dokunX = e.touches[0].clientX; }, { passive: true });
    pImg.addEventListener('touchend', (e) => {
      if (dokunX === null) return;
      const fark = e.changedTouches[0].clientX - dokunX;
      if (Math.abs(fark) > 40) goster(sira + (fark < 0 ? 1 : -1));
      dokunX = null;
    });
  }

  // ---------------- IBAN kopyala ----------------
  const bildirim = $('[data-bildirim]');
  let bildirimZaman;
  const bildir = (metin) => {
    if (!bildirim) return;
    $('[data-bildirim-metin]', bildirim).textContent = metin;
    bildirim.hidden = false;
    clearTimeout(bildirimZaman);
    bildirimZaman = setTimeout(() => { bildirim.hidden = true; }, 2200);
  };
  $$('[data-kopyala]').forEach((btn) => btn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(btn.dataset.kopyala);
      bildir('IBAN kopyalandı');
    } catch {
      const sec = window.getSelection();
      const r = document.createRange();
      r.selectNodeContents($('[data-iban]'));
      sec.removeAllRanges();
      sec.addRange(r);
      bildir('IBAN seçildi, Ctrl+C ile kopyalayabilirsiniz');
    }
  }));
})();
