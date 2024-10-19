# auth-api
what's the password?

### API
When creating the api I opted to first create a base router, `AuthRouter`, and then each new feature/business function would subclass a router from there. Then each router is attached to the `root_router`. This allows for the following things to be true:
- Easily label and version routes based on prefixes
- Allows different routers to have the same sub-endpoint names. ex. `/users` -> `/team/users`
- Enforce Bearer tokens at the `root_router` level

### DB
The `db` is mostly all boilerplate I've collected over the years. It provides the following:
- A scalable generator for injecting the data base session to each request
- common types for default table columns `id`, `created_at`, `last_updated`, etc.
- environment variables for alembic during migrations

### Domains
All logic that doesn't belong directly in the endpoint, but also doesn't directly touch the database. Typically is where I implement objects defined in `/services`.

### Managers
Where we interface with the database. Each table gets a "Manager". `User` -> `UserManager`. A manager abstracts all the functional database code away from the immediate request path. Managers are imported as singletons to increase performance (especially when database pooling at scale). 

### Models
Houses both standard pydantic models and ORM models. I've never liked this design because you often end up defining a model like `User` twice: once in the orm, and again in root of `/models`. It works, but gets cumbersome at scale. I've looking into `sqlmodel` lately.

### Schemas
Houses all pydantic models used in request/response flows for endpoints.


### Services
For storing all code/logic for third-party or internal microservices. In this case that is just `supabase`.

## Project Structure
```
├── /auth
│ ├── app.py
│ ├── app_factory.py
│ ├── enums.py
│ ├── helper.py
│ ├── settings.py
│ ├── api/
│ ├── db/
│ ├── domains/
│ ├── managers/
│ ├── models/
│ ├── schemas/
│ ├── services/
└── /
```

## Run locally

Setup `.env` file
```sh
cp .env.example .env
```

Install dependencies
```sh
poetry install
```

Run server locally
```sh
make server
```
*Note: Runs this command `poetry run uvicorn --reload auth.app:app --host 0.0.0.0 --port 9898`*

## Database Migrations

Create migration
```sh
make alembic-migration
```

Upgrade DB

*Runs all migrations*
```sh
make dp-up
```

Downgrade DB

*Only reverts the previous migration, run over and over to keep reverting older migrations*
```
make db-down
```

## Docker

Build
```sh
docker build -t auth .
```

Run
```sh
docker run auth
```

Should look something like
```
Running on Python 3.11.9. The recommended Python is ^3.11.
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9898 (Press CTRL+C to quit)
```


