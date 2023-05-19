
function unpackString(arr) {{
   const u8 = new Uint8Array(arr.buffer);
   const idx = u8.findIndex((i) => i === 0);
   const unpadded = u8.slice(0, idx);
   const td = new TextDecoder();
   const str = td.decode(unpadded);
   return str;
}}

function getDates() {
  const now = new Date();
  const thisMonth = new Date(now.getFullYear(), now.getMonth(), 1);
  const lastMonth = new Date(thisMonth);
  lastMonth.setMonth(thisMonth.getMonth() - 1);
  return [lastMonth, thisMonth];
}

async function getSeed(date) {
  date = date.toISOString().split('T')[0]
  const url = `https://api.marketdata.app/v1/stocks/candles/D/AAPL/?countback=1&to=${date}&dateformat=timestamp`;
  const resp = await fetch(url);
  const respJson = await resp.json();
  return Math.floor(respJson.c[0] * 10);
}

const encodedChars = new Int32Array([
  1630761265,  946745447,
  2003596134,  879326315,
   892941941, 1652193586,
  1885628534,  929915759,
  1915578981,        120
]);

let validDomainChars = null;

function generateDomain(domainIndex, seed) {
  validDomainChars = unpackString(encodedChars);

  let i = 0;
  let idx = (seed + domainIndex) % validDomainChars.length;
  let domain = "";

  while (true) {
    if (i >= 10) {
      break;
    }
    const ch = validDomainChars.charAt(idx);
    domain += ch;
    idx = ch.charCodeAt(0) + i;

    idx = idx % validDomainChars.length;

    i++;
  }

  return domain;
}

const tlds = ['re', 'ru', 'xyz', 'za'];

async function generateDomains() {
  const domains = [];
  let domainIdx = 0;

  const dates = getDates();

  for (d of dates) {
    const seed = await getSeed(d);
    for (let tld of tlds) {
      for (let i = 0; i < 2; i++) {
        const domain = generateDomain(domainIdx++, seed);
        domains.push(domain + "." + tld);
      }
    }
  }

  return domains;
}

generateDomains().then(p => console.log(p)).catch(e => console.error(e));
