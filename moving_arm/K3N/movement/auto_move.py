from email.mime import base
from logging import Logging
from action_frame import ActionFrame

import sys
import os
import time
import threading
import csv

from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient
from kortex_api.autogen.messages import Base_pb2, BaseCyclic_pb2, Common_pb2

ACTION_TIMEOUT_DURATION = 20

class AutonomousMovement:

    def __init__(self):
        self.storedLocations = {}  # Dictionary[Location]

    def runSequence(self, csvPath: str) -> str:
        Logging.logInfo(f"Running sequence from: {csvPath}")
        return "OK"

    def executeCommand(self) -> str:
        Logging.logInfo("Executing command...")
        return "OK"

    def moveArm(self, frame: ActionFrame) -> str:
        Logging.logInfo("Moving arm using ActionFrame")
        # Will use functions defined below to perform the movement
        # e.g., self.cartesian_action_movement(...) or self.angular_action_movement(...)
        # depending on frame contents, ie: action type
        
        return "OK"
    
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

    def angular_action_movement(base, angles):
    
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
        finished = e.wait(ACTION_TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)

        if finished:
            print("Angular movement completed")
        else:
            print("Timeout on action notification wait")
        return finished
    
    def cartesian_action_movement(base, position,orientation,velocity):
    
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
        finished = e.wait(ACTION_TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)

        if finished:
            print("Cartesian movement completed")
        else:
            print("Timeout on action notification wait")
        return finished

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
        finished = e.wait(ACTION_TIMEOUT_DURATION)
        base.Unsubscribe(notification_handle)

        if finished:
            print("Safe position reached")
        else:
            print("Timeout on action notification wait")
        return finished