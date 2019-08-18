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
```

2) Build and deploy
```
docker-compose build
docker-compose up
```
