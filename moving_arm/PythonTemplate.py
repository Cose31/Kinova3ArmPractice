import sys
import os
import time
import threading


#*******import the library require for Read_CSV function*******
import csv
#*******End here*******

from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient

from kortex_api.autogen.messages import Base_pb2, BaseCyclic_pb2, Common_pb2

# Maximum allowed waiting time during actions (in seconds)
TIMEOUT_DURATION = 20

# Create closure to set an event after an END or an ABORT
def check_for_end_or_abort(e):
    """Return a closure checking for END or ABORT notifications

    Arguments:
    e -- event to signal when the action is completed
        (will be set when an END or ABORT occurs)
    """
    def check(notification, e = e):
        print("EVENT : " + \
              Base_pb2.ActionEvent.Name(notification.action_event))
        if notification.action_event == Base_pb2.ACTION_END \
        or notification.action_event == Base_pb2.ACTION_ABORT:
            e.set()
    return check
""" 
def move_to_home_position(base):
    # Make sure the arm is in Single Level Servoing mode
    base_servo_mode = Base_pb2.ServoingModeInformation()
    base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
    base.SetServoingMode(base_servo_mode)
    
    # Move arm to ready position
    print("Moving the arm to a safe position")
    action_type = Base_pb2.RequestedActionType()
    action_type.action_type = Base_pb2.REACH_JOINT_ANGLES
    action_list = base.ReadAllActions(action_type)
    action_handle = None
    for action in action_list.action_list:
        if action.name == "Home":
            action_handle = action.handle

    if action_handle == None:
        print("Can't reach safe position. Exiting")
        return False

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )

    base.ExecuteActionFromReference(action_handle)
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Safe position reached")
    else:
        print("Timeout on action notification wait")
    return finished
"""
#*******Write the function called move_to_zero_position or move_to_retract_position depending on your UCID*******
#*******Use the move_to_home_position function to write move_to_zero_position or move_to_retract_position*******
#*******Start here*******

def move_to_zero_position(base):
    # Make sure the arm is in Single Level Servoing mode
    base_servo_mode = Base_pb2.ServoingModeInformation()
    base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
    base.SetServoingMode(base_servo_mode)
    
    # Move arm to ready position
    print("Moving the arm to zero position")
    action_type = Base_pb2.RequestedActionType()
    action_type.action_type = Base_pb2.REACH_JOINT_ANGLES
    action_list = base.ReadAllActions(action_type)
    action_handle = None
    for action in action_list.action_list:
        if action.name == "Zero":
            action_handle = action.handle

    if action_handle == None:
        print("Can't reach zero position. Exiting")
        return False

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )

    base.ExecuteActionFromReference(action_handle)
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Zero position reached")
    else:
        print("Timeout on action notification wait")
    return finished
#*******Function end here*******

def angular_action_movement(base,angles):
    
    print("Starting angular action movement ...")
    action = Base_pb2.Action()
    action.name = "Example angular action movement"
    action.application_data = ""

    actuator_count = base.GetActuatorCount()

    # Place arm straight up
    for joint_id in range(actuator_count.count):
        joint_angle = action.reach_joint_angles.joint_angles.joint_angles.add()
        joint_angle.joint_identifier = joint_id
        joint_angle.value = angles[joint_id]

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )
    
    print("Executing action")
    base.ExecuteAction(action)

    print("Waiting for movement to finish ...")
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Angular movement completed")
    else:
        print("Timeout on action notification wait")
    return finished

def cartesian_action_movement(base, position,orientation,velocity):
    
    print("Starting Cartesian action movement ...")
    action = Base_pb2.Action()
    action.name = "Example Cartesian action movement"
    action.application_data = ""

    #feedback = base_cyclic.RefreshFeedback()

    cartesian_pose = action.reach_pose.target_pose
    #speed
    speed=action.reach_pose.constraint.speed
    speed.translation=velocity
    #
    cartesian_pose.x = position[0]         # (meters)
    cartesian_pose.y = position[1]    # (meters)
    cartesian_pose.z = position[2]    # (meters)
    cartesian_pose.theta_x = orientation[0] # (degrees)
    cartesian_pose.theta_y = orientation[1] # (degrees)
    cartesian_pose.theta_z = orientation[2] # (degrees)

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )

    print("Executing action")
    base.ExecuteAction(action)

    print("Waiting for movement to finish ...")
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Cartesian movement completed")
    else:
        print("Timeout on action notification wait")
    return finished

#*******Write the Read_CSV function*******
#*******Start here*******

def read_csv(filename, angle, position, orientation, gripper_position, translation_speed, action_id):
    """
    Reads a Kinova Gen3 action CSV file and extracts required information.

    Parameters
    ----------
    filename : str
        Path to the CSV file
    angle : list (2D)
        Joint angles (angular motion)
    position : list (2D)
        Cartesian positions (x,y,z for pose)
    orientation : list (2D)
        Cartesian orientation (thetaX, thetaY, thetaZ)
    gripper_position : list
        Finger positions
    translation_speed : list
        Pose translation speed constraints
    action_sequence : list
        Action ID (6=pose, 7=angular, 33=finger)
    """
    with open(filename, newline='', mode='r') as file:
        reader = csv.reader(file)
        for lines in reader:
            #Assuming the csv columns are in the order of angle1, angle2, angle3, angle4, angle5, angle6, 
            # posX, posY, posZ, oriX, oriY, oriZ, gripPos, speed, action

            for row in reader:
                if not row:  # skip empty rows
                    continue

                action_type = row[4].strip()  # 5th column = action ID
                action_id.append(int(action_type))

                #THESE ARE GOOD
                if action_type == "6":  # Cartesian Pose
                    pos = [float(row[27]), float(row[28]), float(row[29])]   # X,Y,Z (cols 28-30)
                    ori = [float(row[30]), float(row[31]), float(row[32])]   # θX,θY,θZ (cols 31-33)
                    spd = float(row[33]) if row[33] else 0.0                 # Speed (col 34)

                    position.append(pos)
                    orientation.append(ori)
                    translation_speed.append(spd)

                #
                elif action_type == "7":  # Angular Motion
                    # Joint angles in columns 6-20 (0-based: 5-19, step by 2 as there identifiers are in between)
                    joints = [float(row[i]) for i in range(5, 19, 2)]
                    angle.append(joints)

                elif action_type == "33":  # Finger Position
                    grip = float(row[24]) if row[24] else 0.0  # col 25
                    gripper_position.append(grip)

    return angle, position, orientation, gripper_position, translation_speed, action_id
#*******Function end here*******

def pretty_print_2d(label, array):
    print(f"\n{label}:")
    for i, subarray in enumerate(array):
        print(f"  [{i}] {subarray}")

def main():
    
    # Import the utilities helper module
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import utilities

    # Parse arguments
    args = utilities.parseConnectionArguments()
    
    # Create connection to the device and get the router
    #with utilities.DeviceConnection.createTcpConnection(args) as router:
    angle=[]
    position=[]
    orientation=[]
    gripper_position=[]
    translation_speed=[]
    action_sequence=[]
    
    #*******Add the other require variable below******* 
    
    #*******Add the address of the CSV below*******
    Filename = './Practice.csv'
    
    # Create required services
    # base = BaseClient(router)
    # base_cyclic = BaseCyclicClient(router)
    #gripper services
    # Create the GripperCommand we will send
    gripper_command = Base_pb2.GripperCommand()
    gripper_command.mode = Base_pb2.GRIPPER_POSITION
    finger = gripper_command.gripper.finger.add()
    finger.finger_identifier = 1
    
    #read the marker placing csv file
    read_csv(Filename, angle, position, orientation, gripper_position, 
                translation_speed, action_sequence)
    
    print("CSV file read completed")
    print(f"Number of actions to execute: {len(action_sequence)}")
    print("Action sequence:", action_sequence)
    pretty_print_2d("Angle data:", angle)
    print("Position data:", position)
    print("Orientation data:", orientation)
    print("Gripper position data:", gripper_position)
    print("Translation speed data:", translation_speed)
    print("Starting the action sequence...")
    success=True
    
    #*******Write the loop that perform the action*******
    #*******start here*******
    #use the variable "success" to know that all the action are perform
    with utilities.DeviceConnection.createTcpConnection(args) as router:
        base = BaseClient(router)
        base_cyclic = BaseCyclicClient(router)
        
        #move to zero position
        success=move_to_zero_position(base)
        
        if not success:
            print("Failed to move to zero position. Exiting.")
            return 1
        
        for i, action_type in enumerate(action_sequence):
            if action_type == 6:  # Cartesian Pose
                pos = position.pop(0)
                ori = orientation.pop(0)
                spd = translation_speed.pop(0)
                print(f"\nExecuting Cartesian action {i+1} with position {pos}, orientation {ori}, speed {spd}")
                success = cartesian_action_movement(base, pos, ori, spd)
            
            elif action_type == 7:  # Angular Motion
                joints = angle.pop(0)
                print(f"\nExecuting Angular action {i+1} with joint angles {joints}")
                success = angular_action_movement(base, joints)
            
            elif action_type == 33:  # Finger Position
                grip = gripper_position.pop(0)
                print(f"\nExecuting Gripper action {i+1} with finger position {grip}")
                finger.value = grip
                base.SendGripperCommand(gripper_command)
                time.sleep(2)  # wait for the gripper to move
            
            else:
                print(f"\nUnknown action type {action_type} at action {i+1}. Skipping.")
                continue
            
            if not success:
                print(f"Action {i+1} failed. Exiting sequence.")
                break
    #*******end the loop here*******
    return 0 if success else 1
        
if __name__ == "__main__":
    exit(main())
