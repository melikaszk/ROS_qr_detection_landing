## Overview
This Python script integrates with MAVROS to provide a responsive interface for drone navigation, utilizing WASD and arrow keys for directional movement and altitude adjustments. It uses the OpenCV library to detect a qr code and then land on it. 

## Components
### 1. iris drone model
this model is modified so that it has a camera which sends ROS video outputs. copy the file to '/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models' directory.

### 2. qr_ground
a gazebo model for the qr code. after copying it to the gazebo_models directory, launch gazebo by running the command:

```
gazebo
```
then in the insert section, select qr_ground. this should load the qr code image to your model. next, go to the file tab and choose the 'save world as' and save it as a .world file in the '~/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds' directory. keep in mind to modify your launch file so that it loads your world.

### 3. MAVROS keyboard control and qr code detection (`qr_landing.py`)
this code sends keyboard commands to the drone using MAVROS. After the qr code detection, it lands on the qr code panel in the gazebo world. 

### 4. Launch File (`qr_landing.launch`)
This launch file is used for starting both the Qr_landing.pyscript and the Gazebo classic simulation environment. It's essential for testing the drone's flight path in a virtual setting before any real-world application.

## Usage Instructions
 **Simulation and Control**: Run the following command in your terminal to launch both the `qr_landing.py` script and the Gazebo simulation:

   ```
   roslaunch qr_landing_py qr_landing.launch
   ```

   This command initializes the simulation environment and begins the drone control process.

## Prerequisites
Ensure you have ROS, MAVROS, and Gazebo installed on your system, along with the necessary dependencies for each package.

## Video 
[qr_landing.py](https://drive.google.com/file/d/1ZSuYIc8rOwTO5OXgvvHZDO03DbW1IZwb/view?usp=sharing)https://drive.google.com/file/d/1ZSuYIc8rOwTO5OXgvvHZDO03DbW1IZwb/view?usp=sharing
