# fisheyes_fastapi
 
## update backend
- push the latest version to the `fisheyes_fastapi` repository
- pull the repository in the server you are running
- update the docker:
```bash
docker build -t izjenie/fisheyes_fastapi .
docker push izjenie/fisheyes_fastapi
```

## deploy
run:
```bash
docker compose up -d
```

## check status
check running docker:
```bash
docker ps
```
use `-a` to also check the stopped ones:
```bash
docker ps -a
```

## export mongodb
### export collection
```bash
mongoexport --uri="mongodb://rootuser:rootpass@localhost:27017/genedata?authSource=admin" --collection=genes --out=newgenes.json
```
- dbname is `genedata`
- collectionname is `genes`
- outputfile is `newgenes.json`
### export whole db
```bash
mongodump --uri="mongodb://rootuser:rootpass@localhost:27017/genedata?authSource=admin" --out=./directory
```
in this case:
- dbname is `genedata`
- outputdir is `./directory`



## restore
### Restore a whole db 
```bash
mongorestore --uri="mongodb://rootuser:rootpass@localhost:27017/genedata?authSource=admin" ~/fisheyes_fastapi/data/directory/genedata
```

### Restore a collection
```bash
mongoimport --uri="mongodb://rootuser:rootpass@localhost:27017/genedata?authSource=admin" --collection=genes --file=newgenes.json --jsonArray --mode=upsert
mongoimport --uri="mongodb://rootuser:rootpass@localhost:27017/genedata?authSource=admin" --collection=75pe --file=75pe.json --mode=upsert
```

## To check stuff
```bash
mongosh "mongodb://rootuser:rootpass@localhost:27017/genedata?authSource=admin"
```