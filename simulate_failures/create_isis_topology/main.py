import getpass
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, AuthenticationException
from paramiko.ssh_exception import SSHException
import sqlite3

# List of Cisco IOS-XR devices
DEVICES = [
    {
        "ip_address": "10.225.236.130",
        "device_type": "cisco_xr",
    }
]

DB_FILE = 'devices.db'


def get_login_credentials():
    """Prompt user for SSH credentials."""
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    return username, password


def validate_devices(devices, username, password):
    """Validate connection to each device and collect valid ones."""
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
            prompt = connection.find_prompt().strip('>%$#')
            if ":" in prompt:
                prompt = prompt.split(":")[1].strip()
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
    """Insert valid device information into the SQLite database without duplicates."""
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
    """Read device information from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    rows = cursor.fetchall()
    conn.close()
    return rows


def main():
    username, password = get_login_credentials()
    valid_devices = validate_devices(DEVICES, username, password)
    print("Validated devices:")
    for device in valid_devices:
        print(f"IP: {device['ip_address']}, Device Type: {device['device_type']}, Prompt: {device['prompt']}")

    insert_into_database(valid_devices)

    print("Retrieved valid devices from database:")
    for device in read_from_database():
        print(f"IP: {device[0]}, Device Type: {device[1]}, Prompt: {device[2]}")

    print("Script completed successfully.")


if __name__ == "__main__":
    main()
