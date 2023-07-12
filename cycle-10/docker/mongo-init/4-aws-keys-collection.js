db.createCollection("awsAccessKey");
const awsAccessKeys = db.getCollection("awsAccessKey");
awsAccessKeys.insertMany([
    {id: "AKIAIOSFODNN7EXAMPLE", password: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"}
]);
