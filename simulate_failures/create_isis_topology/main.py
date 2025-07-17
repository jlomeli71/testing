import getpass
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from paramiko.ssh_exception import SSHException

# This Python script access several Cisco IOS-XR routers and get ISIS topology information.

# List of Cisco devices with IOS_XR
devices = [{"ip_address":"10.225.236.130",
           "device_type":"cisco_xr",},
           ]
# Function to get logging credentials for ssh access
def get_login_credentials():
    """Get username and password for SSH access to router devices securely."""
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    return username, password


# Function to validate availability of devices using Netmiko validate the connection to each device getting the prompt
def validate_devices(devices, username, password):
    """Validate the connection to each device."""
    for device in devices:
        try:
            connection = ConnectHandler(
                ip=device["ip_address"],
                device_type=device["device_type"],
                username=username,
                password=password
            )
            print(f"Connection to {device['ip_address']} successful.")

            prompt = connection.find_prompt().strip('>%$#')
            print(f"Device prompt: {prompt}")
            
            connection.disconnect()

        except NetMikoTimeoutException:
                print(f"Failed to connect to {device['ip_address']}: Timeout Exception")
        except AuthenticationException:
                print(f"Failed to connect to {device['ip_address']}: Authentication Exception")
        except SSHException:
                print(f"Failed to connect to {device['ip_address']}: SSH Exception")
        except Exception as e:
                print(f"Failed to connect to {device['ip_address']}: {e}")

# get user and password for ssh access
username, password = get_login_credentials()
validate_devices(devices, username, password)

