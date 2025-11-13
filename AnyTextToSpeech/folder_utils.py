import os


def make_dir(folder_name):
    try:
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    except FileExistsError:
        print(f"Folder '{folder_name}' already exists.")
    except FileNotFoundError:
        print(f"Error: Parent directories do not exist for '{folder_name}'.")
