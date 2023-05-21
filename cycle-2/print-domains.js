#!/usr/bin/env node

const fs = require("fs");

const dga = process.argv[2];

function isReadable(file) {
  try {
    fs.accessSync(dga, fs.constants.R_OK);
    return true;
  } catch {
    return false;
  }
}

if (!fs.existsSync(dga) || !isReadable(dga)) {
  console.error(`Cannot read DGA script: ${dga}`);
  process.exit(1);
}

const script = fs.readFileSync(dga).toString();

eval(script);

generateDomains()
  .then(domains => {
    console.log(domains.join("\n"));
  })
  .catch(e => console.error(e));