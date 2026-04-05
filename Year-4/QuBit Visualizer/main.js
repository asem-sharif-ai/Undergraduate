// Star
(function () {
  const container = document.getElementById('stars');
  for (let i = 0; i < 150; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    const size = Math.random() * 1.8 + 0.4;
    s.style.cssText = `
      left:${Math.random() * 100}%;top:${Math.random() * 100}%;
      width:${size}px;height:${size}px;
      --d:${2 + Math.random() * 4}s;--delay:${-Math.random() * 5}s;
      --min:${0.05 + Math.random() * 0.12};--max:${0.35 + Math.random() * 0.5};
    `;
    container.appendChild(s);
  }
})();

// Quantum State
const state = {
  theta: 0,
  phi: 0,
};

function blochVector() {
  return {
    x: Math.sin(state.theta) * Math.cos(state.phi),
    y: Math.sin(state.theta) * Math.sin(state.phi),
    z: Math.cos(state.theta),
  };
}

// Canvas Setup
const canvas = document.getElementById('sphere');
const ctx = canvas.getContext('2d');

let W, H, cx, cy, R;

function resize() {
  const area = canvas.parentElement;
  W = area.clientWidth;
  H = area.clientHeight;
  const minDim = Math.min(W, H);
  canvas.width = W;
  canvas.height = H;
  R = minDim * 0.36;
  cx = W / 2;
  cy = H / 2;
}
resize();
window.addEventListener('resize', resize);

// Camer
let camAzimuth = -Math.PI / 6;
let camElevation = Math.PI / 5;
let autoRotate = true;
let showTrails = true;
let showGrid = true;

document.getElementById('toggle-rotate').addEventListener('change', e => { autoRotate = e.target.checked; });
document.getElementById('toggle-trails').addEventListener('change', e => {
  showTrails = e.target.checked;
  if (!showTrails) trails.length = 0;
});
document.getElementById('toggle-grid').addEventListener('change', e => { showGrid = e.target.checked; });

// Mouse drag
let dragging = false, lastMX = 0, lastMY = 0;
canvas.addEventListener('mousedown', e => {
  dragging = true; lastMX = e.clientX; lastMY = e.clientY;
  autoRotate = false;
  document.getElementById('toggle-rotate').checked = false;
});
canvas.addEventListener('mousemove', e => {
  if (!dragging) return;
  camAzimuth += (e.clientX - lastMX) * 0.008;
  camElevation -= (e.clientY - lastMY) * 0.008;
  camElevation = Math.max(-Math.PI / 2 + 0.05, Math.min(Math.PI / 2 - 0.05, camElevation));
  lastMX = e.clientX; lastMY = e.clientY;
});
canvas.addEventListener('mouseup', () => dragging = false);
canvas.addEventListener('mouseleave', () => dragging = false);

// Touch
canvas.addEventListener('touchstart', e => {
  dragging = true;
  lastMX = e.touches[0].clientX;
  lastMY = e.touches[0].clientY;
  autoRotate = false;
}, { passive: true });
canvas.addEventListener('touchmove', e => {
  if (!dragging) return;
  camAzimuth += (e.touches[0].clientX - lastMX) * 0.008;
  camElevation -= (e.touches[0].clientY - lastMY) * 0.008;
  camElevation = Math.max(-Math.PI / 2 + 0.05, Math.min(Math.PI / 2 - 0.05, camElevation));
  lastMX = e.touches[0].clientX;
  lastMY = e.touches[0].clientY;
}, { passive: true });
canvas.addEventListener('touchend', () => dragging = false);

// 3D Projection──
function project(x3, y3, z3) {
  const cosA = Math.cos(camAzimuth), sinA = Math.sin(camAzimuth);
  const cosE = Math.cos(camElevation), sinE = Math.sin(camElevation);
  const x1 = x3 * cosA - z3 * sinA;
  const y1 = y3;
  const z1 = x3 * sinA + z3 * cosA;
  const x2 = x1;
  const y2 = y1 * cosE - z1 * sinE;
  const z2 = y1 * sinE + z1 * cosE;
  const fov = 3.5;
  const scale = fov / (fov + z2);
  return { px: cx + x2 * R * scale, py: cy - y2 * R * scale, z: z2, scale };
}

function depth(x3, y3, z3) {
  return project(x3, y3, z3).z;
}

// Trail
const trails = [];
const MAX_TRAIL = 120;

// Dra──
function draw(t) {
  ctx.clearRect(0, 0, W, H);
  const bv = blochVector();

  // Trails
  if (showTrails && trails.length > 1) {
    for (let i = 1; i < trails.length; i++) {
      const a = trails[i - 1];
      const b = trails[i];
      const pa = project(a.x, a.y, a.z);
      const pb = project(b.x, b.y, b.z);
      const alpha = (i / trails.length) * 0.6;
      ctx.beginPath();
      ctx.moveTo(pa.px, pa.py);
      ctx.lineTo(pb.px, pb.py);
      ctx.strokeStyle = `rgba(0,212,255,${alpha})`;
      ctx.lineWidth = 1.5 * (i / trails.length);
      ctx.stroke();
    }
  }

  // Sphere fill
  const grad = ctx.createRadialGradient(cx - R * 0.25, cy - R * 0.25, R * 0.05, cx, cy, R);
  grad.addColorStop(0, 'rgba(0,30,80,0.35)');
  grad.addColorStop(0.6, 'rgba(0,15,50,0.15)');
  grad.addColorStop(1, 'rgba(0,5,20,0.05)');
  ctx.beginPath();
  ctx.arc(cx, cy, R, 0, Math.PI * 2);
  ctx.fillStyle = grad;
  ctx.fill();

  if (showGrid) {
    const latLines = [-60, -30, 0, 30, 60];
    latLines.forEach(deg => {
      const lat = deg * Math.PI / 180;
      const r = Math.cos(lat);
      const yOffset = Math.sin(lat);
      drawEllipse(0, yOffset, 0, r, 0, 1, 0, 'rgba(13,80,160,0.25)', 1);
    });
    for (let i = 0; i < 6; i++) {
      drawGreatCircle(i * Math.PI / 6, 'rgba(13,80,160,0.2)', 1);
    }
    drawEllipse(0, 0, 0, 1, 0, 1, 0, 'rgba(0,212,255,0.18)', 1.5);
  }

  // Sphere outline
  ctx.beginPath();
  ctx.arc(cx, cy, R, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(0,212,255,0.12)';
  ctx.lineWidth = 1;
  ctx.stroke();

  // Axes
  drawAxis(1, 0, 0, 'rgba(0,212,255,0.9)', '+X', '-X');
  drawAxis(0, 1, 0, 'rgba(0,255,170,0.8)', '+Y', '-Y');
  drawAxis(0, 0, 1, 'rgba(255,60,110,0.8)', '|0⟩', '|1⟩');

  // State vector
  const sp = project(bv.x, bv.y, bv.z);

  // Center glow
  const glowGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 0.15);
  glowGrad.addColorStop(0, 'rgba(0,212,255,0.08)');
  glowGrad.addColorStop(1, 'rgba(0,212,255,0)');
  ctx.beginPath();
  ctx.arc(cx, cy, R * 0.15, 0, Math.PI * 2);
  ctx.fillStyle = glowGrad;
  ctx.fill();

  // Projection dashes
  const projXY = project(bv.x, bv.y, 0);
  ctx.setLineDash([3, 5]);
  ctx.beginPath();
  ctx.moveTo(projXY.px, projXY.py);
  ctx.lineTo(sp.px, sp.py);
  ctx.strokeStyle = 'rgba(0,212,255,0.2)';
  ctx.lineWidth = 1;
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(projXY.px, projXY.py);
  ctx.stroke();
  ctx.setLineDash([]);

  // Vector line
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(sp.px, sp.py);
  const lineGrad = ctx.createLinearGradient(cx, cy, sp.px, sp.py);
  lineGrad.addColorStop(0, 'rgba(0,212,255,0.3)');
  lineGrad.addColorStop(1, 'rgba(0,212,255,1)');
  ctx.strokeStyle = lineGrad;
  ctx.lineWidth = 2.5;
  ctx.stroke();

  drawArrow(cx, cy, sp.px, sp.py, '#00d4ff');

  // State dot
  const dotR = 7 * sp.scale;
  const dotGrad = ctx.createRadialGradient(sp.px, sp.py, 0, sp.px, sp.py, dotR * 2);
  dotGrad.addColorStop(0, '#ffffff');
  dotGrad.addColorStop(0.3, '#00d4ff');
  dotGrad.addColorStop(1, 'rgba(0,212,255,0)');
  ctx.beginPath();
  ctx.arc(sp.px, sp.py, dotR * 2, 0, Math.PI * 2);
  ctx.fillStyle = dotGrad;
  ctx.fill();
  ctx.beginPath();
  ctx.arc(sp.px, sp.py, dotR * 0.6, 0, Math.PI * 2);
  ctx.fillStyle = '#ffffff';
  ctx.fill();

  // Gloss
  const gloss = ctx.createRadialGradient(cx - R * 0.3, cy - R * 0.3, 0, cx - R * 0.1, cy - R * 0.1, R * 0.6);
  gloss.addColorStop(0, 'rgba(255,255,255,0.04)');
  gloss.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.beginPath();
  ctx.arc(cx, cy, R, 0, Math.PI * 2);
  ctx.fillStyle = gloss;
  ctx.fill();
}

function drawAxis(ax, ay, az, color, posLabel, negLabel) {
  const p1 = project(ax * 1.18, ay * 1.18, az * 1.18);
  const p2 = project(-ax * 1.18, -ay * 1.18, -az * 1.18);
  const pc = project(0, 0, 0);

  ctx.setLineDash([3, 5]);
  ctx.beginPath();
  ctx.moveTo(pc.px, pc.py);
  ctx.lineTo(p2.px, p2.py);
  ctx.strokeStyle = color.replace(/[\d.]+\)$/, '0.25)');
  ctx.lineWidth = 1;
  ctx.stroke();
  ctx.setLineDash([]);

  ctx.beginPath();
  ctx.moveTo(pc.px, pc.py);
  ctx.lineTo(p1.px, p1.py);
  ctx.strokeStyle = color.replace(/[\d.]+\)$/, '0.6)');
  ctx.lineWidth = 1.5;
  ctx.stroke();

  ctx.font = `bold 11px 'Share Tech Mono', monospace`;
  ctx.fillStyle = color;
  ctx.textAlign = 'center';
  ctx.fillText(posLabel, p1.px, p1.py - 8);
  ctx.fillStyle = color.replace(/[\d.]+\)$/, '0.4)');
  ctx.fillText(negLabel, p2.px, p2.py + 14);
}

function drawArrow(x1, y1, x2, y2, color) {
  const angle = Math.atan2(y2 - y1, x2 - x1);
  const size = 10;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - size * Math.cos(angle - Math.PI / 6), y2 - size * Math.sin(angle - Math.PI / 6));
  ctx.lineTo(x2 - size * Math.cos(angle + Math.PI / 6), y2 - size * Math.sin(angle + Math.PI / 6));
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
}

function drawEllipse(ox, oy, oz, rx, nx, ny, nz, color, lw) {
  const steps = 64;
  const pts = [];
  for (let i = 0; i <= steps; i++) {
    const a = (i / steps) * Math.PI * 2;
    const cos = Math.cos(a), sin = Math.sin(a);
    const x3 = ox + rx * cos;
    const z3 = oz + rx * sin * (Math.abs(nz) > 0.5 ? 1 : 0);
    const y3 = oy + rx * sin * (Math.abs(ny) > 0.5 ? 1 : 0);
    pts.push(project(x3, y3, z3));
  }
  ctx.beginPath();
  pts.forEach((p, i) => i === 0 ? ctx.moveTo(p.px, p.py) : ctx.lineTo(p.px, p.py));
  ctx.strokeStyle = color;
  ctx.lineWidth = lw;
  ctx.stroke();
}

function drawGreatCircle(ang, color, lw) {
  const steps = 64;
  const pts = [];
  for (let i = 0; i <= steps; i++) {
    const a = (i / steps) * Math.PI * 2;
    const x = Math.sin(a) * Math.cos(ang);
    const y = Math.cos(a);
    const z = Math.sin(a) * Math.sin(ang);
    pts.push(project(x, y, z));
  }
  ctx.beginPath();
  pts.forEach((p, i) => i === 0 ? ctx.moveTo(p.px, p.py) : ctx.lineTo(p.px, p.py));
  ctx.strokeStyle = color;
  ctx.lineWidth = lw;
  ctx.stroke();
}

// Update UI
function updateUI() {
  const bv = blochVector();
  const cosH = Math.cos(state.theta / 2);
  const sinH = Math.sin(state.theta / 2);
  const p0 = cosH * cosH;
  const p1 = sinH * sinH;

  document.getElementById('stat-alpha').textContent = cosH.toFixed(4);
  document.getElementById('stat-beta').textContent = sinH.toFixed(4);
  document.getElementById('stat-phase').textContent = (state.phi * 180 / Math.PI).toFixed(2) + '°';

  document.getElementById('pct-zero').textContent = (p0 * 100).toFixed(1) + '%';
  document.getElementById('pct-one').textContent = (p1 * 100).toFixed(1) + '%';
  document.getElementById('bar-zero').style.width = (p0 * 100) + '%';
  document.getElementById('bar-one').style.width = (p1 * 100) + '%';

  document.getElementById('val-bx').textContent = bv.x.toFixed(3);
  document.getElementById('val-by').textContent = bv.y.toFixed(3);
  document.getElementById('val-bz').textContent = bv.z.toFixed(3);

  updateCoordBar('bar-bx', bv.x, 'var(--accent)');
  updateCoordBar('bar-by', bv.y, 'var(--accent4)');
  updateCoordBar('bar-bz', bv.z, 'var(--accent3)');

  const thDeg = Math.round(state.theta * 180 / Math.PI);
  const phDeg = Math.round(((state.phi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI) * 180 / Math.PI);
  document.getElementById('sl-theta').value = thDeg;
  document.getElementById('sl-phi').value = phDeg;
  updateSliderFill(document.getElementById('sl-theta'), 0, 180);
  updateSliderFill(document.getElementById('sl-phi'), 0, 360);
  document.getElementById('val-theta').textContent = thDeg + '°';
  document.getElementById('val-phi').textContent = phDeg + '°';
}

function updateCoordBar(id, val, color) {
  const el = document.getElementById(id);
  const pct = (val + 1) / 2 * 100;
  if (val >= 0) {
    el.style.left = '50%';
    el.style.width = (pct - 50) + '%';
  } else {
    el.style.left = pct + '%';
    el.style.width = (50 - pct) + '%';
  }
  el.style.background = color;
}

function updateSliderFill(el, min, max) {
  const pct = ((el.value - min) / (max - min)) * 100;
  el.style.setProperty('--pct', pct + '%');
}

// Animation
let animFrame = null;
let animating = false;

function animateTo(theta, phi, onDone) {
  let dPhi = ((phi - state.phi) + 3 * Math.PI) % (2 * Math.PI) - Math.PI;
  const startTheta = state.theta;
  const startPhi = state.phi;
  const endTheta = theta;
  const endPhi = startPhi + dPhi;
  const startTime = performance.now();
  const duration = 500;

  animating = true;

  function step(now) {
    const t = Math.min((now - startTime) / duration, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    state.theta = startTheta + (endTheta - startTheta) * ease;
    state.phi = startPhi + (endPhi - startPhi) * ease;
    if (showTrails) trails.push({ ...blochVector() });
    if (trails.length > MAX_TRAIL) trails.shift();
    if (t < 1) {
      animFrame = requestAnimationFrame(step);
    } else {
      animating = false;
      if (onDone) onDone();
    }
  }
  if (animFrame) cancelAnimationFrame(animFrame);
  animFrame = requestAnimationFrame(step);
}

// Sliders
document.getElementById('sl-theta').addEventListener('input', function () {
  state.theta = this.value * Math.PI / 180;
  updateSliderFill(this, 0, 180);
  document.getElementById('val-theta').textContent = this.value + '°';
  if (showTrails) { trails.push({ ...blochVector() }); if (trails.length > MAX_TRAIL) trails.shift(); }
});

document.getElementById('sl-phi').addEventListener('input', function () {
  state.phi = this.value * Math.PI / 180;
  updateSliderFill(this, 0, 360);
  document.getElementById('val-phi').textContent = this.value + '°';
  if (showTrails) { trails.push({ ...blochVector() }); if (trails.length > MAX_TRAIL) trails.shift(); }
});

// Basis States
const basisStates = {
  '|0⟩': [0, 0],
  '|1⟩': [Math.PI, 0],
  '|+⟩': [Math.PI / 2, 0],
  '|-⟩': [Math.PI / 2, Math.PI],
  '|i⟩': [Math.PI / 2, Math.PI / 2],
  '|-i⟩': [Math.PI / 2, -Math.PI / 2],
};

document.querySelectorAll('.state-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.state-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const [theta, phi] = basisStates[this.dataset.state];
    trails.length = 0;
    animateTo(theta, phi);
  });
});

// Quantum Gates
function applyGate(gate) {
  const th = state.theta;
  const ph = state.phi;
  let newTh = th, newPh = ph;

  switch (gate) {
    case 'X': newTh = Math.PI - th; newPh = ph + Math.PI; break;
    case 'Y': newTh = Math.PI - th; newPh = -ph; break;
    case 'Z': newPh = ph + Math.PI; break;
    case 'H': {
      const bv = blochVector();
      newTh = Math.acos(Math.max(-1, Math.min(1, bv.x)));
      newPh = Math.atan2(-bv.y, bv.z);
      break;
    }
    case 'S': newPh = ph + Math.PI / 2; break;
    case 'T': newPh = ph + Math.PI / 4; break;
    case 'Rx': {
      const bv = blochVector();
      const angle = Math.PI / 2;
      const c = Math.cos(angle / 2), s = Math.sin(angle / 2);
      const ny = bv.y * c + bv.z * s;
      const nz = -bv.y * s + bv.z * c;
      newTh = Math.acos(Math.max(-1, Math.min(1, nz)));
      newPh = Math.atan2(ny, bv.x);
      break;
    }
    case 'Ry': {
      const bv = blochVector();
      const angle = Math.PI / 2;
      const c = Math.cos(angle / 2), s = Math.sin(angle / 2);
      const nx = bv.x * c - bv.z * s;
      const nz = bv.x * s + bv.z * c;
      newTh = Math.acos(Math.max(-1, Math.min(1, nz)));
      newPh = Math.atan2(bv.y, nx);
      break;
    }
    case 'Rz': newPh = ph + Math.PI / 2; break;
  }

  document.querySelectorAll('.state-btn').forEach(b => b.classList.remove('active'));
  animateTo(newTh, newPh);
}

document.querySelectorAll('.gate-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    applyGate(this.dataset.gate);
    this.style.transform = 'scale(0.88)';
    setTimeout(() => this.style.transform = '', 150);
  });
});

// Measurement
document.getElementById('btn-measure').addEventListener('click', () => {
  const bv = blochVector();
  const p0 = (1 + bv.z) / 2;
  const outcome = Math.random() < p0 ? 0 : 1;

  const el = document.getElementById('measure-result');
  el.textContent = outcome;
  el.style.color = outcome === 0 ? '#00d4ff' : '#ff3c6e';

  el.style.transition = 'opacity 0.1s, transform 0.1s';
  el.style.opacity = '1';
  el.style.transform = 'translate(-50%, -50%) scale(1.2)';
  setTimeout(() => { el.style.transform = 'translate(-50%, -50%) scale(1)'; }, 100);
  setTimeout(() => { el.style.opacity = '0'; }, 1200);

  trails.length = 0;
  animateTo(outcome === 0 ? 0 : Math.PI, 0);
});

// Main Loop
let lastTime = 0;
function loop(t) {
  const dt = t - lastTime;
  lastTime = t;
  if (autoRotate && !dragging && !animating) {
    camAzimuth += dt * 0.0003;
  }
  draw(t);
  updateUI();
  requestAnimationFrame(loop);
}

updateSliderFill(document.getElementById('sl-theta'), 0, 180);
updateSliderFill(document.getElementById('sl-phi'), 0, 360);
state.theta = 0;
state.phi = 0;
document.querySelector('[data-state="|0⟩"]').classList.add('active');
requestAnimationFrame(loop);
