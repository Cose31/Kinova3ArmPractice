
import sys
import os
import time

from kortex_api.autogen.client_stubs.DeviceManagerClientRpc import DeviceManagerClient
from kortex_api.autogen.client_stubs.InterconnectConfigClientRpc import InterconnectConfigClient
from kortex_api.autogen.messages import Session_pb2, Base_pb2, Common_pb2, InterconnectConfig_pb2, DeviceManager_pb2
import utilities

def createNewBridge(type, interface_name, device_ip):
    if type == "ETHERNET":
        with utilities.DeviceConnection.createTcpConnection(interface_name, device_ip) as router:
            ethernet_bridge = EthernetBridgeConfig(router)
            ethernet_bridge.EnableEthernetBridge()
    if type == "UART":
        with utilities.DeviceConnection.createUARTConnection(interface_name, device_ip) as router:
            uart_bridge = UARTBridgeConfig(router)
            uart_bridge.EnableUARTBridge()

class EthernetBridgeConfig:
    def __init__(self, router):
        # Create required services        
        self.interconnect_config = InterconnectConfigClient(router)
        self.device_manager = DeviceManagerClient(router)
        
        self.interconnect_device_id = self.GetDeviceIdFromDevType(Common_pb2.INTERCONNECT, 0)
        if (self.interconnect_device_id is None):
            print ("Could not find the Interconnect in the device list, exiting...")
            sys.exit(0)

    def GetDeviceIdFromDevType(self, device_type, device_index = 0):
        devices = self.device_manager.ReadAllDevices()

        current_index = 0
        for device in devices.device_handle:
            if device.device_type == device_type:
                if current_index == device_index:
                    print ("Found the Interconnect on device identifier {}".format(device.device_identifier))
                    return device.device_identifier
                current_index += 1
        return None

    def EnableEthernetBridge(self):

        # Configure the Interconnect to enable the bridge
        ethernet_configuration = InterconnectConfig_pb2.EthernetConfiguration()
        ethernet_configuration.device = InterconnectConfig_pb2.ETHERNET_DEVICE_EXPANSION
        ethernet_configuration.enabled = True
        ethernet_configuration.speed = InterconnectConfig_pb2.ETHERNET_SPEED_100M
        ethernet_configuration.duplex = InterconnectConfig_pb2.ETHERNET_DUPLEX_FULL
        try:
            self.interconnect_config.SetEthernetConfiguration(ethernet_configuration, self.interconnect_device_id)
        except Exception as e:
            print ("An unexpected error occured : {}".format(e))

class UARTBridgeConfig:

        