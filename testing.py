def read_file_contents(file_path):
    """
    Reads the contents of a file and returns it as a string.

    :param file_path: The path to the file to be read.
    :return: The contents of the file as a string.
    """
    try:
        with open(file_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    finally:
        pass
        file.close()  

file = 'file.txt'  # Replace with the actual file path
# Call the function to read the file contents
read_file_contents(file)