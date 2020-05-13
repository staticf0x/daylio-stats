# dailyo-stats

A tool to generate stats/charts from Dailyo CSV exports

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

## TODOs

- Try to detect periods of good/bad moods
- Try to detect rapid mood changes
- Make a word cloud from notes and assign them to moods
- Support for more than 5 moods
- Support for custom colors
- Make everything a Django (or just Flask?) app and allow ppl to run it in browser
- Add custom config for the charts -- configurable charts, colors, etc
    + And also create an URL to save the config
