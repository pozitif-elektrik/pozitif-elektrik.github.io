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

  // ---------------- Projeler galerisi: kategori filtresi ----------------
  // Fotoğraflar kategori gruplarında durur; filtre seçili olmayan grupları gizler.
  // Büyütme penceresi (PhotoSwipe) gizli gruplardaki fotoğrafları atlar: assets/js/galeri.js
  const galeri = $('[data-galeri]');
  if (galeri) {
    const gruplar = $$('[data-grup]', galeri);
    const filtreler = $$('[data-filtre]');
    const kaydir = $('[data-filtre-kaydir]');
    const sec = (yeni, kullanici = true) => {
      const filtre = filtreler.some((f) => f.dataset.filtre === yeni) ? yeni : 'hepsi';
      gruplar.forEach((g) => { g.hidden = filtre !== 'hepsi' && g.dataset.grup !== filtre; });
      filtreler.forEach((f) => f.setAttribute('aria-pressed', String(f.dataset.filtre === filtre)));
      // Mobilde yatay kayan filtre çubuğunda seçili düğme görünür kalsın
      const aktif = filtreler.find((f) => f.dataset.filtre === filtre);
      if (kaydir && aktif) kaydir.scrollLeft = Math.max(0, aktif.offsetLeft - kaydir.clientWidth / 2 + aktif.offsetWidth / 2);
      if (kullanici) {
        const url = new URL(location.href);
        if (filtre === 'hepsi') url.searchParams.delete('kategori'); else url.searchParams.set('kategori', filtre);
        history.replaceState(null, '', url);
        // Sayfa galerinin altına inmişse galerinin başına dön
        if (galeri.getBoundingClientRect().top < 0) galeri.scrollIntoView({ block: 'start' });
      }
    };
    filtreler.forEach((f) => f.addEventListener('click', () => sec(f.dataset.filtre)));
    sec(new URLSearchParams(location.search).get('kategori') || 'hepsi', false);
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
