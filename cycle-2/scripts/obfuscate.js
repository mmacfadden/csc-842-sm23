#!/usr/bin/env node

const JavaScriptObfuscator = require('javascript-obfuscator');
const fs = require('fs');
const path = require('path');

const inputFile = process.argv[2];
const mainName = process.argv[3];

console.log(inputFile, mainName);

const input = fs.readFileSync(inputFile).toString();


var obfuscationResult = JavaScriptObfuscator.obfuscate(
  input,
    {
        compact: false,
        controlFlowFlattening: true,
        controlFlowFlatteningThreshold: 1,
        numbersToExpressions: true,
        simplify: true,
        stringArray: true,
        stringArrayEncoding: ["rc4"],
        stringArrayShuffle: true,
        splitStrings: true,
        stringArrayThreshold: 1,
        reservedNames: [mainName],
        renameGlobals: true
    }
);

const obfuscated = obfuscationResult.getObfuscatedCode();

const outputFile = path.join(path.dirname(inputFile), path.basename(inputFile, path.extname(inputFile)) + '.obfuscated.js');
console.log(outputFile);

fs.writeFileSync(outputFile, obfuscated);