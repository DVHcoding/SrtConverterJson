# SRT to JSON Subtitle Converter

This Python script converts subtitle files in SRT (SubRip Subtitle) format into JSON format with an additional Vietnamese translation of the subtitle text.

## Features

- Converts SRT subtitles into JSON format.
- Translates English subtitles into Vietnamese.
- Outputs JSON file with start time, duration, English text, and Vietnamese translation.

## Prerequisites

Before running the script, ensure you have the following Python packages installed:

- `googletrans==4.0.0-rc1` (or any compatible version for translation)
- `re` (comes with Python standard library, no need to install separately)

You can install the required package using pip:

```sh
pip install googletrans==4.0.0-rc1
```
