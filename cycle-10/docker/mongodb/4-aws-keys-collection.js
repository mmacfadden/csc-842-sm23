db.createCollection("awsAccessKey");
const awsAccessKeys = db.getCollection("awsAccessKey");
awsAccessKeys.insertMany([
    {id: "AKIAIOSFODNN7EXAMPLE", password: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"},
    {id: "ASIAY34FZKBNKMUTVV7A", password: "wJalrXUtnFEMI/K7MDENG/bPxRfiC2EXAMPLEKEY"},
    {id: "AKIARJFBAG3EGHFG2FPN", password: "wJalrXUtnFEMI/K7MDENG/bPxRfiC3EXAMPLEKEY"},
]);
