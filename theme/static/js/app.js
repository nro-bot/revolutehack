// Revolute app pages.
//
// Every page works without this file: tabs are links to sections, popups are
// links to the real page or file, and each page is a real page. This script
// adds the app feel on top. It has no dependencies and builds nothing.
//
//   1. Section tabs    mark the current tab
//   2. Popups          closing on a tap outside the card
//   3. Embed popup     Luma, Instagram, YouTube, affiliates, and the email form
//   4. Media viewer    one photo, video or map, with stepping through a group
//   5. Preview clips   which project clip is playing
//   6. Small things    copy buttons, the back button

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const isShown = (el) => el.getClientRects().length > 0;

// ---- 1. Section tabs --------------------------------------------------------
// The stylesheet shows the panel that the address points at. All that is left
// to do here is tell the tab row which tab that is.

function syncTabs() {
  const tabs = $$('.subnav .chip');
  if (!tabs.length) return;
  const current = tabs.find((tab) => tab.hash && tab.hash === location.hash) ?? tabs[0];
  for (const tab of tabs) tab.setAttribute('aria-current', String(tab === current));
}

// ---- 2. Popups --------------------------------------------------------------
// Both popups are <dialog> elements opened with showModal(), so the browser
// does the hard parts: it keeps focus inside, dims and disables the page
// behind, and closes on Escape and on Android's back button or back gesture.
// The only thing added here is closing on a tap outside the card.

for (const dialog of $$('dialog')) {
  dialog.addEventListener('click', (event) => {
    // A click on the dialog itself is a click outside its card.
    if (event.target === dialog || event.target.closest('[data-close]')) dialog.close();
  });
}

// ---- 3. Embed popup ---------------------------------------------------------
// A link with data-pop="embed" opens its site in a frame, with a button to the
// real page. Without data-embed it shows a short description and the button.
// A link with data-pop="email" opens the email form.

const pop = $('#pop');
const popFrame = $('#pop-frame');
const popGo = $('#pop-go');
const mailSubject = $('#mail-subject');
const mailBody = $('#mail-body');
let mailTo = '';

function mailHref() {
  const params = new URLSearchParams();
  if (mailSubject.value) params.set('subject', mailSubject.value);
  if (mailBody.value) params.set('body', mailBody.value);
  // Mail apps expect %20 for spaces, not the + that URLSearchParams writes.
  const query = params.toString().replaceAll('+', '%20');
  popGo.href = mailTo + (query ? `?${query}` : '');
}

function openPop(link) {
  const isEmail = link.dataset.pop === 'email';
  const embed = isEmail ? '' : link.dataset.embed;

  $('#pop-embed').hidden = isEmail;
  $('#pop-email').hidden = !isEmail;
  pop.classList.toggle('small', isEmail || !embed);
  pop.classList.toggle('video', link.dataset.shape === 'video');

  if (isEmail) {
    mailTo = link.href;
    pop.setAttribute('aria-label', 'Email us');
    popGo.textContent = 'Open in mail app';
    popGo.removeAttribute('target');
    mailHref();
  } else {
    pop.setAttribute('aria-label', link.dataset.title);
    $('#pop-title').textContent = link.dataset.title;
    $('#pop-about').textContent = link.dataset.about;
    popGo.textContent = link.dataset.action;
    popGo.href = link.href;
    popGo.target = '_blank';
    popFrame.classList.remove('loaded');
    popFrame.hidden = !embed;
    if (embed) {
      popFrame.title = link.dataset.title;
      popFrame.src = embed;
    }
  }
  if (!pop.open) pop.showModal();
}

popFrame.addEventListener('load', () => popFrame.classList.add('loaded'));
pop.addEventListener('close', () => {
  if (pop.open) return; // already reopened
  // Emptying the frame stops whatever was playing in it.
  popFrame.removeAttribute('src');
  popFrame.hidden = true;
});
mailSubject.addEventListener('input', mailHref);
mailBody.addEventListener('input', mailHref);
$('#pop-email').addEventListener('submit', (event) => event.preventDefault());

// ---- 4. Media viewer --------------------------------------------------------
// A link with data-view="photo|video|map" opens in the viewer. Links that share
// a data-group can be stepped through; a link without one is shown on its own.

const viewer = $('#viewer');
const stage = $('#vstage');
const caption = $('#vcap');
const counter = $('#vcount');
const prevButton = $('#vprev');
const nextButton = $('#vnext');
let shown = null;

function groupOf(link) {
  if (!link.dataset.group) return [link];
  return $$(`[data-view][data-group="${link.dataset.group}"]`).filter(isShown);
}

function preload(link) {
  if (link?.dataset.view === 'photo') new Image().src = link.href;
}

function show(link) {
  shown = link;
  const kind = link.dataset.view;
  let media;

  if (kind === 'video') {
    media = document.createElement('video');
    media.src = link.href;
    if (link.dataset.poster) media.poster = link.dataset.poster;
    media.controls = true;
    media.playsInline = true;
    media.autoplay = !reducedMotion;
  } else if (kind === 'map') {
    media = document.createElement('iframe');
    media.src = link.dataset.embed;
    media.title = `Map: ${link.dataset.title}`;
    media.referrerPolicy = 'strict-origin-when-cross-origin';
  } else {
    media = document.createElement('img');
    media.alt = link.dataset.cap ?? '';
    media.draggable = false;
    if (link.dataset.thumb) {
      // The thumbnail is already loaded, so show it at once and swap in the
      // full picture when it arrives.
      media.src = link.dataset.thumb;
      const full = new Image();
      full.onload = () => {
        if (shown === link) media.src = link.href;
      };
      full.src = link.href;
    } else {
      media.src = link.href;
    }
  }
  stage.replaceChildren(media);

  const text = [link.dataset.cap, link.dataset.credit].filter(Boolean).join('  ·  ');
  caption.replaceChildren(text);
  if (kind === 'map') {
    const open = document.createElement('a');
    open.href = link.href;
    open.target = '_blank';
    open.rel = 'noopener';
    open.textContent = 'Open in Maps';
    caption.append('  ·  ', open);
  }

  const group = groupOf(link);
  const index = group.indexOf(link);
  viewer.classList.toggle('solo', group.length < 2);
  counter.textContent = `${index + 1} / ${group.length}`;
  prevButton.disabled = index <= 0;
  nextButton.disabled = index >= group.length - 1;
  preload(group[index + 1]);
  preload(group[index - 1]);
}

function step(offset) {
  if (!shown) return;
  const group = groupOf(shown);
  const next = group[group.indexOf(shown) + offset];
  if (next) show(next);
}

prevButton.addEventListener('click', () => step(-1));
nextButton.addEventListener('click', () => step(1));
viewer.addEventListener('close', () => {
  if (viewer.open) return; // already reopened
  stage.replaceChildren(); // stops a playing video
  shown = null;
});
viewer.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowLeft') step(-1);
  if (event.key === 'ArrowRight') step(1);
});

// Swipe sideways for the next or previous item, and down to close.
let swipeStart = null;
viewer.addEventListener('pointerdown', (event) => {
  if (event.target.closest('button, a, video, iframe')) return;
  swipeStart = { x: event.clientX, y: event.clientY };
});
viewer.addEventListener('pointercancel', () => (swipeStart = null));
viewer.addEventListener('pointerup', (event) => {
  if (!swipeStart) return;
  const dx = event.clientX - swipeStart.x;
  const dy = event.clientY - swipeStart.y;
  swipeStart = null;
  if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.4) step(dx < 0 ? 1 : -1);
  else if (dy > 72 && dy > Math.abs(dx) * 1.4) viewer.close();
});

// ---- 5. Preview clips -------------------------------------------------------
// One clip plays at a time: the one last pointed at while it is on screen,
// otherwise the first one on screen. People who ask for less motion get the
// still frames.

const clips = $$('[data-clip]');
let pointedAt = null;

function inViewport(el) {
  const box = el.getBoundingClientRect();
  return box.width > 0 && box.bottom > 0 && box.top < innerHeight;
}
// The part of the screen a clip has to reach before it plays: clear of the
// tabs at the top and of the bottom bar.
function inPlayZone(el) {
  const box = el.getBoundingClientRect();
  return box.width > 0 && box.bottom > innerHeight * 0.08 && box.top < innerHeight * 0.72;
}

function pickClip() {
  if (!clips.length || reducedMotion) return;
  const playing = pointedAt && inViewport(pointedAt) ? pointedAt : clips.find(inPlayZone);
  for (const clip of clips) {
    const video = $('video', clip);
    if (clip === playing) {
      video.play().then(
        () => video.classList.add('on'),
        () => {}, // the browser declined to play; the still frame stays
      );
    } else {
      video.pause();
      video.classList.remove('on');
    }
  }
}

if (clips.length && !reducedMotion) {
  // Look again whenever a clip scrolls into or out of the play zone.
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(pickClip, { rootMargin: '-8% 0px -28% 0px' });
    for (const clip of clips) observer.observe(clip);
  }
  for (const clip of clips) {
    // Pointing anywhere on a project's card counts, not only at its picture.
    (clip.closest('.win') ?? clip).addEventListener('pointerenter', (event) => {
      if (event.pointerType === 'touch') return;
      pointedAt = clip;
      pickClip();
    });
  }
  pickClip();
}

// ---- 6. Small things --------------------------------------------------------

// Copy buttons: <button data-copy="text">.
for (const button of $$('[data-copy]')) {
  button.addEventListener('click', async () => {
    const label = button.textContent;
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.textContent = 'Copied';
    } catch {
      // No clipboard access: select the text beside the button instead.
      const code = button.parentElement.querySelector('code');
      if (code) getSelection().selectAllChildren(code);
      button.textContent = 'Selected';
    }
    setTimeout(() => (button.textContent = label), 2000);
  });
}

// The back button returns to wherever the visitor was on this site. Arriving
// from elsewhere, it goes to the address in its link instead. On the homepage
// with nowhere to go back to, it is dimmed.
const VISITED = 'revolute-visited';

function hasVisited() {
  try {
    return sessionStorage.getItem(VISITED) === '1';
  } catch {
    return false;
  }
}
function markVisited() {
  try {
    sessionStorage.setItem(VISITED, '1');
  } catch {
    // Storage is blocked. The back button falls back to its link.
  }
}
function canGoBack() {
  return hasVisited() && (window.navigation?.canGoBack ?? history.length > 1);
}
function syncBack() {
  const onHome = document.body.classList.contains('page-upcoming');
  for (const back of $$('[data-back]')) {
    back.setAttribute('aria-disabled', String(onHome && !canGoBack()));
  }
}

// ---- Wiring -----------------------------------------------------------------

document.addEventListener('click', (event) => {
  // Leave new-tab clicks alone: every link here has a real address.
  if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  const link = event.target.closest('a');
  if (!link) return;

  if (link.dataset.pop) {
    event.preventDefault();
    openPop(link);
  } else if (link.dataset.view) {
    event.preventDefault();
    show(link);
    if (!viewer.open) viewer.showModal();
  } else if (link.hasAttribute('data-back')) {
    if (canGoBack()) {
      event.preventDefault();
      history.back();
    }
  } else if (link.origin === location.origin && !link.target) {
    markVisited();
  }
});

addEventListener('hashchange', () => {
  markVisited();
  syncTabs();
  syncBack();
  pickClip();
});
// A page restored from the back/forward cache needs its state read again.
addEventListener('pageshow', () => {
  syncTabs();
  syncBack();
});

syncTabs();
syncBack();
