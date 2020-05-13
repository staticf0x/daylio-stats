# daylio-stats

A tool to generate stats/charts from Daylio CSV exports

## Running locally

### Installation

After cloning the repo:

- `$ npm install`
- `$ pipenv install`

### Secret key for Django

Either set the `DS_SECRET_KEY` env variable directly, or read the key from a file.

For bash:

```
$ export DS_SECRET_KEY=$(cat .ds_secret_key)
```

For fish:

```
$ set -x DS_SECRET_KEY (cat .ds_secret_key)
```

### Run the development server

For port 8000:

```
$ pipenv shell
$ ./manage.py runserver 8000
```
