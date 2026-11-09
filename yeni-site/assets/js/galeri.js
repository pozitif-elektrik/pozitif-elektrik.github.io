// Pozitif Marin Elektrik — fotoğraf büyütme penceresi
// PhotoSwipe 5.4.4 (MIT, https://photoswipe.com): dokunarak kaydırma, iki parmakla
// yakınlaştırma, aşağı kaydırıp kapatma, klavye ve ekran okuyucu desteği.
//
// Galeri: [data-lightbox] içindeki <a data-pswp-width data-pswp-height href="büyük.jpg">
// öğeleri. Gizli (filtre dışı) gruplardaki fotoğraflar atlanır. Kütüphane
// yüklenemezse bağlantılar büyük fotoğrafı doğrudan açar.
import PhotoSwipeLightbox from 'https://cdn.jsdelivr.net/npm/photoswipe@5.4.4/dist/photoswipe-lightbox.esm.min.js';

const KAYNAK = 'https://cdn.jsdelivr.net/npm/photoswipe@5.4.4/dist/';

// Pencere stili yalnızca galerisi olan sayfalarda, sayfa açıldıktan sonra yüklenir
const stil = document.createElement('link');
stil.rel = 'stylesheet';
stil.href = KAYNAK + 'photoswipe.css';
document.head.append(stil);

const lightbox = new PhotoSwipeLightbox({
  gallery: '[data-lightbox]',
  children: 'a[data-pswp-width]:not([hidden] *)',
  pswpModule: () => import(KAYNAK + 'photoswipe.esm.min.js'),
  bgOpacity: 0.97,
  // Masaüstünde alttaki açıklama ve oklar için pay; telefonda fotoğraf tam ekran
  paddingFn: (alan) => (alan.x < 768
    ? { top: 0, right: 0, bottom: 0, left: 0 }
    : { top: 56, right: 72, bottom: 64, left: 72 }),
  closeTitle: 'Kapat (Esc)',
  zoomTitle: 'Yakınlaştır',
  arrowPrevTitle: 'Önceki fotoğraf',
  arrowNextTitle: 'Sonraki fotoğraf',
  errorMsg: 'Fotoğraf yüklenemedi',
  indexIndicatorSep: ' / ',
});

lightbox.on('uiRegister', () => {
  const pswp = lightbox.pswp;
  // Zemin: sitenin koyu laciverti
  pswp.element.style.setProperty('--pswp-bg', '#060b16');
  // Alt açıklama: fotoğrafın kategorisi
  pswp.ui.registerElement({
    name: 'aciklama',
    className: 'pswp__aciklama pswp__hide-on-close pointer-events-none absolute inset-x-0 bottom-0 bg-linear-to-t from-black/70 to-transparent px-4 pb-5 pt-12 text-center text-sm font-semibold tracking-wide text-white',
    appendTo: 'root',
    onInit: (el) => {
      el.setAttribute('aria-live', 'polite');
      const yaz = () => { el.textContent = pswp.currSlide?.data.element?.dataset.baslik || ''; };
      pswp.on('change', yaz);
      pswp.on('afterInit', yaz);
    },
  });
});

// Telefonda "geri" tuşu sayfadan çıkmak yerine pencereyi kapatsın
lightbox.on('beforeOpen', () => history.pushState({ pswp: true }, ''));
lightbox.on('close', () => { if (history.state?.pswp) history.back(); });
window.addEventListener('popstate', () => {
  const pswp = lightbox.pswp;
  if (!pswp) return;
  // Açılış animasyonu sürerken kapatma isteği yok sayılır; animasyon bitince kapat
  if (pswp.opener.isOpen) pswp.close();
  else pswp.on('openingAnimationEnd', () => pswp.close());
});

lightbox.init();
