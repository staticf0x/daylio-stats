# dailyo-stats

A simple script to generate a plot based on Dailyo export CSV file.

## Usage

```
$ pipenv install
$ pipenv shell
$ ./mood.py <path to CSV file>
```

This will save a png file with the plot.

## TODOs

- Try to detect periods of good/bad moods
- Try to detect rapid mood changes
- Make a word cloud from notes and assign them to moods
- Support for more than 5 moods
- Support for custom colors
- Make everything a Django (or just Flask?) app and allow ppl to run it in browser
