for programmers

installation

repo link: https://github.com/renscy/readr

general
install python >= 3.6.7.

windows
(i coded it using pycharm)
install pycharm (https://www.jetbrains.com/pycharm/download/)
create new project
set up virtual environment for the project (https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)
use this virtual environment for the project (https://intellij-support.jetbrains.com/hc/en-us/community/posts/360004289920-How-activate-virtualenv-from-pycharm-terminal-)
install needed libraries in your project's venv using "pip freeze > requirements.txt" at the root folder
(to use the actual libraries used and their prerequisites, type in "windows_requirements.txt" instead)

ubuntu
<optional>
create a virtual environment for python
activate the virtual environment
</optional>
install needed libraries using "pip freeze > requirements.txt" on root directory
(to use the actual libraries used and their prerequisites, type in "extended_requirements.txt" instead)

overview
the program in theory extracts information in five phases:
- preprocessing
- extraction
- classification
- merging
- writing

the code is divided into modules with functions roughly representing these phases:
- preprocessing -> preprocess.py, extract.py
- extraction -> extract.py
- classification -> ai.py
- merging & writing -> write.py

other modules used in the program are:
modules:
config.py -> responsible for handling settings.ini, and checking if all mentioned files are valid
filter.py -> filters for contour based on their properties
interface.py -> functions integrating button commands to their equivalent tasks
misc.py -> functions used for troubleshooting or looking at partial results of functions
model.py -> workaround module to load the model files into other modules
translate.py -> if the numbers were used to represent something else, this can be used. unused.
ui.py -> integrates the ui classes and the interface

classes:
appmenu.py -> contains the buttons on the ui
apptracker.py -> contains the status bar below the menu

other files/folder in the root dir:
assets/ -> contains the images used in the program
build/ -> pyinstaller files
dist/ -> pyinstaller exe files, version is based on date compiled
files/ -> contains preset files in json needed by the program to read documents
models/ -> contains the models that classifies the characters
train/ -> contains the script for the training and architecture of models (model.py) and for evaluating it (eval.py)

test.py -> script that prints out the contents of the json preset files, for debug
readr.spec -> pyinstaller file
extended_requirements -> complete requirements for ubuntu, including prerequisite libraries
requirements -> basic required libraries
windows_requirements -> complete requirements for windows, including prerequisite libraries
README.md -> read this too
settings.ini -> contains settings for the program
main.py -> run this