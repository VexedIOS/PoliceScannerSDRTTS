import os


def make_dir(folder_name):
    try:
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    except FileExistsError:
        print(f"Folder '{folder_name}' already exists.")
    except FileNotFoundError:
        print(f"Error: Parent directories do not exist for '{folder_name}'.")

def check_all_files_in_folder(folder_path):
    os_paths = []
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        # Check if the entry is a file
        if os.path.isfile(full_path):
            os_paths.append(full_path)
    return os_paths
