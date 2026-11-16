import test from 'node:test';
import assert from 'node:assert/strict';

test('four selectors replay exact archived attenuation values and signed bar directions', async () => {
  const listeners = {};
  const attrs = {};
  const make = () => ({
    textContent: '', value: '', style: {},
    classList: {
      classes: new Set(),
      toggle(key, enabled) { enabled ? this.classes.add(key) : this.classes.delete(key); },
      contains(key) { return this.classes.has(key); },
    },
    setAttribute(key, value) { attrs[key] = value; },
  });
  const output = make();
  const tag = make();
  const heading = make();
  const description = make();
  const meter = make();
  const track = make();
  const buttons = Object.fromEntries(['original','reworded','formal','terse'].map(id => [id, {
    dataset: { wording: id },
    pressed: 'false',
    setAttribute(key, value) { if (key === 'aria-pressed') this.pressed = value; },
    addEventListener(event, callback) { listeners[id] = callback; },
  }]));
  const panelNodes = {
    '#contrastOutput': output,
    '#wordingTag': tag,
    '#wordingHeading': heading,
    '#wordingDescription': description,
    '#contrastMeter': meter,
    '.signed-track': track,
  };
  const panel = {
    dataset: {},
    querySelector(selector) { return panelNodes[selector] || null; },
    querySelectorAll(selector) { return selector === '[data-wording]' ? Object.values(buttons) : []; },
  };

  globalThis.document = {
    querySelector(selector) { return selector === '.experiment-panel' ? panel : null; },
    querySelectorAll() { return []; },
  };
  globalThis.window = {};
  await import('../docs/site.js');

  for (const [id, value, tone, width] of [
    ['original', '+0.206', 'positive', 41.10849],
    ['reworded', '−0.021', 'negative', 4.13466],
    ['formal', '−0.046', 'negative', 9.16377],
    ['terse', '−0.002', 'negative', .46731],
  ]) {
    listeners[id]();
    assert.equal(output.textContent, value);
    assert.equal(panel.dataset.tone, tone);
    assert.ok(Math.abs(Number.parseFloat(meter.style.width) - width) < .0005);
    assert.ok(meter.classList.contains(tone));
    assert.equal(buttons[id].pressed, 'true');
    assert.equal(Object.values(buttons).filter(button => button.pressed === 'true').length, 1);
    assert.ok(description.textContent.toLowerCase().includes('attenuation') || description.textContent.toLowerCase().includes('phrasing'));
    assert.ok(tag.textContent.includes(id.toUpperCase()));
  }
});
