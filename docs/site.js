import { WORDING_CONTRASTS, formatContrast, relativeMagnitude } from './study-data.mjs';

const get = (selector, parent = document) => parent.querySelector(selector);
const getAll = (selector, parent = document) => [...parent.querySelectorAll(selector)];

function initializeExplorer() {
  const panel = get('.experiment-panel');
  if (!panel) return;
  const buttons = getAll('[data-wording]', panel);
  const output = get('#contrastOutput', panel);
  const tag = get('#wordingTag', panel);
  const heading = get('#wordingHeading', panel);
  const description = get('#wordingDescription', panel);
  const meter = get('#contrastMeter', panel);
  const track = get('.signed-track', panel);

  function selectCondition(condition) {
    if (!condition) return;
    const positive = condition.value >= 0;
    buttons.forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.wording === condition.id));
    });
    panel.dataset.tone = positive ? 'positive' : 'negative';
    output.value = formatContrast(condition.value);
    output.textContent = formatContrast(condition.value);
    tag.textContent = `${condition.label.toUpperCase()} WORDING`;
    heading.textContent = condition.heading;
    description.textContent = condition.explanation;
    meter.classList.toggle('positive', positive);
    meter.classList.toggle('negative', !positive);
    // Each side of the symmetric signed axis occupies half the track.
    meter.style.width = `${relativeMagnitude(condition.value) / 2}%`;
    track.setAttribute('aria-label', `${condition.label} wording contrast: ${positive ? 'positive' : 'negative'} ${Math.abs(condition.value).toFixed(3)} on a scale from negative 0.25 to positive 0.25`);
  }

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      selectCondition(WORDING_CONTRASTS.find(condition => condition.id === button.dataset.wording));
    });
  });
  selectCondition(WORDING_CONTRASTS[0]);
}

function initializeFigureDialog() {
  const dialog = get('#figureDialog');
  if (!dialog) return;
  const largeImage = get('#figureDialogImage', dialog);
  const caption = get('#figureDialogCaption', dialog);
  getAll('[data-figure-open]').forEach(button => {
    button.addEventListener('click', () => {
      const figure = button.closest('figure');
      const thumbnail = get('img', button);
      if (!thumbnail) return;
      if (typeof dialog.showModal !== 'function') {
        window.open(thumbnail.src, '_blank', 'noopener,noreferrer');
        return;
      }
      largeImage.src = thumbnail.src;
      largeImage.alt = thumbnail.alt;
      caption.textContent = get('figcaption', figure)?.textContent.trim() || '';
      dialog.showModal();
    });
  });
  get('[data-dialog-close]', dialog)?.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => largeImage.removeAttribute('src'));
}

function initializeNavigation() {
  const toggle = get('.menu-toggle');
  const navigation = get('#primaryNav');
  if (!toggle || !navigation) return;
  toggle.addEventListener('click', () => {
    const open = navigation.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  getAll('a', navigation).forEach(link => link.addEventListener('click', () => {
    navigation.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation');
  }));
}

function initializeReadingProgress() {
  const progress = get('#readingProgress');
  if (!progress) return;
  let scheduled = false;
  function update() {
    const available = document.documentElement.scrollHeight - window.innerHeight;
    const percent = available > 0 ? Math.min(100, (window.scrollY / available) * 100) : 0;
    progress.style.width = `${percent}%`;
    scheduled = false;
  }
  window.addEventListener('scroll', () => {
    if (!scheduled) {
      window.requestAnimationFrame(update);
      scheduled = true;
    }
  }, { passive: true });
  window.addEventListener('resize', update);
  update();
}

function initializeReveals() {
  if (!('IntersectionObserver' in window)) return;
  document.body.classList.add('enhanced');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -30px 0px', threshold: 0.07 });
  getAll('.reveal').forEach(element => observer.observe(element));
}

initializeExplorer();
initializeFigureDialog();
initializeNavigation();
initializeReadingProgress();
initializeReveals();
