#!/usr/bin/env node

const fs = require("fs")

const script = fs.readFileSync("out/dga.js").toString();

eval(script);

generateDomains()
  .then(domains => {
    console.log(domains.join("\n"));
  })
  .catch(e => console.error(e));