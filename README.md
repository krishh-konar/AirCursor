# AirCursor
Emulate mouse actions on your computer with hand gestures. (Still under development :P)

## Dependencies
You can install requirements including OpenCV Binaries using requirements.txt 
`pip install -r requirements.txt`

## OpenCV Issues
This tool is being written using `OpenCV 4.1` and `Python 3.7`.

## How to Use
Upon starting a program, a calibration program opens up. Use the calibration window silders to adjust the HSV values to extract out the palm from the image, as shown on the window. Press `q` once calibration is complete. If you don't edit the values and leave them to zero, the default values will be used.

`Lower_HSV_threshold = [0, 78, 103]`
`Upper_HSV_threshold = [35, 125, 170]`

**Note:** The default values are dependent on a particular environmental conditions and may change considerably from environment to environment. It is advised to calibrate the values once and replace them in the program in order to skip the process.

Once calibration is finished, a newer window pops up showing the contour of hand and controlling the hand, along with mouse control. Press `q` to quit the program. 


## DA WoC WarmUp tasks:

* Learn about Virtual Environments and set up one for Python.
* Compile and Install OpenCV (using or without using CUDA support(nVidia GPU))
* Pull this repo and execute the current program
