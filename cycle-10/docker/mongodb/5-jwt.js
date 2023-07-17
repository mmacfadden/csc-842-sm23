db.createCollection("jwt");
const jwts = db.getCollection("jwt");
jwts.insertMany([
    {jwt: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.5mhBHqs5_DTLdINd9p5m7ZJ6XD0Xc55kIaCRY5r6HRA"},
    {jwt: "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJGb28gYmFyIiwibmFtZSI6Ik1pY2hhZWwgRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.xms1lINSQP9omxeDW7QoHikWlpA3XaX9P7EsKpLyVQKK-9sKWIX8Ove-qe8Zo0hISRNquMOcX21brtvOI0j3hQ"},
]);
