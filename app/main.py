import sys
import re
import os
import subprocess
from builtin import *

def find_executable(command_name):
    """Check if a command exists in current directory and is executable"""
    file_path = os.path.join(".", command_name)
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

def main():

    # Wait for user input
    while True:
        sys.stdout.write("$ ")
        command = input()
        if False:
            pass  
        elif re.match(r'^\s*pwd\s*$', command):
            # Print current working directory
            pwd()
        elif re.match(r'^\s*cd\s*(.*)$', command):
            # Change directory
            match = re.search(r'^\s*cd\s*(.*)$', command)
            path = match.group(1).strip()
            change_directory(path)
            print()
        elif re.match(r'^\s*echo\s+(.+)$', command):
            # Extract everything after "echo " (handles leading/trailing spaces)
            match = re.search(r'^\s*echo\s+(.+)$', command)
            text = match.group(1)
            echo_command(text)

        elif re.match(r'^\s*exit\s*( \d+)?$', command):
            # Extract the exit code if provided, default to last_exit_code
            match = re.search(r'^\s*exit\s*( \d+)?$', command)
            exit_shell(int(match.group(1)) if match.group(1) else 0)
        elif re.match(r'^\s*type\s+(.+)$', command):
            args = command.split()
            for arg in args[1:]:
                if type_command(arg):
                    print(f"{arg} is a shell built-in command")
                else:
                    print(f"{arg} : not found")
        elif re.match(r'^\s*cat\s+(.+)$', command):
            # Extract file arguments from "cat" command
            match = re.search(r'^\s*cat\s+(.+)$', command)
            file_args = match.group(1).split()
            concatenate_files(file_args)    
        else:
            # Check if it's an executable in current directory
            input_args = command.split()
            if input_args and find_executable(input_args[0]):
                try:
                    # Execute the local executable
                    executable_path = os.path.join(".", input_args[0])
                    result = subprocess.run([executable_path] + input_args[1:], 
                                          capture_output=True, text=True)
                    if result.stdout:
                        print(result.stdout.strip())
                    if result.stderr:
                        print(result.stderr.strip(), file=sys.stderr)
                    last_exit_code = result.returncode
                except Exception as e:
                    print(f"Error executing {input_args[0]}: {e}")
                    last_exit_code = 1
            else:
                print(f"{command}: command not found")
            
if __name__ == "__main__":
    main()
