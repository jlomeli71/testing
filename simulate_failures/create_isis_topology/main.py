import getpass
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, AuthenticationException
from paramiko.ssh_exception import SSHException
import sqlite3

# List of Cisco IOS-XR devices
DEVICES = [
    {
        "ip_address": "10.225.236.130",
        "device_type": "cisco_xr_ssh",
    }
]

DB_FILE = 'devices.db'


def get_login_credentials():
    """
    Prompt the user to enter SSH login credentials.

    Returns:
        tuple: A tuple containing the entered username (str) and password (str).
    """
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    return username, password


def validate_devices(devices, username, password):
    """
    Attempts to connect to each device in the provided list using the given credentials.
    For each device, if the connection is successful, retrieves and normalizes the device prompt,
    then adds the device information to a list of valid devices. Handles connection, authentication,
    and SSH exceptions gracefully, printing error messages for failed connections.

    Args:
        devices (list): List of dictionaries, each containing 'ip_address' and 'device_type' keys.
        username (str): Username for device authentication.
        password (str): Password for device authentication.

    Returns:
        list: List of dictionaries for successfully connected devices, each containing
              'ip_address', 'device_type', and the normalized 'prompt'.
    """
    valid = []
    for device in devices:
        try:
            connection = ConnectHandler(
                ip=device["ip_address"],
                device_type=device["device_type"],
                username=username,
                password=password
            )
            print(f"Connection to {device['ip_address']} successful.")
            prompt = connection.find_prompt().strip()
            # Remove trailing prompt characters
            for char in ('>', '#', '$', '%'):
                if prompt.endswith(char):
                    prompt = prompt[:-1]
            if ":" in prompt:
                prompt = prompt.split(":")[-1].strip()
            valid.append({
                "ip_address": device["ip_address"],
                "device_type": device["device_type"],
                "prompt": prompt
            })
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
    return valid


def insert_into_database(devices):
    """
    Inserts a list of device dictionaries into the SQLite database, ensuring no duplicate entries are added.
    If the 'devices' table does not exist, it is created with columns for IP address, device type, and prompt.
    Each device is only inserted if an identical entry does not already exist in the table.

    Args:
        devices (list of dict): A list of dictionaries, each containing 'ip_address', 'device_type', and 'prompt' keys.

    Returns:
        None
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            ip_address TEXT,
            device_type TEXT,
            prompt TEXT,
            UNIQUE(ip_address, device_type, prompt)
        )
    ''')
    for device in devices:
        cursor.execute('''
            SELECT COUNT(*) FROM devices WHERE ip_address=? AND device_type=? AND prompt=?
        ''', (device['ip_address'], device['device_type'], device['prompt']))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO devices (ip_address, device_type, prompt)
                VALUES (?, ?, ?)
            ''', (device['ip_address'], device['device_type'], device['prompt']))
    conn.commit()
    conn.close()
    print("Device information inserted into database (duplicates avoided).")


def read_from_database():
    """
    Fetches all device records from the devices table in the database.

    Returns:
        list of tuple: A list containing all rows from the devices table.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    rows = cursor.fetchall()
    conn.close()
    return rows


# From devices from sqlite database, access each device and get isis database
def get_isis_database(device, username, password):
    """
    Retrieve the ISIS database from a network device using SSH.

    Args:
        device (dict): A dictionary containing device connection details. 
            Expected keys are 'ip_address' and 'device_type'.
        username (str): The username for device authentication.
        password (str): The password for device authentication.

    Returns:
        str or None: The output of the 'show isis database graph' command if successful, 
            otherwise None if an error occurs.

    Raises:
        Exception: Prints an error message if unable to retrieve the ISIS database.
    """
    try:
        connection = ConnectHandler(
            ip=device['ip_address'],
            device_type=device['device_type'],
            username=username,
            password=password
        )
        isis_output = connection.send_command('show isis database graph')
        connection.disconnect()
        return isis_output
    except Exception as e:
        print(f"Error retrieving ISIS database for {device['ip_address']}: {e}")
        return None

    
def main():
    """
    Main function to validate network devices, store their information in a database, 
    and retrieve ISIS database information from the devices.
    """
    username, password = get_login_credentials()
    valid_devices = validate_devices(DEVICES, username, password)
    print("Validated devices:")
    for device in valid_devices:
        print(f"IP: {device['ip_address']}, Device Type: {device['device_type']}, Prompt: {device['prompt']}")

    insert_into_database(valid_devices)

    print("Retrieved valid devices from database:")
    db_devices = read_from_database()
    for device in db_devices:
        print(f"IP: {device[0]}, Device Type: {device[1]}, Prompt: {device[2]}")

    # Example of retrieving ISIS database from a device
    if valid_devices:
        isis_database = get_isis_database(valid_devices[0], username, password)
        if isis_database:
            print(f"ISIS Database for {valid_devices[0]['ip_address']}:\n{isis_database}")
        else:
            print("Failed to retrieve ISIS database.")


# Note: Replace 'your_username' and 'your_password' with actual credentials or modify the code to use the credentials obtained from user input.

if __name__ == "__main__":
    main()

# This code is designed to connect to Cisco IOS-XR devices, validate connections, store device information in a SQLite database, and retrieve ISIS databases from the devices.
# Ensure you have the required libraries installed: netmiko, paramiko, sqlite3.