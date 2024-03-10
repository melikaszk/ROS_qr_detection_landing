#!/usr/bin/env python3

# Import necessary libraries
import rospy  # ROS Python API for interfacing with ROS systems
import cv2  # OpenCV library for computer vision tasks
from cv_bridge import CvBridge, CvBridgeError  # Tools for converting between ROS and OpenCV image formats
from sensor_msgs.msg import Image  # ROS message type for images
from mavros_msgs.msg import State  # Message type for drone state (e.g., mode, armed status)
from geometry_msgs.msg import PoseStamped  # Message type for specifying a position and orientation in space
from nav_msgs.msg import Odometry  # Message type for drone odometry information
from mavros_msgs.srv import CommandBool, SetMode, SetModeRequest, CommandBoolRequest  # ROS services for drone commands
from pynput.keyboard import Key, Listener  # Tools for keyboard event handling

# Initialize global variables for drone state and pose
current_state = State()  # Stores the current state of the drone (mode, armed, etc.)
global_pose = Odometry()  # Stores the global position of the drone
local_pose = PoseStamped()  # Stores the target pose (position and orientation)
bridge = CvBridge()  # Object for converting between ROS and OpenCV images

# Callback function for state updates from the drone
def state(msg):
    global current_state
    current_state = msg  # Update global variable with current state information
    rospy.loginfo("Drone Mode: %s, Armed: %s, Connected: %s", current_state.mode, current_state.armed, current_state.connected)

# Callback function for global position updates
def global_position(command):
    global global_pose
    global_pose = command  # Update global variable with current global position information

# Function to set a waypoint
def set_waypoint(x, y, z):
    local_pose.pose.position.x = x
    local_pose.pose.position.y = y
    local_pose.pose.position.z = z
    loc_pub.publish(local_pose)  # Publish the updated waypoint to move the drone

# Callback function for processing images from the camera
def fro_cam_callback(data):
    try:
        cv_image_front = bridge.imgmsg_to_cv2(data, "bgr8")  # Convert ROS image to OpenCV format
        
        qr_detector = cv2.QRCodeDetector()  # Initialize QR code detector
        
        data, bbox, _ = qr_detector.detectAndDecode(cv_image_front)  # Detect and decode QR code
        
        if bbox is not None:  # If QR code is detected
            print("QR Code detected: ", data)
            bbox = bbox.astype(int)  # Ensure bounding box coordinates are integers
            bbox = bbox.reshape((-1, 1, 2))  # Reshape for drawing
            cv2.polylines(cv_image_front, [bbox], True, (255, 0, 0), thickness=2)  # Draw bounding box around QR code
            # Set the drone to land by setting the Z coordinate to 0
            local_pose.pose.position.z = 0.0
            set_waypoint(local_pose.pose.position.x, local_pose.pose.position.y, local_pose.pose.position.z)
        cv2.imshow("Front Camera with QR Detection", cv_image_front)  # Display image with QR code detection
        cv2.waitKey(1)  # Wait for a key press with a timeout of 1ms
    except CvBridgeError as e:
        print(e)  # Print error if there's a problem converting the image

# Keyboard event handler for manual control
def on_press(key):
    print(f"Key pressed: {key}")
    step_size = 0.5  # Define step size for drone movement
    try:
        # Handle movement controls based on key press
        if key.char == 'w':  # Move forward
            local_pose.pose.position.x += step_size
        elif key.char == 's':  # Move backward
            local_pose.pose.position.x -= step_size
        elif key.char == 'a':  # Move left
            local_pose.pose.position.y -= step_size
        elif key.char == 'd':  # Move right
            local_pose.pose.position.y += step_size
        elif key.char == 'r':  # Reset to initial position
            local_pose.pose.position.x = 0.0
            local_pose.pose.position.y = 0.0
            local_pose.pose.position.z = 3.0
    except AttributeError:
        # Handle altitude control with up and down arrow keys
        if key == Key.up:  # Increase altitude
            local_pose.pose.position.z += step_size
        elif key == Key.down:  # Decrease altitude
            local_pose.pose.position.z -= step_size
            
    # Apply the updated waypoint after key press
    set_waypoint(local_pose.pose.position.x, local_pose.pose.position.y, local_pose.pose.position.z)


# Start keyboard listener in a separate thread to listen for key presses
listener = Listener(on_press=on_press)
listener.start()

# Main function
if __name__ == "__main__":
    rospy.init_node("Qr_landing")  # Initialize ROS node
    
    # Initialize ROS subscribers and publishers
    state_sub = rospy.Subscriber("/mavros/state", State, callback=state)
    global_sub = rospy.Subscriber("/mavros/global_position/local", Odometry, callback=global_position)
    loc_pub = rospy.Publisher("/mavros/setpoint_position/local", PoseStamped, queue_size=10)
    fro_cam_sub = rospy.Subscriber("/camera/color/image_raw", Image,callback= fro_cam_callback)

    # Initialize ROS service clients for arming the drone and setting its mode
    rospy.wait_for_service("/mavros/cmd/arming")
    arming_client = rospy.ServiceProxy("/mavros/cmd/arming", CommandBool)
    rospy.wait_for_service("/mavros/set_mode")
    mode_client = rospy.ServiceProxy("/mavros/set_mode", SetMode)
    
    rate = rospy.Rate(20)  # Set loop rate

    # Setting the drone to OFFBOARD mode and arming it
    offb_set_mode = SetModeRequest()
    offb_set_mode.custom_mode = 'OFFBOARD'
    arm_cmd = CommandBoolRequest()
    arm_cmd.value = True

    # Initial settings for pose
    local_pose.pose.position.x = 0.0
    local_pose.pose.position.y = 0.0
    local_pose.pose.position.z = 0.0

    # Publish initial settings
    for _ in range(100):
        if rospy.is_shutdown():
            break
        loc_pub.publish(local_pose)

    # Main control loop
    while not rospy.is_shutdown():
        # Check and handle OFFBOARD mode and arming status
        if current_state.mode != 'OFFBOARD' and current_state.connected:
            if mode_client.call(offb_set_mode).mode_sent:
                rospy.loginfo("OFFBOARD enabled")
        elif not current_state.armed:
            if arming_client.call(arm_cmd).success:
                rospy.loginfo("Vehicle armed")
                
        # Continuously publish the updated pose
        loc_pub.publish(local_pose)
        rate.sleep()  # Maintain the loop rate