document.addEventListener('alpine:init', () => {
  Alpine.data('studioShell', () => ({
    open: false,
    toggleMenu() {
      this.open ? this.closeMenu() : this.openMenu();
    },
    openMenu() {
      this.open = true;
      document.body.classList.add('menu-open');
      const menu = document.getElementById('site-menu');
      if (menu) menu.classList.add('is-open');
    },
    closeMenu() {
      this.open = false;
      document.body.classList.remove('menu-open');
      const menu = document.getElementById('site-menu');
      if (menu) menu.classList.remove('is-open');
    },
    trapFocus(event) {
      const items = [...document.querySelectorAll('#site-menu a, #site-menu button')];
      if (!items.length) return;
      const first = items[0], last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  }));
});

document.addEventListener('DOMContentLoaded', () => {
  const sectionHeight = document.querySelector('.section-height');
  const track = document.querySelector('.track');
  const stickyElement = document.querySelector('.sticky-element');
  const rabbitWrapper = document.querySelector('.rabbit-wrapper');
  const runnerCanvas = rabbitWrapper?.querySelector('.warrior-run-canvas');
  const runnerContext = runnerCanvas?.getContext('2d');
  const processSection = document.querySelector('#our-process');
  const howSection = document.querySelector('.how-we-do-it-section');
  const heroWarriorCanvas = document.querySelector('.hero-warrior-canvas');
  const heroWarriorContext = heroWarriorCanvas?.getContext('2d');
  const footerWarriorCanvas = document.querySelector('.footer-warrior-canvas');
  const footerWarriorContext = footerWarriorCanvas?.getContext('2d', { willReadFrequently: true });
  const serviceModal = document.querySelector('#service-modal');
  const serviceModalTitle = document.querySelector('#service-modal-title');
  const serviceModalDescription = document.querySelector('#service-modal-description');
  const serviceModalTags = document.querySelector('#service-modal-tags');
  
  if (!sectionHeight || !track) return;

  const desktopQuery = window.matchMedia('(min-width: 992px)');
  const reducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  let maxScrollDistance = 0;
  let scrollTimeout = null;
  let lastScrollY = window.scrollY;
  let pendingScrollY = lastScrollY;
  let scrollRenderFrame = null;
  let processMetrics = null;
  let heroWarriorMetrics = null;
  let lastRunnerScrollTime = performance.now();
  let runnerVelocity = 0;
  let runnerFrame = 0;
  let runnerFrameTime = null;
  let runnerIsActive = false;
  let resizeFrame = null;

  const runnerFrameWidth = 261;
  const runnerFrameHeight = 269;
  const runnerFrameCount = 32;
  const runnerFrameColumns = 8;
  // The first eight frames are a stationary lead-in, not part of the run.
  const runnerFirstRunningFrame = 8;
  const runnerSprite = runnerCanvas ? new Image() : null;
  const heroWarriorFrameWidth = 640;
  const heroWarriorFrameHeight = 360;
  const heroWarriorFrameCount = 64;
  const heroWarriorFrameColumns = 6;
  const heroWarriorSprite = heroWarriorCanvas ? new Image() : null;
  let heroWarriorFrame = -1;
  let runnerSpriteRequested = false;
  let heroWarriorSpriteRequested = false;
  let runnerSpriteReady = false;
  let heroWarriorSpriteReady = false;
  let heroWarriorPreloadScheduled = false;

  let currentFacing = 1;

  function drawRunnerFrame(frame) {
    if (!runnerContext || !runnerSpriteReady) return;

    const frameIndex = Math.floor(frame) % runnerFrameCount;
    const sourceX = (frameIndex % runnerFrameColumns) * runnerFrameWidth;
    const sourceY = Math.floor(frameIndex / runnerFrameColumns) * runnerFrameHeight;
    runnerContext.clearRect(0, 0, runnerFrameWidth, runnerFrameHeight);
    runnerContext.drawImage(
      runnerSprite,
      sourceX,
      sourceY,
      runnerFrameWidth,
      runnerFrameHeight,
      0,
      0,
      runnerFrameWidth,
      runnerFrameHeight
    );
  }

  function drawHeroWarriorFrame(frame) {
    if (!heroWarriorContext || !heroWarriorSpriteReady) return;

    const frameIndex = Math.max(0, Math.min(heroWarriorFrameCount - 1, Math.round(frame)));
    if (frameIndex === heroWarriorFrame) return;

    heroWarriorFrame = frameIndex;
    const sourceX = (frameIndex % heroWarriorFrameColumns) * heroWarriorFrameWidth;
    const sourceY = Math.floor(frameIndex / heroWarriorFrameColumns) * heroWarriorFrameHeight;
    heroWarriorContext.clearRect(0, 0, heroWarriorFrameWidth, heroWarriorFrameHeight);
    heroWarriorContext.drawImage(
      heroWarriorSprite,
      sourceX,
      sourceY,
      heroWarriorFrameWidth,
      heroWarriorFrameHeight,
      0,
      0,
      heroWarriorFrameWidth,
      heroWarriorFrameHeight
    );
  }

  function stopRunner() {
    if (!runnerIsActive && runnerFrame === 0) return;

    runnerIsActive = false;
    runnerFrameTime = null;
    runnerFrame = 0;
    drawRunnerFrame(runnerFrame);
  }

  function startRunner() {
    if (!runnerCanvas || !runnerSprite?.naturalWidth || reducedMotionQuery.matches || runnerIsActive) return;

    runnerIsActive = true;
    runnerFrameTime = null;
    // Begin at the first running pose; frames 0–7 are a stationary lead-in.
    runnerFrame = runnerFirstRunningFrame;
    drawRunnerFrame(runnerFrame);
  }

  function advanceRunnerFromScroll(timestamp) {
    if (!runnerIsActive) return;

    // Draw only when the browser delivers scroll input. This eliminates a
    // continuous render loop and keeps the gait strictly tied to the visitor.
    // Keep the gait deliberately measured, even during fast scroll input.
    const framesPerSecond = Math.max(4, Math.min(12, 4 + runnerVelocity / 90));
    const frameInterval = 1000 / framesPerSecond;
    if (runnerFrameTime === null) {
      runnerFrameTime = timestamp;
      return;
    }

    const elapsed = timestamp - runnerFrameTime;
    if (elapsed < frameInterval) return;

    const framesToAdvance = Math.max(1, Math.floor(elapsed / frameInterval));
    // Loop only through the actual running poses, never back through the
    // stationary lead-in that caused the visible shuffle.
    runnerFrame = runnerFirstRunningFrame
      + ((runnerFrame - runnerFirstRunningFrame + framesToAdvance)
        % (runnerFrameCount - runnerFirstRunningFrame));
    runnerFrameTime = timestamp - (elapsed % frameInterval);
    drawRunnerFrame(runnerFrame);
  }

  function loadRunnerSprite() {
    if (!runnerSprite || !runnerCanvas || runnerSpriteRequested || !desktopQuery.matches || reducedMotionQuery.matches) return;

    runnerSpriteRequested = true;
    runnerSprite.decoding = 'async';
    runnerSprite.fetchPriority = 'low';
    runnerSprite.addEventListener('load', async () => {
      try {
        await runnerSprite.decode();
      } catch (error) {
        // A loaded image remains drawable when explicit decode is unavailable.
      }
      runnerSpriteReady = Boolean(runnerSprite.naturalWidth);
      drawRunnerFrame(0);
    }, { once: true });
    runnerSprite.src = runnerCanvas.dataset.sprite;
  }

  function loadHeroWarriorSprite() {
    if (!heroWarriorSprite || !heroWarriorCanvas || heroWarriorSpriteRequested || !desktopQuery.matches || reducedMotionQuery.matches) return;

    heroWarriorSpriteRequested = true;
    heroWarriorSprite.decoding = 'async';
    heroWarriorSprite.fetchPriority = 'low';
    heroWarriorSprite.addEventListener('load', async () => {
      try {
        await heroWarriorSprite.decode();
      } catch (error) {
        // A loaded image remains drawable when explicit decode is unavailable.
      }
      heroWarriorSpriteReady = Boolean(heroWarriorSprite.naturalWidth);
      renderScroll(window.scrollY);
    }, { once: true });
    heroWarriorSprite.src = heroWarriorCanvas.dataset.sprite;
  }

  function scheduleHeroWarriorPreload() {
    if (heroWarriorPreloadScheduled || heroWarriorSpriteRequested || !desktopQuery.matches || reducedMotionQuery.matches) return;

    heroWarriorPreloadScheduled = true;
    const preload = () => {
      heroWarriorPreloadScheduled = false;
      loadHeroWarriorSprite();
    };
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(preload);
    } else {
      window.setTimeout(preload, 200);
    }
  }

  function startFooterWarrior() {
    if (!footerWarriorCanvas || !footerWarriorContext) return;

    const video = document.createElement('video');
    video.src = footerWarriorCanvas.dataset.video;
    video.muted = true;
    video.loop = true;
    video.playsInline = true;
    video.preload = 'metadata';

    const renderFrame = () => {
      if (video.readyState >= HTMLMediaElement.HAVE_CURRENT_DATA) {
        // Crop the landscape source around the warrior, then remove only the
        // neon-green key. The Kenyan flag's darker green stays intact.
        footerWarriorContext.drawImage(video, 280, 0, 720, 720, 0, 0, 360, 360);
        const frame = footerWarriorContext.getImageData(0, 0, 360, 360);
        const pixels = frame.data;

        for (let index = 0; index < pixels.length; index += 4) {
          const red = pixels[index];
          const green = pixels[index + 1];
          const blue = pixels[index + 2];
          const chroma = green - Math.max(red, blue);

          if (green > 150 && red < 110 && blue < 110 && chroma > 90) {
            pixels[index + 3] = 0;
          } else if (green > 110 && red < 120 && blue < 120 && chroma > 50) {
            // Soften the keyed edge to prevent a bright green fringe.
            pixels[index + 3] = Math.max(0, Math.min(255, (90 - chroma) * 6));
          }
        }
        footerWarriorContext.putImageData(frame, 0, 0);
      }
      if (!reducedMotionQuery.matches) window.requestAnimationFrame(renderFrame);
    };

    video.addEventListener('canplay', () => {
      if (!reducedMotionQuery.matches) video.play().catch(() => {});
      window.requestAnimationFrame(renderFrame);
    }, { once: true });
    video.load();
  }

  function initBookingCalendar() {
    const calendar = document.querySelector('.appointment-layout:not([data-calendar-ready])');
    if (!calendar) return;
    calendar.dataset.calendarReady = 'true';

    let availableDates = [];
    try {
      availableDates = JSON.parse(calendar.dataset.availableDates || '[]');
    } catch (error) {
      return;
    }
    const available = new Set(availableDates);
    const grid = calendar.querySelector('[data-calendar-grid]');
    const monthLabel = calendar.querySelector('[data-calendar-month]');
    const selectedInput = calendar.querySelector('[data-selected-date]');
    const selectedLabel = calendar.querySelector('[data-selected-date-label]');
    const previous = calendar.querySelector('[data-calendar-prev]');
    const next = calendar.querySelector('[data-calendar-next]');
    const submit = calendar.querySelector('[data-booking-submit]');
    const today = new Date();
    let visibleMonth = new Date(today.getFullYear(), today.getMonth(), 1);

    if (selectedInput.value) {
      const selected = new Date(`${selectedInput.value}T00:00:00`);
      if (!Number.isNaN(selected.valueOf())) visibleMonth = new Date(selected.getFullYear(), selected.getMonth(), 1);
    } else if (availableDates.length) {
      const firstOpen = new Date(`${availableDates[0]}T00:00:00`);
      if (!Number.isNaN(firstOpen.valueOf())) visibleMonth = new Date(firstOpen.getFullYear(), firstOpen.getMonth(), 1);
    }

    const formatKey = (date) => [date.getFullYear(), String(date.getMonth() + 1).padStart(2, '0'), String(date.getDate()).padStart(2, '0')].join('-');
    const formatLabel = (date) => date.toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'long' });

    const render = () => {
      const year = visibleMonth.getFullYear();
      const month = visibleMonth.getMonth();
      const monthStart = new Date(year, month, 1);
      const days = new Date(year, month + 1, 0).getDate();
      const mondayFirstOffset = (monthStart.getDay() + 6) % 7;
      monthLabel.textContent = monthStart.toLocaleDateString(undefined, { month: 'long', year: 'numeric' });
      grid.replaceChildren();

      for (let blank = 0; blank < mondayFirstOffset; blank += 1) {
        const spacer = document.createElement('span');
        spacer.className = 'calendar-day is-empty';
        grid.append(spacer);
      }
      for (let day = 1; day <= days; day += 1) {
        const date = new Date(year, month, day);
        const key = formatKey(date);
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'calendar-day';
        button.textContent = String(day);
        if (available.has(key)) {
          button.classList.add('is-available');
          button.setAttribute('aria-label', `Book ${formatLabel(date)}`);
          if (selectedInput.value === key) button.classList.add('is-selected');
          button.addEventListener('click', () => {
            selectedInput.value = key;
            selectedLabel.textContent = `${formatLabel(date)} selected`;
            submit.disabled = false;
            render();
          });
        } else {
          button.disabled = true;
          button.setAttribute('aria-label', `${formatLabel(date)} is unavailable`);
        }
        grid.append(button);
      }
    };

    previous.addEventListener('click', () => { visibleMonth.setMonth(visibleMonth.getMonth() - 1); render(); });
    next.addEventListener('click', () => { visibleMonth.setMonth(visibleMonth.getMonth() + 1); render(); });
    submit.disabled = !available.has(selectedInput.value);
    render();
  }

  const serviceDetails = {
    'web-development': ['Web Development', 'Purpose-built websites that are fast, accessible, easy to manage, and designed to turn attention into action.'],
    branding: ['Branding', 'A clear brand foundation: strategy, positioning, visual identity, and the practical tools to use it with confidence.'],
    'graphic-design': ['Graphic Design', 'Distinct campaign, editorial, social, and print design that makes every brand touchpoint feel considered and connected.'],
    videography: ['Videography', 'Concept, direction, filming, and edits that give your brand a moving story people want to keep watching.'],
    photography: ['Photography', 'Original imagery for your people, products, spaces, and campaigns—planned around the way your audience sees your business.'],
    'digital-storytelling': ['Digital Storytelling', 'A connected narrative across words, visuals, and digital channels that makes your value instantly easier to understand.'],
    'service-portals': ['Service Portals', 'Focused online portals that make it easier for customers, teams, or partners to find information and complete important tasks.'],
    'service-systems': ['Service Systems', 'Thoughtful internal systems and workflows that reduce friction, create consistency, and help your service scale.'],
    'communication-strategy': ['Communication Strategy', 'A practical plan for what to say, who to say it to, and how each message supports your wider business goals.']
  };

  if (serviceModal && serviceModalTitle && serviceModalDescription && serviceModalTags) {
    // The horizontal track is transformed on desktop. Place the dialog at the
    // document root so its fixed position is always relative to the viewport.
    if (serviceModal.parentElement !== document.body) document.body.append(serviceModal);

    let modalTrigger = null;
    const closeServiceModal = () => {
      if (serviceModal.open) serviceModal.close();
      document.body.classList.remove('modal-open');
      if (modalTrigger) modalTrigger.focus();
    };

    document.querySelectorAll('[data-service]').forEach((card) => {
      card.addEventListener('click', () => {
        const fallback = serviceDetails[card.dataset.service] || [];
        const title = card.dataset.title || fallback[0];
        const description = card.dataset.description || fallback[1];
        if (!title) return;
        modalTrigger = card;
        serviceModalTitle.textContent = title;
        serviceModalDescription.textContent = description;
        const tags = (card.dataset.tags || '')
          .split('/')
          .map((tag) => tag.trim())
          .filter(Boolean);
        serviceModalTags.replaceChildren(...(tags.length ? tags : ['Strategy', 'Design', 'Delivery']).map((tag) => {
          const item = document.createElement('li');
          item.textContent = tag;
          return item;
        }));
        serviceModal.showModal();
        document.body.classList.add('modal-open');
        serviceModal.querySelector('.service-modal-close').focus();
      });
    });

    serviceModal.querySelector('.service-modal-close').addEventListener('click', closeServiceModal);
    serviceModal.querySelector('.service-modal-cta').addEventListener('click', closeServiceModal);
    serviceModal.addEventListener('click', (event) => {
      if (event.target === serviceModal) closeServiceModal();
    });
    serviceModal.addEventListener('cancel', () => document.body.classList.remove('modal-open'));
  }

  function cachePanelMetrics() {
    if (!desktopQuery.matches) {
      processMetrics = null;
      heroWarriorMetrics = null;
      return;
    }

    const viewWidth = window.innerWidth;
    if (rabbitWrapper && processSection) {
      const lastStep = processSection.querySelector('.process-single:last-child');
      const yellowLine = processSection.querySelector('.yellow-line');
      const maxTrackX = lastStep
        ? Math.max(0, lastStep.offsetLeft - 15)
        : Math.max(0, (yellowLine?.offsetWidth || 0) - rabbitWrapper.offsetWidth);

      processMetrics = {
        offset: processSection.offsetLeft,
        width: processSection.offsetWidth,
        maxTrackX,
        startScroll: processSection.offsetLeft - viewWidth * 0.15,
        // Keep the mascot's journey proportional to the longer editorial panel.
        scrollRange: Math.max(1400, Math.round((processSection.offsetWidth || 1380) * 0.86)),
        viewWidth,
      };
    }

    if (howSection) {
      heroWarriorMetrics = {
        offset: howSection.offsetLeft,
        width: howSection.offsetWidth,
      };
    }
  }

  function updateTrackHeights() {
    if (desktopQuery.matches) {
      // Allow track to calculate its natural flex width
      track.style.width = 'max-content';
      const trackWidth = track.scrollWidth;
      const viewportWidth = window.innerWidth - 60; // 60px sidebar
      maxScrollDistance = Math.max(0, trackWidth - viewportWidth);
      
      // Height needed to vertically scroll through the entire horizontal track
      sectionHeight.style.height = `${maxScrollDistance + window.innerHeight}px`;
      cachePanelMetrics();
      renderScroll(window.scrollY);
    } else {
      sectionHeight.style.height = '';
      track.style.width = '';
      track.style.transform = '';
      if (stickyElement) stickyElement.style.overflow = 'visible';
      clearTimeout(scrollTimeout);
      rabbitWrapper?.classList.remove('is-running');
      stopRunner();
      if (scrollRenderFrame) cancelAnimationFrame(scrollRenderFrame);
      scrollRenderFrame = null;
      cachePanelMetrics();
    }
  }

  function onScroll() {
    if (!desktopQuery.matches) return;

    scheduleHeroWarriorPreload();
    pendingScrollY = window.scrollY;
    if (scrollRenderFrame) return;

    scrollRenderFrame = requestAnimationFrame(() => {
      scrollRenderFrame = null;
      renderScroll(pendingScrollY);
    });
  }

  function renderScroll(scrollY) {
    const clampedScroll = Math.min(maxScrollDistance, Math.max(0, scrollY));
    
    // Translate the track horizontally
    track.style.transform = `translate3d(-${clampedScroll}px, 0, 0)`;

    // Process-section mascot: it runs only while the visitor is actively
    // scrolling this panel, then settles into the matching still artwork.
    if (rabbitWrapper && processMetrics) {
      const { offset, width, maxTrackX, startScroll, scrollRange, viewWidth } = processMetrics;
      const timelineProgress = Math.max(0, Math.min(1, (clampedScroll - startScroll) / scrollRange));
      const targetX = timelineProgress * maxTrackX;
      const isProcessVisible = clampedScroll + viewWidth > offset
        && clampedScroll < offset + width;
      // Do not animate while the warrior is waiting at either end of the line.
      // His running sequence begins exactly when his horizontal journey begins.
      const isMovingAlongTimeline = timelineProgress > 0 && timelineProgress < 1;
      if (clampedScroll + viewWidth * 2 > offset) loadRunnerSprite();

      // Work from the actual input delta, not a tween. That makes both the
      // runner's position and its gait stop at exactly the same time.
      const scrollDelta = scrollY - lastScrollY;
      const hasScrollInput = Math.abs(scrollDelta) > 0.1;
      if (scrollDelta < -0.1) {
        currentFacing = -1;
      } else if (scrollDelta > 0.1) {
        currentFacing = 1;
      }

      if (isProcessVisible) {
        // Use a direct update while scrolling. A long positional tween can keep
        // moving after the visitor stops, which disconnects the art from its run.
        rabbitWrapper.style.transform = `translate3d(${targetX}px, 0, 0) scaleX(${currentFacing})`;

        if (isMovingAlongTimeline && hasScrollInput && !reducedMotionQuery.matches) {
          loadRunnerSprite();
          if (runnerSpriteReady) {
            const scrollTime = performance.now();
            const elapsed = Math.max(16, scrollTime - lastRunnerScrollTime);
            runnerVelocity = Math.abs(scrollDelta) / elapsed * 1000;
            lastRunnerScrollTime = scrollTime;

            rabbitWrapper.classList.add('is-running');
            startRunner();
            advanceRunnerFromScroll(scrollTime);
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
              rabbitWrapper.classList.remove('is-running');
              stopRunner();
            }, 120);
          }
        } else if (!isMovingAlongTimeline) {
          clearTimeout(scrollTimeout);
          rabbitWrapper.classList.remove('is-running');
          stopRunner();
        }
      } else {
        clearTimeout(scrollTimeout);
        rabbitWrapper.classList.remove('is-running');
        stopRunner();
      }
    }

    // The supplied animation is scrubbed by this panel's scroll position. It
    // never plays on its own: stop scrolling and the warrior stops immediately.
    if (heroWarriorCanvas && heroWarriorMetrics) {
      const { offset, width } = heroWarriorMetrics;
      // Start as soon as this panel enters the viewport and finish when it
      // leaves it. This makes the animation perceptible throughout the panel,
      // rather than waiting for the panel's left edge to reach the viewport.
      const visibleStart = offset - window.innerWidth;
      const progress = Math.max(0, Math.min(1, (clampedScroll - visibleStart) / Math.max(width + window.innerWidth, 1)));
      const isHowSectionVisible = clampedScroll + window.innerWidth > offset && clampedScroll < offset + width;
      if (scrollY > 0 && isHowSectionVisible) loadHeroWarriorSprite();
      drawHeroWarriorFrame(reducedMotionQuery.matches ? 0 : progress * (heroWarriorFrameCount - 1));
    }

    lastScrollY = scrollY;
  }

  function scheduleTrackUpdate() {
    if (resizeFrame) cancelAnimationFrame(resizeFrame);
    resizeFrame = requestAnimationFrame(() => {
      resizeFrame = null;
      updateTrackHeights();
    });
  }

  // Smooth click navigation for anchor links
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href*="#"]');
    if (!link) return;

    const href = link.getAttribute('href');
    const hashIndex = href.indexOf('#');
    if (hashIndex === -1) return;

    const targetId = href.slice(hashIndex + 1);
    if (!targetId) return;

    const targetElement = document.getElementById(targetId);
    if (!targetElement) return;

    if (desktopQuery.matches && track.contains(targetElement)) {
      event.preventDefault();
      
      // Calculate scroll offset based on element horizontal position
      const targetLeft = targetElement.offsetLeft;
      const scrollPos = Math.min(maxScrollDistance, Math.max(0, targetLeft));
      
      window.scrollTo({
        top: scrollPos,
        behavior: 'smooth'
      });
      history.pushState(null, '', `#${targetId}`);
    } else if (!desktopQuery.matches) {
      event.preventDefault();
      targetElement.scrollIntoView({ behavior: 'smooth' });
      history.pushState(null, '', `#${targetId}`);
    }
  });

  // Initial setup
  updateTrackHeights();
  startFooterWarrior();
  initBookingCalendar();

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', scheduleTrackUpdate, { passive: true });
  desktopQuery.addEventListener('change', scheduleTrackUpdate);

  // If page loaded with a hash, jump to it
  if (window.location.hash) {
    setTimeout(() => {
      const target = document.querySelector(window.location.hash);
      if (target && desktopQuery.matches) {
        window.scrollTo({ top: target.offsetLeft, behavior: 'auto' });
      } else if (target) {
        target.scrollIntoView({ behavior: 'auto', block: 'start' });
      }
    }, 150);
  }

  // HTMX focus and error management
  document.body.addEventListener('htmx:afterSwap', (event) => {
    if (event.detail.target.id === 'inquiry-form') {
      const status = document.querySelector('.success-message, .error-message');
      if (status) {
        status.setAttribute('tabindex', '-1');
        status.focus();
      }
    }
    if (event.detail.target.id === 'appointment-booking') initBookingCalendar();
  });

  ['htmx:responseError', 'htmx:sendError'].forEach((name) => {
    document.body.addEventListener(name, (event) => {
      const error = event.detail.elt.querySelector('.request-error');
      if (error) {
        error.hidden = false;
        error.setAttribute('role', 'alert');
      }
    });
  });
});
