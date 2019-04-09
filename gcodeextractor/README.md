# GCode Extractor

This program transforms a pcb drawing into a gcode.

## Getting started

To use this program, you need to launch main.py with the proper parameters or launch UI.py in /UI/ and enter the parameters in the boxes.
The PCB drawing you are using needs to be of format *.pbm ,
there are plenty of converters online to change your file format, such as [this converter we used](https://convertio.co/fr/pdf-pbm/).

### Prerequisites

Since the program is coded in python, you need to install python, we used python 3.7.
You can use an IDE or cmd to launch the program or the UI.

### Using the program

After downloading the project, you can launch UI.py in S4-P3-Projet/gcodeextractor/UI/ for the user interface of the program.

Enter the parameters in the proper boxes:

```
- Pcb drawing file path you want to convert into gcode, this file needs to be of type *.pbm
- Gcode file you want to save with the path where you want to save it.
  If the file doesn't exist, a new file will be created, file type needs to be *.gcode
- If the pbm file is of type binary or ASCII. To find the type, you can open the file in a text editor,
  ASCII files will start with P1 while binary with P4. Also, binary type will contain unreadable characters.
- Width of your pcb, units are entered later, 
- Height of your pcb, it must be of the same units as the width
- Radius of the tool you are using, units must be in mm.
- Units type for the width and height
```
Once all parameters are entered, you can click on the **execute program** button.
If everything is good, you should read **SUCCESS** on the bottom of the UI, else and error code should appear.

### Algorithms

To convert a pcb image into a gcode, we first find where the tool will have to travel, in order to create the pcb. This is done in the path.py file. The pcb image is a matrix in which the connections are represented by 1's and the empty space by 0's, we use 2's to represent the tool's path. path.py has 3 functions, the first one (scanHorizontal) adds 2's on the left or the right of 1's if they are the beginning or end of a line, it adds a column of 2's the size of the tool's diameter at a tool's radius away from the 1. the second function (scanVertical) is similar but instead of looking and adding on the left or right side, it does on the up or down side. The third function (twoRemoving) removes 2's where there shouldn't be, by looking near the 1's and removing 2's that would make the tool touch the 1.

We then create a sequence of coordinates for the tool to follow to cover all the path we just created. This is done in gcodeCreator.py. We create a sequence of straight lines only, circles or diagonals are a sum of straight lines. The sequence is created by the function *create sequence* that goes through all pixels in the image to find a 2 where the tool will start working. It starts the sequence by a set of coordinates (-1,-1), which means it is starting a new path, and a set of coordinates where the 2 is. Then it uses the function *findDirection* to seek for 2's nearby to find a direction where to travel. It will continue in this direction with the function *findEndOfLine* until it hits the last 2 of the line, adding its coordinates to the sequence, and then seek for another direction until it can't find any 2's. All the 2's covered by the sequence are changed by 3's so the algorithm never cover the same 2 twice. Once it comes to the end of a path, the algorithm will continue looking for 2's where to start paths from until it has looked through all the pixels of the image.

The last file is GcodeBuilder.py, it transforms the sequence of point into a standard gcode file. It does so by changing the coordinates in pixels, into coordinates in mm according to the dimensions of the pcb. If the coordinates are (-1,-1), this means the sequence has finished a path and the tool should not be working until it gets to the next coordinates. The gcode file also starts with a header and ends with a footer to add some configurations and a homing.

### tests

For path.py's function, we tested the three functions with small matrix of 0's and 1's and wrote the expected results manually to compare if the functions returned what we expected. We also tested if the algorithms would still work if it had to write or read out of bound of the image, which is verified in the algorithms. 

The tests for GcodeCreator.py were made in a similar way, with small matrices of 0's and 2's and an expected sequence of coordinates to compare. We also tested if the algorithm had to read out of bound of the image.

For GcodeBuilder.py, we created some coordinates sequences and a similar but simpler algorithm that would give us the resulting gcode. We compared the function's results with the simpler algorithm's results to see if they were the same. We also tested for different pixel sizes.

## Authors

**Ian Lalonde** 

**Marc-Antoine Lafrenière** 
