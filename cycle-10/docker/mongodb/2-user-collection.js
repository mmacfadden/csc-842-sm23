db.createCollection("users");
const usersCollection = db.getCollection("users");

const users = [
  {id: "michael", password: "89e01536ac207279409d4de1e5253e01f4a1769e696db0d6062ca9b8f56767c8"},
  {id: "tony", password: "0307c722793c8c2981acdf660d4529692fc618bef4d8313be0677091077aa6af"},
  {id: "alec", password: "ce569449bb9ebda90c4b1b0b5844bb6d3087c17ac6291ba7e259ff18d4820646"},
  {id: "john", password: "9f8adace3963c66e0322620b2b38cc312c5583cb6e14ef79dadd9180612bfda7"}
];

users.forEach(user => {
  usersCollection.insertOne(user);
});
