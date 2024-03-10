## Overview
This Python script integrates with MAVROS to provide a responsive interface for drone navigation, utilizing WASD and arrow keys for directional movement and altitude adjustments. It uses the OpenCV library to detect a qr code and then land on it. 

## Components

### 2. MAVROS keyboard control and qr code detection (`qr_landing.py`)
this code sends keyboard commands to the drone using MAVROS. After the qr code detection, it lands on the qr code panel in the gazebo world. 

### 3. Launch File (`qr_landing.launch`)
This launch file is used for starting both the Qr_landing.pyscript and the Gazebo classic simulation environment. It's essential for testing the drone's flight path in a virtual setting before any real-world application.

## Usage Instructions

1. **CSV File Creation**: Start by running the `make_csv.py` script to create the flight path CSV file. This step is crucial as it defines the trajectory for the drone.

2. **Simulation and Control**: Run the following command in your terminal to launch both the `qr_landing.py` script and the Gazebo simulation:

   ```
   roslaunch qr_landing_py qr_landing.launch
   ```

   This command initializes the simulation environment and begins the drone control process.

## Prerequisites
Ensure you have ROS, MAVROS, and Gazebo installed on your system, along with the necessary dependencies for each package.

## Video 
[qr_landing.py](https://drive.google.com/file/d/1ZSuYIc8rOwTO5OXgvvHZDO03DbW1IZwb/view?usp=sharing)https://drive.google.com/file/d/1ZSuYIc8rOwTO5OXgvvHZDO03DbW1IZwb/view?usp=sharing
