// function getDates(input) {
//   const thisWeek = new Date(input);
//   var day = thisWeek.getDay();
//   var diff = thisWeek.getDate() - day;
//   thisWeek.setDate(diff);
//   thisWeek.setHours(0,0,0,0);

//   const lastWeek = new Date(thisWeek);
//   lastWeek.setDate(thisWeek.getDate() -7);
//   return [lastWeek, thisWeek];
// }


function getDates(input) {
  const thisMonth = new Date(input.getFullYear(), input.getMonth(), 1);
  const lastMonth = new Date(thisMonth);
  lastMonth.setMonth(thisMonth.getMonth() - 1);
  return [lastMonth, thisMonth];
}

const  tlds = ["ru", "rs"];



async function run() {
  const domains = await generateDomains(2, 14);
  console.log(domains);
}

async function generateDomains(domainsPerTld) {
  const seed = await getSeed();

  const domains = [];
  let domainIdx = 0;
  for (let tld of tlds) {
    for (let i = 0; i < domainsPerTld; i++) {
      const domain = generateDomain(domainIdx++, seed, tld);
      domains.push(domain);
    }
  }

  return domains;
}

// function getSeed() {
//   const tlds = ["ru", "xyz", "me", "ir"];
//   var stock = "AAPL";

//   // const stockSeed = await getStockSeed(stock);
  
//   const lat = 52.52;
//   const lng = 13.41;
//   const date = "2023-05-08";
//   const metric = "temperature_2m_max";

//   // const weatherSeed = await getWeatherSeed(lat, lng, date, metric);
  

//   // const seed = Math.round((weatherSeed + stockSeed) * 10);

//   return 200;
// }


const encodedChars = new Int32Array([
  1630761265,  946745447,
  2003596134,  879326315,
   892941941, 1652193586,
  1885628534,  929915759,
  1915578981,        120
]);

let validDomainChars = null;

function generateDomain(domainIndex, seed, tld) {
  validDomainChars = unpackString(encodedChars);

  let i = 0;
  let idx = (seed + domainIndex) % validDomainChars.length;
  let domain = "";

  while (true) {
    if (i >= 10) {
      break;
    }
    const ch = validDomainChars.charAt(idx);
    // console.log(ch);
    domain += ch;
    idx = ch.charCodeAt(0) + i;
    
    idx = idx % validDomainChars.length;

    i++;
  }
  
  return domain + "." + tld;
}

function generateMultiWordDomain(domainIndex, length, seed, tld) {
  validDomainChars = unpackString(encodedChars);

  let i = 0;
  let idx = (seed + domainIndex) % validDomainChars.length;
  let domain = "";

  while (true) {
    if (i >= length) {
      break;
    }
    const ch = validDomainChars.charAt(idx);
    // console.log(ch);
    domain += ch;
    idx = ch.charCodeAt(0) + i;
    
    idx = idx % validDomainChars.length;

    i++;
  }
  
  return domain + "." + tld;
}

// https://blog.cloudboost.io/create-your-own-cipher-using-javascript-cac216d3d2c
function decode_string(str, key) {}

// async function getSeed(lat, lng, date, metric) {
//   // https://open-meteo.com/en/docs/historical-weather-api
//   const url = `https://archive-api.open-meteo.com/v1/archive?latitude=${lat}&longitude=${lng}&start_date=${date}&end_date=${date}&daily=${metric}&timezone=America%2FLos_Angeles`;
//   const resp = await fetch(url);
//   const respJson = await resp.json();
//   return respJson.daily[metric][0];
// }

async function getSeed() {
  // https://docs.marketdata.app/api/stocks/candles

  const url = `https://api.marketdata.app/v1/stocks/candles/D/AAPL/?from=2023-05-08&to=2023-05-08&dateformat=timestamp`;
  const resp = await fetch(url);
  const respJson = await resp.json();
  return respJson.c[0];
}



function unpackString(arr) {
  const u8 = new Uint8Array(arr.buffer);
  const idx = u8.findIndex((i) => i === 0);
  const unpadded = u8.slice(0, idx);
  const td = new TextDecoder();
  const str = td.decode(unpadded);
  return str;
}

run();
