# SugsnFlask
Backend for Sugsn

## Instructions to deploy
1) Make .env file with the following properties
```
PGID=<INSERT PGID>
PUID=<INSERT PUID>
LETSENCRYPT_EMAIL=<INSERT LETSENCRYPT_EMAIL>
VIRTUAL_HOST=<INSERt VIRTUAL_HOST>
LETSENCRYPT_HOST=<INSERT LETSENCRYPT_HOST>
VIRTUAL_PORT=<INSERT VIRTUAL_PORT>
NETWORK_NAME=<INSERT NETWORK_NAME>
API_KEY=<INSERT API_KEY>
MONGO_URL=<INSERT MONGO_URL> // NOTE: For docker, use container name
FLASK_URL=<INSERT FLASK_URL> // NOTE: For docker, use container name
```

2) Build and deploy
```
docker-compose build
docker-compose up
```
