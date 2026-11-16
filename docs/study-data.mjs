/**
 * Frozen, source-verified CI V2.1 attenuation contrasts.
 * These are source-table measurements, not answer accuracy or model reruns.
 */
export const STUDY = Object.freeze({
  questionUnits: 32,
  factorialCells: 1024,
  directions: 2,
  wordingVariants: 4,
  instructionTemplates: 4,
  metric: 'attenuation',
  pairedMean: 0.2262157364724729,
  pairedBootstrap95: Object.freeze([0.18425554478965706, 0.2741488260786011]),
  rotatedOriginal: -0.023924244812204388,
  independentModelReplay: false,
  doi: '10.5281/zenodo.24280041',
  sourceHash: '303c7a42509d2480107591bfd3c5c3467f657233aa272fba546fa73a2d374f77',
});

export const WORDING_CONTRASTS = Object.freeze([
  Object.freeze({ id: 'original', label: 'Original', value: 0.20554245016147377,
    heading: 'A strong positive response',
    explanation: 'The archived signed edit exhibited a +0.206 average math-plus-format versus generic attenuation contrast under the original wording.' }),
  Object.freeze({ id: 'reworded', label: 'Reworded', value: -0.020673286310999125,
    heading: 'The effect changes sign',
    explanation: 'When the question was reworded, the same archived comparison was −0.021 on average. Phrasing and token positions changed together.' }),
  Object.freeze({ id: 'formal', label: 'Formal', value: -0.04581887087037813,
    heading: 'A more negative contrast',
    explanation: 'Formal phrasing produced an average attenuation contrast of −0.046 in this historical panel.' }),
  Object.freeze({ id: 'terse', label: 'Terse', value: -0.002336535904948797,
    heading: 'Almost no average contrast',
    explanation: 'The terse variant was close to zero at −0.002. This is an attenuation response, not an answer-correctness rate.' }),
]);

export function formatContrast(value) {
  const formatted = Math.abs(value).toFixed(3);
  return `${value < 0 ? '−' : '+'}${formatted}`;
}

export function relativeMagnitude(value) {
  if (!Number.isFinite(value)) return 0;
  return Math.max(0, Math.min(100, (Math.abs(value) / 0.25) * 100));
}
