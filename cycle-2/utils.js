function packString(str) {
  const te = new TextEncoder();
  const u8 = te.encode(str);
  const pad = 4 - u8.length % 4;
  const paddArr = [];
  for (let i = 0; i < pad; i++) {
    paddArr.push(0);
  }
  const padded = new Uint8Array(u8.length + pad);
  padded.set(u8, 0);
  padded.set(paddArr, u8.length);
  console.log(padded.length);
  
  return new Int32Array(padded.buffer);
}