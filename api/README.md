# Artist 2D - API

The backend API that the frontend and internal crons use to do things.

## Getting Started

This is a WIP.

### One-time Setup

This only needs to be run once per local development machine, not for each API directory.

1. You will need python (see Pipfile for version) and pip.
2. You will need to set to create a gcp iam role for your local dev (name it "YOURNAME-local-dev") and download the json secret stuff.


### Local Setup

Set up your local development environment for the API.


3. Create a `.env` file that specifies GCP envvars.
   - You can start by copying the example and updating the values. `cp .env.example .env`
   - Or you can copy a `.env` file from another api in this project.
4. `make setup` will handle pipenv fun for you.
    - Run this again if new packages were added with `pipenv install ...`
5. Do something to improve this getting started guide!

#### Local Django Admin

The app uses oauth and the Django admin can be accessed on a locally running server at [http://localhost:8000/admin/].

The first time your run, and any time you destroy your `docker-compose` volumes, you'll need to set yourself up as a super user.

1. [Sign in with OAuth](http://localhost:8000/accounts/google/login/?process=login). This creates an account that you will give staff and superuser access.
1. Jump onto the running psql container.
    1. Find the container ID by running `docker ps` and copy the `Container ID` for the `postgres` image.
    1. Run `docker exec it containerIdThatYouCopied bash` to connect to the running postgres container.
    1. Run `psql artist -Upostgres` to access the `artist` database.
    1. Run `select * from auth_user;` to see your user table. You should see exactly 1 user and it should be you.
    1. Give yourself super admin permissions by running `update auth_user set is_staff = 't', is_superuser = 't' where id = 1;`. This assumes your user's row ID is 1. It should be.
1. Access the admin console at [http://localhost:8000/admin/].



## Run

```
make run
```

## Test

```
make test
```

## Deploy

Bump the version in (variables.tf)[../infra/app/variables.tf] and merge PR. The CD pipeline will test and deploy.

## Learn More

[Tech Spec](docs/tech_spec.md)


## Social Auth

http://localhost:8000/accounts/google/login/?process=login
