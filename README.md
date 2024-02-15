# Wikipedia Scraper

Wikipedia Scraper will query an API to obtain a list of countries and their past political leaders. Then it will extract and sanitize their the first paragraph from their page and export it as a json file.

## Installation

1. Clone the repository with `git clone`. 
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries.

```bash
pip install -r requirements.txt
```

## Usage
1. Navigate to the clone directory.
2. Run `main.py` via the terminal. You might need to user `python3` instead of `python`. 
```bash
python main.py
```
2. Open the json file `leaders_data.json` to check the results.

For any questions on how to navigate and run a python file from terminal, see more [here](https://vteams.com/blog/how-to-run-a-python-script-in-terminal/#:~:text=To%20execute%20a%20Python%20script,you're%20using%20Python%203.).




## Visuals
A successful terminal will look like:

```
Starting a session to leaders API.
Connection with API was well stablished and cookie was collected.
List of countries was well collected.
Collecting the links for each leader.
Information about leaders from fr was well collected.
Information about leaders from us was well collected.
Information about leaders from ru was well collected.
Information about leaders from ma was well collected.
Information about leaders from be was well collected.
Collecting leader's names and paragraphs.
Exporting to json file.
Finished exporting.
```
And the outputted json file `leaders_data.json` might have keys and values as: 

```json

{
    "François Hollande": "François Hollande, né le 12 août 1954 à Rouen (Seine-Inférieure) (etc).",
    "Ельцин, Борис Николаевич": "Бори́с Никола́евич Е́льцин (1 февраля 1931 (1931-02-01) (etc.)"

}
```
Note, we only put some of the entries and uses (etc.) in this picture to make the example more concise.

An unsuccessful run might quit after displaying error messages such as:

* In case the API is down:
```
Problem connecting to API.
```
* In case the cookie for the connection has expired, or could not be collected:
```
Cookie is invalid.
```


## Timeline
This project took three days to be completed.

## Motivation

This project is part of [Becode](https://becode.org/) AI & Data Science training. 
The goals were: to practice OOP, file handling, working with API and parsing HTML.