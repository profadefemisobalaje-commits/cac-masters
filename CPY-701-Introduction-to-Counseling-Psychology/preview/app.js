/* CPY 701 lecture preview player */
(function () {
  const D = window.CPY701;
  const $ = (id) => document.getElementById(id);
  const stage = $('stage'), img = $('slide'), video = $('video'), cap = $('caption');
  const seek = $('seek'), clock = $('clock'), playBtn = $('playBtn'), modeBtn = $('modeBtn');
  let W = null, mode = 'slides', t = 0, playing = false, last = 0, curSlide = -1, raf = null;

  const fmt = (s) => {
    s = Math.max(0, s);
    const m = Math.floor(s / 60), ss = Math.floor(s % 60);
    return String(m).padStart(2, '0') + ':' + String(ss).padStart(2, '0');
  };

  function tabs() {
    const nav = $('tabs');
    nav.innerHTML = '';
    D.weeks.forEach((w) => {
      const b = document.createElement('button');
      b.textContent = 'Week ' + w.num;
      b.title = w.title;
      b.onclick = () => load(w.id);
      b.dataset.id = w.id;
      nav.appendChild(b);
    });
  }

  function load(id) {
    W = D.weeks.find((w) => w.id === id);
    mode = 'slides';
    t = 0; playing = false; curSlide = -1;
    document.querySelectorAll('#tabs button').forEach((b) => b.classList.toggle('active', b.dataset.id === id));
    // outline
    const ol = $('outline');
    ol.innerHTML = '';
    W.slides.forEach((s, i) => {
      const li = document.createElement('li');
      li.textContent = (i + 1) + '. ' + s.title;
      li.onclick = () => { goto(i); };
      ol.appendChild(li);
    });
    // files
    const up = W.id.toUpperCase();
    const fl = $('files');
    fl.innerHTML = '';
    const add = (href, label) => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = href; a.textContent = label; a.download = '';
      li.appendChild(a); fl.appendChild(li);
    };
    if (W.mode === 'narrated') {
      add(W.video, 'Narrated lecture video (MP4, 1080p)');
      add('/dist/' + W.id + '-captions.srt', 'Captions (SRT)');
      add(W.vtt, 'Captions (WebVTT)');
    } else {
      const li = document.createElement('li');
      li.innerHTML = '<em>Narrated MP4 delivered earlier — slide playback shown here.</em>';
      fl.appendChild(li);
    }
    add('/dist/CPY701-' + up + '-slides.pptx', 'Editable slide deck (PPTX)');
    // note + badge
    $('weekNote').textContent = W.mode === 'narrated'
      ? 'Week ' + W.num + ' · ' + W.title + ' — full narrated video available; use “Full video” for the lecture film with embedded captions, or the slide player to step through slides with live captions.'
      : 'Week ' + W.num + ' · ' + W.title + ' — caption-synced slide playback (the narrated MP4 for this week was delivered earlier and is not stored in this sandbox).';
    modeBtn.style.display = W.mode === 'narrated' ? '' : 'none';
    // video element
    if (W.mode === 'narrated') {
      video.src = W.video;
      video.innerHTML = '<track kind="subtitles" src="' + W.vtt + '" srclang="en" label="English" default>';
    }
    applyMode();
    seek.max = 1000;
    update(true);
  }

  function applyMode() {
    const isVid = mode === 'video' && W.mode === 'narrated';
    video.style.display = isVid ? '' : 'none';
    img.style.display = isVid ? 'none' : '';
    cap.style.display = isVid ? 'none' : '';
    ['playBtn', 'prevBtn', 'nextBtn'].forEach((i) => { $(i).style.display = isVid ? 'none' : ''; });
    seek.style.display = isVid ? 'none' : '';
    clock.style.display = isVid ? 'none' : '';
    modeBtn.textContent = isVid ? 'Slide player' : 'Full video';
    $('modeBadge').textContent = 'WEEK ' + W.num + ' · ' + (isVid ? 'NARRATED VIDEO' : 'SLIDE PLAYER');
    if (isVid) { video.currentTime = t; video.play(); }
    else { video.pause(); }
  }

  function slideAt(time) {
    let idx = 0;
    for (let i = 0; i < W.slides.length; i++) if (time >= W.slides[i].start) idx = i;
    return idx;
  }

  function update(force) {
    const isVid = mode === 'video' && W.mode === 'narrated';
    if (isVid) return;
    const i = slideAt(t);
    if (i !== curSlide || force) {
      curSlide = i;
      img.src = W.slides[i].file;
      document.querySelectorAll('#outline li').forEach((li, k) => li.classList.toggle('now', k === i));
    }
    const cue = W.cues.find((c) => t >= c.s && t < c.e);
    cap.textContent = cue ? cue.t : '';
    clock.textContent = fmt(t) + ' / ' + fmt(W.duration);
    seek.value = Math.round((t / W.duration) * 1000);
  }

  function loop(ts) {
    raf = requestAnimationFrame(loop);
    if (!playing) { last = ts; return; }
    const dt = (ts - last) / 1000; last = ts;
    t = Math.min(W.duration, t + dt);
    if (t >= W.duration) { playing = false; playBtn.textContent = '▶'; }
    update(false);
  }

  function goto(i) {
    t = W.slides[i].start + 0.01;
    if (mode === 'video' && W.mode === 'narrated') video.currentTime = t;
    update(true);
  }

  playBtn.onclick = () => {
    playing = !playing;
    playBtn.textContent = playing ? '❚❚' : '▶';
    if (playing && t >= W.duration) t = 0;
  };
  $('prevBtn').onclick = () => goto(Math.max(0, slideAt(t) - 1));
  $('nextBtn').onclick = () => goto(Math.min(W.slides.length - 1, slideAt(t) + 1));
  seek.oninput = () => { t = (seek.value / 1000) * W.duration; update(true); };
  modeBtn.onclick = () => { mode = mode === 'video' ? 'slides' : 'video'; applyMode(); };
  video.addEventListener('timeupdate', () => { t = video.currentTime; });
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') return;
    if (e.code === 'Space') { e.preventDefault(); playBtn.onclick(); }
    if (e.code === 'ArrowRight') $('nextBtn').onclick();
    if (e.code === 'ArrowLeft') $('prevBtn').onclick();
  });

  tabs();
  load(D.weeks[0].id);
  raf = requestAnimationFrame(loop);
})();
