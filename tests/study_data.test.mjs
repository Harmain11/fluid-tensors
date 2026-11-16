import test from 'node:test';
import assert from 'node:assert/strict';

import { STUDY, WORDING_CONTRASTS, formatContrast, relativeMagnitude } from '../docs/study-data.mjs';

test('archived contrast explorer exposes the four exact signed-edit means', () => {
  assert.deepEqual(
    WORDING_CONTRASTS.map(({ id, value }) => [id, value]),
    [
      ['original', 0.20554245016147377],
      ['reworded', -0.020673286310999125],
      ['formal', -0.04581887087037813],
      ['terse', -0.002336535904948797],
    ],
  );
});

test('the metadata calls the archival measurement attenuation, not accuracy', () => {
  assert.equal(STUDY.questionUnits, 32);
  assert.equal(STUDY.factorialCells, 1024);
  assert.equal(STUDY.metric, 'attenuation');
  assert.equal(STUDY.pairedMean, 0.2262157364724729);
  assert.equal(STUDY.rotatedOriginal, -0.023924244812204388);
  assert.equal(STUDY.doi, '10.5281/zenodo.24280041');
  assert.equal(STUDY.independentModelReplay, false);
});

test('contrast formatting preserves signs, including the near-zero terse condition', () => {
  assert.equal(formatContrast(0.20554245016147377), '+0.206');
  assert.equal(formatContrast(-0.020673286310999125), '−0.021');
  assert.equal(formatContrast(-0.002336535904948797), '−0.002');
});

test('meter lengths remain bounded for tiny, zero and large magnitudes', () => {
  assert.equal(relativeMagnitude(0), 0);
  assert.equal(relativeMagnitude(0.25), 100);
  assert.equal(relativeMagnitude(-0.5), 100);
  assert.ok(relativeMagnitude(-0.002336535904948797) > 0);
});
