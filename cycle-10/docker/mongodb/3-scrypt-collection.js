db.createCollection("scrypt");
const scryptCollection = db.getCollection("scrypt");
scryptCollection.insertMany([
  {id: "michael", password: "$s0$e0801$epIxT/h6HbbwHaehFnh/bw==$7H0vsXlY8UxxyW/BWx/9GuY7jEvGjT71GFd6O4SZND0="},
  {id: "tony", password: "$s0$100808$6McCjsQBpcCShLWq4nl3gg==$gs+Tz5DLGCDtYHGpIkP4i3EDpufBzsEGvoXzegkO5cU="},
]);
