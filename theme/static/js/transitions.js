// Revolute: the one page transition that needs a script.
//
// Moving between a project's card and its page, the picture grows from one
// into the other. For that, the browser needs the two pictures to share a
// name, and only those two: a named picture is drawn on its own layer during
// any transition, above the rest of the page, which would hide the place
// label that sits on its corner. So the name is given here, only for that
// one move, and taken away when the move ends.
//
// This file is loaded as an ordinary script in the <head>, not as a module:
// `pagereveal` fires before the page is first drawn, and a module would run
// too late to hear it. Browsers without cross-page transitions never fire
// these events, and simply change page.

(() => {
  const slugOf = (address) => {
    try {
      return new URL(address, location.href).pathname.match(/\/projects\/([^/]+)\/?$/)?.[1];
    } catch {
      return undefined;
    }
  };

  function name(slug, transition) {
    if (!slug) return;
    const name = `project-${slug}`;
    // A card can be on the page twice, in two tabs. Take the one showing.
    const picture = [...document.querySelectorAll(`[data-vt="${name}"]`)].find((el) => el.offsetParent);
    if (!picture) return;
    picture.style.viewTransitionName = name;
    transition.finished.finally(() => {
      picture.style.viewTransitionName = '';
    });
  }

  // Leaving a page: going to a project, or leaving one.
  addEventListener('pageswap', (event) => {
    if (!event.viewTransition || !event.activation) return;
    name(slugOf(event.activation.entry.url) ?? slugOf(location.href), event.viewTransition);
  });

  // Arriving on a page: at a project, or back from one.
  addEventListener('pagereveal', (event) => {
    const from = window.navigation?.activation?.from;
    if (!event.viewTransition || !from) return;
    name(slugOf(location.href) ?? slugOf(from.url), event.viewTransition);
  });
})();
