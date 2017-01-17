# Cinemas

Script downloads list of movies from [Afisha.ru](http://www.afisha.ru/msk/schedule_cinema/), 
gets their rating from [Kinopoisk](https://www.kinopoisk.ru/) and shows movies with the highest rating.  
By default script chooses only new popular films (which are shown in more than 10 cinemas) and 
shows 10 best of them. You can change this settings using script arguments.

## Usage

- **Clone repository:** `git clone https://github.com/Sir-Nightmare/13_cinemas.git`  
- **Install necessary modules:** `pip3 install -r requirements.txt` 
- **Launch the script:** `python cinemas.py  <options>` 

**Options:**

description | type | key | default value
--- | --- | --- | ---|
**Number of movies to show** | int | `-m, --movies`| 10
**Minimum number of cinemas** | int | `-c, --cinemas`| 10


**Examples:**

```
python cinemas.py 
python cinemas.py -m 15 -c 0
```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
