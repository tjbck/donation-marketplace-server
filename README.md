# Donation Marketplace Server (Backend)

Donation Marketplace Server is a non-profit web application backend, built with Python (FastAPI).

## Installation

To deploy the backend, you must have docker installed on your system.

Once you've installed docker, run the following command to setup all its dependencies.

### MongoDB 

```bash
docker run -d -p 27017:27017 --name mongodb --restart always -e MONGO_INITDB_ROOT_USERNAME='root' -e MONGO_INITDB_ROOT_PASSWORD='root' mongo:latest
```

### Recaptcha

This application requires you to provide your own Recaptcha credentials to function correctly.

You can obtain your credentials [here](https://www.google.com/recaptcha/about/).

## Deployment

Build the backend image on your local machine to deploy like such:

```bash
docker build -t marketplace-server .
```

After docker finishes building the image, run the following command to deploy:

```bash
docker run -d -p 3030:3030 --name marketplace-server -e SECRET_KEY='SECRET_KEY' -e RECAPTCHA_SECRET='YOUR_RECAPTCHA_SECRET' -e DB_CRED='root:root' -e DB_URL='host.docker.internal' --add-host=host.docker.internal:host-gateway marketplace-server
```

* Note: Run `openssl rand -hex 32` to obtain a secure secret key.

## Testing

All the tests run automatically when you build the docker image for this backend.

If the tests fail, the build process will terminate with error messages.

### Manual Testing

You first need to install all python3 requirements by running the command below:

```bash
pip3 install -r requirements.txt
```

Once you've installed the requirements, run the following command to setup Test MongoDB environment:

```bash
docker run -d -p 27018:27017 --name mongodb-test -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=root mongo:latest
```

Once you've installed the all the requirements, simply run:

```bash
pytest
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)