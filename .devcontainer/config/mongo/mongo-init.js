
db = db.getSiblingDB('admin').auth(
    process.env.MONGO_INITDB_ROOT_USERNAME,
    process.env.MONGO_INITDB_ROOT_PASSWORD);


db.getSiblingDB('Hyfi');

db.createUser({
  user: 'alpha',
  pwd: 'developer',
  roles: [
      {
      role: 'dbOwner',
      db: 'Hyfi'
      },
      {
      role: 'readWrite',
      db: 'Hyfi'
      },
      {
      role: 'userAdminAnyDatabase'
      }
  ]
});

db.createUser({
  user: 'beta',
  pwd: 'developer',
  roles: [
    {
      role: 'readWrite',
      db: 'Hyfi'
    }
  ]
});

db.createUser({
  user: 'gamma',
  pwd: 'developer',
  roles: [
    {
      role: 'readWrite',
      db: 'Hyfi'
    }
  ]
});


db.createCollection("users", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: ["name", "email", "password", "age"],
         properties: {
             _id: {
                bsonType: "objectId",
                description: "must be an objectId and is required",
                uniqueItems: true,
                default: new ObjectId()
             },
            name: {
               bsonType: "string",
               description: "required and must be a string"
            },
            email: {
               bsonType: "string",
               description: "required and must be a string representing an email address",
               pattern: "^\\S+@\\S+\\.\\S+$",
               uniqueItems: true
            },
            password: {
               bsonType: "string",
               description: "required and must be a string"
            },
            age: {
               bsonType: "int",
               description: "required and must be an integer"
            },
            roles: {
               bsonType: "array",
               description: "must be an array of strings",
               items: {
                  bsonType: "string"
               },
               default: ["user"]
            },
            last_updated: {
               bsonType: "date",
               description: "must be a date string in the format YYYY-MM-DD HH:MM:SS",
               default: new Date()
            }
         }
      }
   }
})


