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

valid_devices = []

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
            if ":" in prompt:
                prompt = prompt.split(":")[1].strip()
            else:
                pass           
            valid_devices.append({"ip_address": device["ip_address"], "device_type":device["device_type"],"prompt": prompt})
            print(f"Device prompt: {prompt}")
            connection.disconnect()

        except NetMikoTimeoutException:
                print(f"Failed to connect to {device['ip_address']}: Timeout Exception")
        except AuthenticationException:
                print(f"Failed to connect to {device['ip_address']}: Authentication Exception")
        except SSHException:
                print(f"Failed to connect to {device['ip_address']}: SSH Exception")
        except Exception as error:
                print(f"Failed to connect to {device['ip_address']}: {error}")

# get user and password for ssh access
username, password = get_login_credentials()
validate_devices(devices, username, password)
print("Validated devices:")
for device in valid_devices:
    print(f"IP: {device['ip_address']}, Device Type: {device['device_type']}, Prompt: {device['prompt']}")

# Function to insert data into sqlite database from valid_devices
def insert_into_database(valid_devices):
    """Insert valid device information into the database."""
    import sqlite3

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('devices.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            ip_address TEXT,
            device_type TEXT,
            prompt TEXT
        )
    ''')

    # Insert valid if not in table
    for device in valid_devices:
        cursor.execute('''
            INSERT INTO devices (ip_address, device_type, prompt)
            VALUES (?, ?, ?)
        ''', (device['ip_address'], device['device_type'], device['prompt']))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Device information inserted into database.")

# Insert valid devices into the database
insert_into_database(valid_devices)

# Read data from the database to get more commands for further processing
def read_from_database():
    """Read device information from the database."""
    import sqlite3

    # Connect to the SQLite database
    conn = sqlite3.connect('devices.db')
    cursor = conn.cursor()

    # Query to select all devices
    cursor.execute('SELECT * FROM devices')
    rows = cursor.fetchall()    

    # Print the device information
    for row in rows:
        print(f"IP: {row[0]}, Device Type: {row[1]}, Prompt: {row[2]}")

    # Close the connection
    conn.close()
    return rows

valid_devices = read_from_database
print("Retrieved valid devices from database:")
for device in valid_devices():
    print(f"IP: {device[0]}, Device Type: {device[1]}, Prompt: {device[2]}")

# End of script 
print("Script completed successfully.")