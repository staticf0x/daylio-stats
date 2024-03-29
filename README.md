# daylio-stats

A tool to generate stats/charts from Daylio CSV exports.

Currently supports:

- Creating a chart of all data since the beginning of tracking
- Smoothing the chart with a rolling average

Locally you can use:

```
$ ./manage.py generate_charts <path to Daylio CSV>
```

to get more charts than we're able to generate now on Heroku.

## Running locally

### Installation

After cloning the repo:

- `$ npm install` (this is only for development currently)
- `$ poetry install`

### Secret key for Django

Either set the `DS_SECRET_KEY` env variable directly, or read the key from a file.

For bash:

```bash
$ export DS_SECRET_KEY=$(cat .ds_secret_key)
```

For fish:

```fish
$ set -x DS_SECRET_KEY (cat .ds_secret_key)
```

Or just create `.env` file and put it in there:

```
DS_SECRET_KEY=...
```

### Database password

Same as with the secret key:

Either set the `DS_DB_PASSWORD` env variable directly, or read the key from a file.

For bash:

```bash
$ export DS_DB_PASSWORD=$(cat .ds_db_password)
```

For fish:

```fish
$ set -x DS_DB_PASSWORD (cat .ds_db_password)
```

### Setting the dev environment

Go to `dayliostats/settings.py` and set

```python
DEBUG = True
ADMIN = True
```

### Run the development server

For port 8000:

```
$ poetry shell
$ ./manage.py runserver 8000
```

### Or use gunicorn

```
$ gunicorn dayliostats.wsgi
```

### Or use Docker

```
$ docker run --rm -e DS_SECRET_KEY="<secret key>" -p 8000:8000 daylio-stats
```

## Running tests

```
$ ./manage.py test
```
