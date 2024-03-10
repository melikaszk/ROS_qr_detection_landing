## Overview
 This Python script integrates with MAVROS to offer a responsive way to control your drone. With just the WASD keys for direction and arrow keys for altitude, you can fly your drone .I've incorporated OpenCV to smartly detect a QR code and execute landing.
 
## Components
### 1. iris drone model
I've tailored the Iris drone model to include a camera that sends ROS video outputs. To get started, simply copy the modified model into your '/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_gazebo-classic/models' directory.

### 2. qr_ground
After copying it to the gazebo_models directory, launch gazebo with:

```
gazebo
```
Navigate to the insert section, select qr_ground, the QR code image appears in your model. Next, save your world by going to the file tab and choosing 'save world as'. Save it as a .world file in the '~/PX4-Autopilot/Tools/simulation/gazebo-classic/sitl_gazebo-classic/worlds' directory. Remember to adjust your launch file to load your custom world.

### 3. MAVROS keyboard control and qr code detection (`qr_landing.py`)
This code allows the drone to respond to keyboard commands via MAVROS. Once the QR code is detected, the drone lands on the QR code panel in the Gazebo world.

### 4. Launch File (`qr_landing.launch`)
Use this launch file to kickstart both the qr_landing.py script and the Gazebo classic simulation environment. It's a crucial step for validating the drone's flight capabilities virtually before taking on the real world.

## Usage Instructions
 **Simulation and Control**: Launch your drone simulation and control interface with:


   ```
   roslaunch qr_landing_py qr_landing.launch
   ```

  This command sets the stage for your simulation environment and activates the drone control sequence. 

## Prerequisites
Ensure you have ROS, MAVROS, and Gazebo installed on your system, along with the necessary dependencies for each package.

## Video 
in persian:
[qr_landing.py](https://drive.google.com/file/d/1ZSuYIc8rOwTO5OXgvvHZDO03DbW1IZwb/view?usp=sharing)https://drive.google.com/file/d/1ZSuYIc8rOwTO5OXgvvHZDO03DbW1IZwb/view?usp=sharing
