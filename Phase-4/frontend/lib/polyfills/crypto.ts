/**
 * Polyfill for crypto.randomUUID()
 * Required for ChatKit and other libraries that depend on this Web Crypto API feature
 */

if (typeof window !== 'undefined' && !crypto.randomUUID) {
  // @ts-ignore
  crypto.randomUUID = function randomUUID() {
    return '10000000-1000-4000-8000-100000000000'.replace(/[018]/g, (c: any) =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  };
}
