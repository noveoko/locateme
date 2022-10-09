## People by Nationality
This is a simple script to build a dataset of people by nationality using Wikipedia as the primary data source

## Build the entire dataset
Run the following command in your command line:
```bash
python 'fetch_data.py'

```

This will visit every page in the 'countries_to_fetch.txt' file and extract all the people links. Next it will save the links to a seperate CSV file for each country

## Notes
Years 1900-1950 are given when no year is listed and years ending in 2025 are for people currently living. Feel free to ignore these values or update them by researching the specific people.


## Trouble-shooting

### Create the table

```bash
sqlite3 locateme.db "create table people(name text, link text, start text, end text, country text);"
```

Datasets used

https://simplemaps.com/data/world-cities

## Useful utilities
https://github.com/noveoko/locateme/blob/master/utilities/Recursive_Person_Extractor.ipynb
