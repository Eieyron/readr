# Readr

## About
A simple document form reader that uses machine learning to read handwritten digits extracted from boxed fields.

## To Do
* better looking UI?
* selecting multiple files?
* tooltips?
* ~~os-independent functions~~
* ~~functional UI~~
* ~~output read data to csv~~
* ~~implement settings~~

## Installation
### Python and PIP
* install Python 3.6.8+ and PIP
```
sudo apt update
sudo apt install python3-dev python3-pip
```
* check versions
```
python3 --version
pip3 --version
```

### Virtual Environment
Set up a virtual environment to isolate the project's dependencies
* Install `virtualenv`
	`sudo pip3 install -U virtualenv`
* Check
	`virtualenv --version`
* Create a virtual environment
	`virtualenv -p python3 ./path/to/venv/`
* Use the virtual environment
	`source ./path/to/venv/bin/activate`
* Stop using the virtual environment
	`deactivate`

#### Or
Since project is required to use Python 3+, we can only use Python 3's `venv`:
* Create a new virtual environment using `venv`
	`python3 -m name_of_venv ./path/to/venv/`


### Dependencies
* `pip3 install -r /path/to/requirements.txt` for installation of libraries used only  
* `pip3 install -r ./extended_requirements.txt` for installation of libraries and their dependencies in Ubuntu
* `pip3 install -r ./windows_requirements.txt` for installation of libraries and their dependencies in Windows

## Testing the Program
### Basic
* Run `main.py`
	`python3 main.py`
* Select `./test/test_image.png` as image file, `./test/` as image directory, and `./test/test_file.csv` as csv file when asked.
* Check `test_file.csv` for the read data.

### Advanced
* To change the settings, edit `settings.ini` in root folder.
* To change the headers or column names when writing to file, edit `keys.csv` in `files/` using a text editor or spreadsheet.
	* First row corresponds to labels defined in `format.csv`
	* Columns under the first row will be written as header or column name, written in order from top to bottom, then left-to-right where values of the corresponding field will be written under.
* To change the structure to be constructed of the image, edit `format.csv` in `files/` using a text editor or spreadsheet
	* First line corresponds to labels for each section of the document extracted
	* Second column determines the number of columns per section of the document
	* Third column determines symbols to use when joining a row of fields for each section.
	* Fourth column is the first item number for each section

## Setup for New Sheet Format

## Restrictions
* Do not delete or remove a line in `settings.ini`, `format.csv`, `keys.csv` and any file referenced in `settings.ini`.
* Scanned image should be upright as much as possible, or should have the top bottom on the viewer's left side.