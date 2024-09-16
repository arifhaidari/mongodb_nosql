## Database: MongoDB & NoSQL + Docker

In this project we use docker in order to setup the MongoDB

step 1

docker exec -it my_mongo bash

importing collection

mongoimport -d sample -c books --authenticationDatabase admin --username datascientest --password dst123 --file /data/db/books.json

step 2

mongosh -u datascientest -p dst123
