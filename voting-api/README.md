# Artist 2D - Voting API

This is the API that interacts with the client-side frontend. It fetches art and allows voting.

## Getting Started

This is a WIP.

1. You will need python (see Pipfile for version) and pip.
2. You will need to set to create a gcp iam role for your local dev (name it "YOURNAME-local-dev") and download the json secret stuff.
3. Create a `.env` file that specifies GCP envvars.
   - You can start by copying the example and updating the values. `cp .env.example .env`
4. `make setup` will handle pipenv fun for you.
5. Do something to improve this getting started guide!

## Run

```
make run
```

This generate and an image to a path I find convenient because I haven't made it a variable yet.

## Test

```
make test
```

## Deploy


```
make deploy
```


## Learn More

[Tech Spec](docs/tech_spec.md)
