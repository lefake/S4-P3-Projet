# Device Communication

This code is use to communicate with the device

## Getting Started

To use this UI you must have a GCode file to sent to the device unless you want to control manually the device.

### Prerequisites

Since the program is coded in python, you need to install python, we used python 3.7.
You can use an IDE or cmd to launch the program or the UI.

## Using the program

After downloading the project,
You can launch CommunicationMain.py in S4-P3-Projet/devicecommunication/ for the user interface of the program.

### Automatic mode

Enter the parameters in the proper boxes:

```
- The GCode file's path.
- COM port of the OpenCR (ex: COM8).
- The communication baudrate of the OpenCR.
- Maximum communication time in seconds.
  This is the maximum time to accept an anwser when a command is request.
- Sleep inital time in seconds. 
  This is the boot time of the OpenCR. The time to wait before sending the first command.
```
Once all parameters are entered, you can click on the **Start** button.
At the moment everything runs in one thread so the UI is block by the communication

### Manual mode

The manual mode uses the values entered in the Auto tab so be sure the COM port is specified.
At the moment all +/- buttons dont move the motors in a relative movement. 
Hence it's better to use the text field to move the mototrs
