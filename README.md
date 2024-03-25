# 3DBurdenn_Python
Python script to calculate percent volume occupied by a stain in segmented image stacks

Burden analysis with new python script (written by Phill Jones)
* put the burden_calc.py script in the same folder as above pythonburden
* put images to be analysed in a folder pythonburden/data
* open pyCharm
* file -> open  then choose folder pythonburden
*  In bottom right corner, click on last thing on the right and choose “add new interpreter”, create new, be sure to be in directory with the burden_calc.py OR if it remembers, choose environment with name of folder
*  Click on “current file” in top right corner
* Run the programme!

If a new virtual enviroment, will need to install packages. To do this, open terminal. In finder, control click on puthonburden folder, hold down option, and click copy as pathname. In terminal cd "pathname". Then type . venv/bin/activate (enter) to activate virtual environment. Install packages:
pip install python-csv
pip install Pillow
pip install numpy 
