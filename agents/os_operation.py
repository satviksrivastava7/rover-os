import os
import shutil
import fnmatch

def create_file(file_path, content=""):
    """
    Creates a new file with optional content.

    Args:
        file_path (str): The full path including the filename.
        content (str): The initial content to write to the file (defaults to empty).

    Returns:
        bool: True if the file was created successfully, False otherwise.
    """
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Successfully created file: {file_path}")
        return True
    except FileExistsError:
        print(f"Error: File already exists at {file_path}")
        return False
    except IsADirectoryError:
         print(f"Error: Cannot create file; a directory exists at {file_path}")
         return False
    except PermissionError:
        print(f"Error: Permission denied to create file at {file_path}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while creating file {file_path}: {e}")
        return False

def create_directory(dir_path):
    """
    Creates a new directory. Creates parent directories if they don't exist.

    Args:
        dir_path (str): The path to the directory to create.

    Returns:
        bool: True if the directory was created or already exists, False otherwise.
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Successfully created directory (or it already exists): {dir_path}")
        return True
    except FileExistsError:
        print(f"Error: A file exists at {dir_path} where a directory was expected.")
        return False
    except PermissionError:
        print(f"Error: Permission denied to create directory at {dir_path}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while creating directory {dir_path}: {e}")
        return False

def delete_item(path):
    """
    Deletes a file or a directory (and its contents).

    Args:
        path (str): The path to the file or directory to delete.

    Returns:
        bool: True if the item was deleted, False if it didn't exist or couldn't be deleted.
    """
    if not os.path.exists(path):
        print(f"Error: Item does not exist at {path}")
        return False

    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"Successfully deleted file: {path}")
            return True
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Successfully deleted directory: {path}")
            return True
        else:
            print(f"Error: {path} is not a file or directory. Cannot delete.")
            return False
    except PermissionError:
        print(f"Error: Permission denied to delete {path}")
        return False
    except OSError as e:
        print(f"Error deleting {path}: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while deleting {path}: {e}")
        return False

def rename_item(old_path, new_path):
    """
    Renames a file or directory.

    Args:
        old_path (str): The current path of the item.
        new_path (str): The desired new path/name for the item.

    Returns:
        bool: True if the item was renamed, False otherwise.
    """
    if not os.path.exists(old_path):
        print(f"Error: Item does not exist at {old_path}")
        return False
    if os.path.exists(new_path):
        print(f"Error: Cannot rename to {new_path}; an item already exists there.")
        return False

    try:
        os.rename(old_path, new_path)
        print(f"Successfully renamed '{old_path}' to '{new_path}'")
        return True
    except PermissionError:
        print(f"Error: Permission denied to rename {old_path}")
        return False
    except OSError as e:
        print(f"Error renaming {old_path} to {new_path}: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while renaming {old_path}: {e}")
        return False

def update_file_content(file_path, content, mode='w'):
    """
    Writes content to a file.

    Args:
        file_path (str): The path to the file.
        content (str): The content to write.
        mode (str): File open mode ('w' for overwrite, 'a' for append). Defaults to 'w'.

    Returns:
        bool: True if the file was updated, False otherwise.
    """
    if mode not in ['w', 'a']:
        print(f"Error: Invalid mode '{mode}'. Use 'w' (overwrite) or 'a' (append).")
        return False
    if not os.path.exists(file_path) and mode == 'a':
         print(f"Warning: File {file_path} does not exist. Creating for append mode.")

    try:
        with open(file_path, mode) as f:
            f.write(content)
        print(f"Successfully updated file: {file_path} (mode: {mode})")
        return True
    except IsADirectoryError:
        print(f"Error: Cannot update file; {file_path} is a directory.")
        return False
    except PermissionError:
        print(f"Error: Permission denied to update file at {file_path}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while updating file {file_path}: {e}")
        return False

def read_file_content(file_path):
    """
    Reads the content of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str or None: The content of the file if successful, None otherwise.
    """
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        print(f"Error: File does not exist or is not a file at {file_path}")
        return None

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        print(f"Successfully read file: {file_path}")
        return content
    except PermissionError:
        print(f"Error: Permission denied to read file at {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading file {file_path}: {e}")
        return None

def bulk_rename(directory, pattern, rename_func):
    """
    Renames multiple files in a directory based on a pattern and a renaming function.
    Does NOT operate recursively in subdirectories.

    Args:
        directory (str): The directory to perform renaming in.
        pattern (str): A glob-style pattern (e.g., '*.txt') to filter files.
        rename_func (function): A function that takes the original filename (str)
                                returns the new filename (str) or None to skip.

    Returns:
        dict: A dictionary containing lists of 'renamed' and 'failed' renames.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory not found or is not a directory: {directory}")
        return {'renamed': [], 'failed': []}

    results = {'renamed': [], 'failed': []}
    print(f"Starting bulk rename in '{directory}' for pattern '{pattern}'...")

    try:
        for item_name in os.listdir(directory):
            item_path = os.path.join(directory, item_name)

            if os.path.isfile(item_path) and fnmatch.fnmatch(item_name, pattern):
                try:
                    new_name = rename_func(item_name)
                    if new_name is None or new_name == item_name:
                        continue

                    new_path = os.path.join(directory, new_name)

                    if os.path.exists(new_path):
                         print(f"Warning: Skipping rename of '{item_name}' to '{new_name}'; target already exists.")
                         results['failed'].append({'item': item_name, 'reason': 'Target name already exists'})
                         continue

                    os.rename(item_path, new_path)
                    print(f" Renamed '{item_name}' to '{new_name}'")
                    results['renamed'].append({'old_name': item_name, 'new_name': new_name})

                except Exception as e:
                    print(f" Error renaming '{item_name}': {e}")
                    results['failed'].append({'item': item_name, 'reason': str(e)})

    except PermissionError:
        print(f"Error: Permission denied to list directory contents: {directory}")
    except Exception as e:
        print(f"An unexpected error occurred during bulk rename: {e}")

    print(f"Bulk rename finished. Renamed: {len(results['renamed'])}, Failed: {len(results['failed'])}")
    return results

def bulk_edit(directory, pattern, edit_func):
    """
    Reads, edits (using a function), and writes back content for multiple files.
    Does NOT operate recursively in subdirectories.

    Args:
        directory (str): The directory to perform editing in.
        pattern (str): A glob-style pattern (e.g., '*.txt') to filter files.
        edit_func (function): A function that takes the original file content (str)
                              and returns the modified content (str).

    Returns:
        dict: A dictionary containing lists of 'edited' and 'failed' edits.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory not found or is not a directory: {directory}")
        return {'edited': [], 'failed': []}

    results = {'edited': [], 'failed': []}
    print(f"Starting bulk edit in '{directory}' for pattern '{pattern}'...")

    try:
        for item_name in os.listdir(directory):
            item_path = os.path.join(directory, item_name)

            if os.path.isfile(item_path) and fnmatch.fnmatch(item_name, pattern):
                try:
                    original_content = read_file_content(item_path) 
                    if original_content is None:
                         results['failed'].append({'item': item_name, 'reason': 'Could not read file'})
                         continue 

                    modified_content = edit_func(original_content)

                    success = update_file_content(item_path, modified_content, mode='w') 

                    if success:
                         print(f" Edited '{item_name}'")
                         results['edited'].append(item_name)
                    else:
                         results['failed'].append({'item': item_name, 'reason': 'Could not write file'})


                except Exception as e:
                    print(f" Error editing '{item_name}': {e}")
                    results['failed'].append({'item': item_name, 'reason': str(e)})

    except PermissionError:
        print(f"Error: Permission denied to list directory contents: {directory}")
    except Exception as e:
        print(f"An unexpected error occurred during bulk edit: {e}")

    print(f"Bulk edit finished. Edited: {len(results['edited'])}, Failed: {len(results['failed'])}")
    return results


if __name__ == "__main__":
    test_dir = "os_operations_test_dir"
    create_directory(test_dir)
    print("-" * 20)

    create_file(os.path.join(test_dir, "file1.txt"), "This is file 1.")
    create_file(os.path.join(test_dir, "file2.log"), "Log entry one.\nLog entry two.")
    create_file(os.path.join(test_dir, "another_file.txt")) # Empty file
    create_file(os.path.join(test_dir, "file1.txt"), "Attempting to create file1.txt again.") # Should show error

    create_directory(os.path.join(test_dir, "subdir"))
    create_file(os.path.join(test_dir, "subdir", "nested_file.txt"), "Inside subdir.")

    print("-" * 20)

    content1 = read_file_content(os.path.join(test_dir, "file1.txt"))
    if content1 is not None:
        print(f"Content of file1.txt:\n{content1}")

    content_non_existent = read_file_content(os.path.join(test_dir, "non_existent.txt")) # Should show error

    print("-" * 20)

    update_file_content(os.path.join(test_dir, "another_file.txt"), "New content for empty file.")
    update_file_content(os.path.join(test_dir, "file2.log"), "Appending new log.\n", mode='a')
    update_file_content(os.path.join(test_dir, "non_existent_update.txt"), "This should create a new file.") # Should create

    print("-" * 20)

    content2 = read_file_content(os.path.join(test_dir, "file2.log"))
    if content2 is not None:
        print(f"Content of file2.log after append:\n{content2}")

    print("-" * 20)

    rename_item(os.path.join(test_dir, "another_file.txt"), os.path.join(test_dir, "renamed_file.txt"))
    rename_item(os.path.join(test_dir, "subdir"), os.path.join(test_dir, "renamed_subdir")) # Rename directory

    print("-" * 20)

    def add_suffix_func(original_name):
        if original_name.endswith('.txt'):
            base, ext = os.path.splitext(original_name)
            return f"{base}_processed{ext}"
        return None 

    bulk_rename(test_dir, "*.txt", add_suffix_func)

    print("-" * 20)

    def add_header_func(original_content):
        header = "--- Log Start ---\n"
        return header + original_content

    bulk_edit(test_dir, "*.log", add_header_func)

    print("-" * 20)

    print("Cleaning up test directory...")
    delete_item(test_dir) 

    if not os.path.exists(test_dir):
        print(f"Successfully deleted {test_dir}")
    else:
        print(f"Failed to delete {test_dir}")