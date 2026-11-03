// eclAIr books: negatives the accountant's way, in parentheses and in ink, never in red (Keith, 3 Nov 2026). Bigcapital's server
// shows them with a minus unless a report asks otherwise, so every report request that names no format asks for parentheses.
// A format someone chooses on a report still wins.
const REPORTS = '/api/reports/';
const PARENS = 'numberFormat[negativeFormat]=parentheses';

function withParens(url: string): string {
  if (!url.includes(REPORTS) || /numberFormat|number_format/.test(url)) return url;
  return url + (url.includes('?') ? '&' : '?') + PARENS;
}

if (typeof window !== 'undefined' && window.fetch) {
  const original = window.fetch.bind(window);
  window.fetch = (input: RequestInfo | URL, init?: RequestInit) => {
    if (typeof input === 'string') return original(withParens(input), init);
    if (input instanceof URL) return original(new URL(withParens(input.toString())), init);
    if (input instanceof Request && input.url.includes(REPORTS)) return original(new Request(withParens(input.url), input), init);
    return original(input, init);
  };
}

export {};
