# lego-collection

Creates a local copy of public [Rebrickable](https://rebrickable.com) database appended with additional table containing user sets.

It uses [jncraton/rebrickable-sqlite](https://github.com/jncraton/rebrickable-sqlite) to create an SQLite database from public [Rebrickable](https://rebrickable.com) csv-dumps. Then it creates a `set_lists` table containing all sets from user's Set Lists.

## Docker

- Build docker image:
```
docker build -t bricks:latest . 
```
- Run docker container:
```
docker container run --rm --name lego-collection \
    --env LOGIN=<rebrickable username> \
    --env PASSWORD=<rebrickable password> \
    --env API_KEY=<rebrickable API key> \
    --volume=/path/to/database/dir:/database \
    lego-collection:latest
```

## Docker compose

- Change variables' values in `sample.env`
- Run compose tool:
```
docker compose up
