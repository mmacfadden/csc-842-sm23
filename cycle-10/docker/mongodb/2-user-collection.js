db.createCollection("email_accounts");
const usersCollection = db.getCollection("email_accounts");

const users = [
  {id: "michael", email: "michael@example.org"},
  {id: "john", email: "john@example.org"}
];

users.forEach(user => {
  usersCollection.insertOne(user);
});
