# Readr
###### Absolutely needs a better name

## About
A simple document form reader that uses machine learning to read handwritten digits extracted from boxed fields.

## To Do
* create dist file using pyinstaller
* require valid `settings.ini`, `format.csv`, `keys.csv`
* stop program if any values in `settings.ini`, `format.csv`, `keys.csv` is missing or wrong.
* better looking UI? *(hmm)*
* ~~selecting multiple files?~~
* ~~tooltips?~~
* ~~os-independent functions~~
* ~~functional UI~~
* ~~output read data to csv~~
* ~~implement settings~~

## Installation

### Python and PIP
* install Python 3.6+ and PIP
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
Since project is required to use Python 3+, we can also use Python 3's `venv` instead:
* Create a new virtual environment using `venv`
	
	`python3 -m name_of_venv ./path/to/venv/`

* Use the virtual environment

    `source ./path/to/venv/bin/activate`
    
* Stop using the virtual environment

    `deactivate`
    
### Dependencies
* For installation of libraries used only
 
    `pip3 install -r /path/to/requirements.txt`
     
* For installation of libraries and their dependencies in Ubuntu
    
    `pip3 install -r ./extended_requirements.txt`
    
* For installation of libraries and their dependencies in Windows
    
    `pip3 install -r ./windows_requirements.txt`

###### In case `pip3` doesn't work or is missing, try `pip` instead.

## Testing the Program

### Basic
* Run `main.py`
	
	`python3 main.py`
	
* Select `./test/test_image.png` as image file, `./test/` as image directory, 
    and `./test/test_file.csv` as csv file when asked.

* Check `test_file.csv` for the read data.

### Advanced
* To change the settings, edit `settings.ini` in root folder.
* To change the headers or column names when writing to file, 
    edit `keys.csv` in `files/` using a text editor or spreadsheet.
	* First row corresponds to labels defined in `format.csv`
	* Columns under the first row will be written as header or column name, written in order from top to bottom, 
	then left-to-right where values of the corresponding field will be written under.
* To change the structure to be constructed of the image, 
    edit `format.csv` in `files/` using a text editor or spreadsheet
	* First row corresponds to labels for each section of the document extracted
	* Second row determines the number of columns per section of the document
	* Third row determines symbols to use when joining a row of fields for each section.
	* Fourth row is the first item number for each section

## Setup for a New Sheet Format

### Create a New Sheet
The program segments and structures the sheet based on these elements:

#### Region
* Region is the closed box containing the sections and fields to be extracted. 
* It should be the largest element in the image area-wise.
* A sheet can only have one of this.

#### Section 
* Section is the closed box inside the region to group columns of fields.
* It should not share a column with other sections.
* Sections are ordered leftmost first.

#### Field
* Field is the closed box inside the section for the user to write values on.
* It can be joined along with fields of the same row in a section to represent decimal values, fractions, dates, etc.
* Fields are ordered from left-to-right, then top-to-bottom.

### Setup `format.csv` and `keys.csv`
These files are necessary for the program to know how to segment and structure your new sheet. The file `format.csv`, 
as mentioned earlier, determines the labels, symbols, number of items and columns the program will extract and use. 
Meanwhile, `keys.csv` determines the column names or headers that will be written at the top of the csv file,
and which fields will be considered.

Either edit the default files in `files/` to accommodate the new sheet
or create a new one and edit `settings.ini` to point to it. 

Lastly, in `settings.ini`, under `[ORIENTATION]`, 
set `is_landscape` to `True` if the sheet is crosswise, and `False` otherwise.  

### Tweaking and Troubleshooting
If the new sheet isn't correctly read or causes errors:
* Set the values under `[DEBUG]` in `settings.ini` to `True` to see how the program detects and segments the image.
    * Set `show_contours` to `True` to see what elements were extracted by the program.
    * Set `show_region` to `True` to see what the program detects as the region.
    * Similarly, set any of `show_section`, `show_field`, `show_character` 
    to see what the program detects as a section, field, and character, respectively.
    
* Try adjusting the values under `[REGION]` in `settings.ini`.
    * Try lowering `min_ratio` and raising `max_ratio` under `[REGION]` if the image's region is not detected.

* If the program now reads the image properly, make sure to set the values under `[DEBUG` to `False` again, 
as it may slow down the program.

* Make sure the next images to be read are scanned with the same setup, equipment, and settings 
so as not to tweak the program again.

## Restrictions
* Do not delete or remove a line in `settings.ini`, `format.csv`, `keys.csv` and any file referenced in `settings.ini`.
* Scanned image should be upright as much as possible, or should have the top bottom on the viewer's left side.