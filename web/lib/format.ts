// Shared figure formatting. Savings are pence-based from the API; show small
// values in p and larger in £, and grams vs kg — always as tabular mono figures.
// Sign is carried separately so the £/p threshold keys off magnitude: a negative
// saving is a real result, not a formatting edge case.
export function money(p: number): string {
  const rounded = Math.round(p);
  const sign = rounded < 0 ? "-" : "";
  const abs = Math.abs(p);
  return abs >= 100 ? `${sign}£${(abs / 100).toFixed(2)}` : `${sign}${Math.abs(rounded)}p`;
}

export function grams(g: number): string {
  return g >= 1000 ? `${(g / 1000).toFixed(2)} kg` : `${Math.round(g)} g`;
}
