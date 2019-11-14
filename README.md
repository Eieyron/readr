# Readr
###### Absolutely needs a better name

## About
A simple document form reader that uses machine learning to read handwritten digits extracted from boxed fields.

## Installation

### Python and PIP
* Install Python 3.6.7 and PIP
```
sudo apt update
sudo apt install python3-dev python3-pip
```
* Check versions
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

#### Or:
Since project is required to use Python 3+, we can also use Python 3's `venv` instead:
* Create a new virtual environment using `venv`
	
	`python3 -m name_of_venv ./path/to/venv/`

* Use the virtual environment

    `source ./path/to/venv/bin/activate`
    
* Stop using the virtual environment

    `deactivate`
    
### Dependencies
* For installation of libraries used only _(recommended)_
 
    `pip3 install -r /path/to/requirements.txt`
     
* For installation of libraries and their dependencies in Ubuntu
    
    `pip3 install -r ./extended_requirements.txt`
    
* For installation of libraries and their dependencies in Windows
    
    `pip3 install -r ./windows_requirements.txt`

###### In case `pip3` doesn't work or is missing, try `pip` instead.

## Testing the Script

### Basic
* Run `main.py`
	
	`python3 main.py`
	
* Select `./test/test_image.png` as image file, `./test/` as image directory, 
    and `./test/test_file.csv` as csv file when asked.

* Check `test_file.csv` for the read data.

### Advanced
* To change the settings, edit `settings.ini` in root folder.
* To change how the program reads the scanned form, 
edit the `*.txt` file indicated in `settings.ini` under `[FILE]` and in line `form`,
or replace it with another one.
* To check how the program reads the `*.txt` file, run `test.py`. 
_(Needs a Python installation set up to do this)_

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

#### Character
* Character is the digits inside the field.
* Characters are only ordered from left-to-right, as the fields are designed for one row of characters only. 

### Setup `txt` file
The `txt` file referenced in `settings.ini` under `[FILE]` and in line `form` 
determines how the program will understand and structure the form. The `txt` file follows the `JSON` syntax.

### Tweaking and Troubleshooting
If the new sheet isn't correctly read or causes errors:
* Set the values under `[DEBUG]` in `settings.ini` to `True` to see how the program detects and segments the image.
    * Set `show_contours` to `True` to see what elements were extracted by the program.
    * Set `show_region` to `True` to see what the program detects as the region.
    * Similarly, set any of `show_section`, `show_field`, `show_character` 
    to see what the program detects as a section, field, and character, respectively.
    
* Try adjusting the values under `settings` in  `*.txt`.
    * Try lowering `"min_ratio"` and raising `"max_ratio"` under `"region"` if the image's region is not detected.

* If the program now reads the image properly, make sure to set the values under `[DEBUG]` to `False` again, 
as it may slow down the program.

* Make sure the next images to be read are scanned with the same setup, equipment, and settings 
so as not to tweak the program again.

## Compiling
The project can be compiled as is into a redistributable executable file, using PyInstaller. 
This can make the project available to machines with no existing Python installations and more convenient to users,
given that the machine where its `exe` file is compiled is similar to the target machine, particularly their OSes.

In the root directory of the project:
* Generate a `spec` file

```
pyi-makespec --hidden-import=tensorflow.keras --icon=./assets/icon.ico --windowed --onefile --name readr main.py
```

* Run PyInstaller on the `spec` file to generate the executable:

```
pyinstaller --clean readr.spec
```

* Move the generated `exe` file in `dist/` into a new folder somewhere else. 

* Finally, copy the `models/`, and `assets/` folders. You can then either create two new `csv` files containing
the format and column names separately, and edit `settings.ini` accordingly to point to it, 
or just copy the default `*.txt` in `files/` to the folder where the generated `exe` file is located.
Again, don't forget to make sure to edit `settings.ini` to point to these two files.

* Try running the generated `exe` file. If its needed files are found, it will run as intended.

## Recreating the model
The script to train the model is found in `./train/model.py`. 
Take note that the script requires `tensorflow=2.0.0a0` to run.

## Restrictions
* Do not delete or remove a line in `settings.ini`, `*.txt` and any file referenced in `settings.ini`.
* Scanned image should be upright as much as possible, or should have the top bottom on the viewer's left side.
* The `csv` files to be written data on must either be empty or always have a header. 