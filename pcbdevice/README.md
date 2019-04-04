# PCB Device

This program transforms a pcb drawing into a gcode

## Getting started

To use this program, you need to launch main.py with the proper parameters or launch UI.py in /UI/ and enter the parameters in the boxes.
The PCB drawing your are using needs to be of format *.pbm ,
there are plenty of converters online to change your file format, such as [this converter we used](https://convertio.co/fr/pdf-pbm/)

### Prerequisites

Since the program is coded in python, you need to install python, we used python 3.7.
You can use an IDE or cmd to launch the program or the UI

### Using the program

After downloading the project,
You can launch UI.py in S4-P3-Projet/pcbdevice/UI/ for the user interface of the program.

Enter the parameters in the proper boxes:

```
- Pcb drawing file path you want to convert into gcode, this file needs to be of type *.pbm
- Gcode file you want to save with the path where you want to save it.If the file doesn't exist, a new file will be created, file type     need to be *.gcode
- If the pbm file is of type binary or ascii. To find the type, you can open the file in a text editor,
  ascii files will start with P1 while binary with P4. Also, birary type will contain unreadable characters.
- Width dimension of your pcb, units are entered later, 
- Height dimension of your pcb, must be of the same units as width
- Radius of the tool you are using, units must be in mm.
- Units type for the width and height
```
Once all parameters are entered, you can click on the **execute program** button.
If everything is good, you should read **SUCCESS** on the bottom of the UI, else and error code should appear.

## People in this project

**Ian Lalonde** 

**Marc-Antoine Lafrenière** 

**Maxime Laporte** 

**Guillaume Pépin** 

**Louis-Philippe Baillargeon** 
