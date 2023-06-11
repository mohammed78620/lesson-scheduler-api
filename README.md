# Lesson Scheduler API
Lesson Scheduler API is a RESTful Application Interface, exposing resources for clients to book and view lessons. The Lesson Scheduler API has been developed with [Django](https://www.djangoproject.com) and the [Django REST Framework](https://www.django-rest-framework.org/). The Lesson Scheduler API has a **weak dependency with PostgreSQL** due postgres-specific ORM fields, Django cannot use other SQL databases such as SQLite.

The Lesson Scheduler API is NOT a standalone product. When running the Lesson Scheduler API on production, you must configure throttling, authentication, monitoring and others. 

> The Lesson Scheduler API is permissionless and dumb. If you don't run it behind a gateway, you risk the data being stolen. 

# Table of Contents
- [⚙️ Development](#development)
    - [🐳 Docker](#docker)
    - [🧪 Testing](#testing)
    - [📔 Documentation](#documentation)
    - [💯 Extra Points](#extra-points)
    - [♻️ Alternatives](#alternatives)
- [💻 Production](#production)
    - [📜 Commands](#commands)
    - [🐍 Environment](#environment)


# Development
The Lesson Scheduler API is configured with an **out-of-the-box** development environment via [docker](https://www.docker.com/) and managed with [docker compose](https://docs.docker.com/compose/). Before continuing, **make sure you have docker available in your system**.

To run the development server, simply run the following command in your preferred cli.

```bash
docker compose -f docker-compose.dev.yaml up -d
```

Docker will orchestrate the following containers

- 🖥️ A Django Development Server at http://localhost:8000
- ⚙️ A PostgreSQL Database at http://localhost:5347

You're all set now! Go to http://localhost:8000/api/schema/swagger-ui/, you should see the Open API UI. Happy coding!

Check live logs coming from the Django Server 

```bash
docker logs lesson-scheduler-api-web-1 --follow
```

## 🐳 Docker
If you're developing via Docker, then we've got you covered! This section outlines all the different Docker configurations you should be aware of.

First things first, be aware that **there is one docker compose specifications**, one for development `docker-compose.dev.yaml`. 

All configurations come with **out-of-the-box smart reload** that will restart the development server when any source file is created or updated. Also, when running a docker configuration, be aware that docker will run a series of initial commands in `docker-entrypoint.sh` that will collect static files, run database migrations and start a web server.


## 🧪 Testing
The Lesson Scheduler API runs tests via the [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/) Framework and implements unit testing for ORM models and integration testing for api endpoints. To programatically populate the database with dummy data points, the Lesson Scheduler API uses [model-bakers](https://github.com/model-bakers/model_bakery) library to easily create fixtures. Because of [postgres-specific fields](https://docs.djangoproject.com/en/4.1/ref/contrib/postgres/fields/) used by django, tests must be run under a postgres database. You might execute them via docker as follows.

To run the tests from a docker container, simply run
```bash
docker exec -i lesson-scheduler-api-web-1 bash -c 'poetry run python lesson_scheduler_api/manage.py test core.tests --buffer' 
```

Alternatively, tests can be run from source ( prior to having a postgres database running )
```bash
poetry run poetry run python lesson_scheduler_api/manage.py test core.tests --buffer
```
