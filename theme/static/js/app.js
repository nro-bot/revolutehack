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
// iPhones and iPods say so. An iPad says it is a Mac, but a Mac has no touch.
const isAppleTouchDevice =
  /iPhone|iPad|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

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
// A link with data-pop="stack" shows several pages, one under another.
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

const popEmbed = $('#pop-embed');
const popStack = $('#pop-stack');
const popAct = $('#pop-act');
const embedBox = $('.embed', popEmbed);
let slowTimer = 0;

// Shows nothing until the page inside has loaded. If it takes a long time,
// or the site refuses to load here, the description shows instead.
function loadFrame(address, title) {
  clearTimeout(slowTimer);
  popFrame.classList.remove('loaded');
  embedBox.classList.remove('slow');
  embedBox.classList.add('framed');
  slowTimer = setTimeout(() => embedBox.classList.add('slow'), 6000);
  popFrame.hidden = false;
  popFrame.title = title;
  popFrame.src = address;
}

function openPop(link) {
  const kind = link.dataset.pop; // embed | stack | email
  const embed = kind === 'embed' ? link.dataset.embed : '';
  const action = kind === 'email' ? 'Open in mail app' : link.dataset.action;

  popEmbed.hidden = kind !== 'embed';
  popStack.hidden = kind !== 'stack';
  $('#pop-email').hidden = kind !== 'email';
  pop.classList.toggle('small', kind === 'email' || (kind === 'embed' && !embed));
  pop.classList.toggle('video', link.dataset.shape === 'video');

  // Whatever was in the frame is from the last popup.
  clearTimeout(slowTimer);
  popFrame.classList.remove('loaded');
  popFrame.removeAttribute('src');
  popFrame.hidden = true;
  embedBox.classList.remove('framed', 'slow');

  // Several pages, one under another: they are written into the page as a
  // <template>, so they only start loading now.
  popStack.replaceChildren(kind === 'stack' ? $(`#${link.dataset.stack}`).content.cloneNode(true) : '');
  popStack.scrollTop = 0;
  for (const frame of $$('iframe', popStack)) nearStack.observe(frame);

  // The button to the real page. A popup without `data-action` has none.
  popAct.hidden = !action;
  popGo.textContent = action ?? '';
  if (kind === 'email') {
    mailTo = link.href;
    pop.setAttribute('aria-label', 'Email us');
    popGo.removeAttribute('target');
    mailHref();
  } else {
    pop.setAttribute('aria-label', link.dataset.title);
    popGo.href = link.href;
    popGo.target = '_blank';
  }
  if (kind === 'embed') {
    $('#pop-title').textContent = link.dataset.title;
    $('#pop-about').textContent = link.dataset.about;
    if (embed) loadFrame(embed, link.dataset.title);
  }
  if (!pop.open) pop.showModal();
}

// Each page in a stack starts loading when it is scrolled near, and appears
// once it has loaded. A load event does not bubble, so it is caught on its
// way down.
const nearStack = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      nearStack.unobserve(entry.target);
      entry.target.src = entry.target.dataset.src;
    }
  },
  { root: popStack, rootMargin: '600px 0px' },
);
popStack.addEventListener(
  'load',
  (event) => {
    if (event.target.getAttribute('src')) event.target.classList.add('loaded');
  },
  true,
);

popFrame.addEventListener('load', () => {
  if (!popFrame.getAttribute('src')) return;
  clearTimeout(slowTimer);
  embedBox.classList.remove('slow');
  popFrame.classList.add('loaded');
});
pop.addEventListener('close', () => {
  if (pop.open) return; // already reopened
  // Emptying the frame stops whatever was playing in it.
  clearTimeout(slowTimer);
  popFrame.removeAttribute('src');
  popFrame.hidden = true;
  popStack.replaceChildren();
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
    media.alt = link.dataset.cap ?? $('img', link)?.alt ?? '';
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

  // Photos and videos in the gallery have no caption, only a credit: one line.
  const text = [link.dataset.cap, link.dataset.credit].filter(Boolean).join('  ·  ');
  caption.replaceChildren(text);
  viewer.classList.toggle('nocap', !link.dataset.cap);
  if (kind === 'map') {
    // The link under the map opens the Maps app: Apple Maps on an iPhone or
    // iPad, where it is the one already installed, and Google Maps elsewhere.
    const useApple = isAppleTouchDevice && link.dataset.apple;
    const open = document.createElement('a');
    open.href = useApple ? link.dataset.apple : link.href;
    open.target = '_blank';
    open.rel = 'noopener';
    open.textContent = useApple ? 'Open in Apple Maps' : 'Open in Google Maps';
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

// The back button on the page does exactly what the browser's own back
// button does. When the browser has nowhere to go back to, it is dimmed.
function canGoBack() {
  return window.navigation?.canGoBack ?? history.length > 1;
}
function syncBack() {
  for (const back of $$('[data-back]')) back.setAttribute('aria-disabled', String(!canGoBack()));
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
    event.preventDefault();
    if (canGoBack()) history.back();
  }
});

addEventListener('hashchange', () => {
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
