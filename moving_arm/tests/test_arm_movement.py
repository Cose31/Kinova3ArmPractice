from moving_arm.K3N import utilities


with utilities.DeviceConnection.createTcpConnection(args) as router:
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