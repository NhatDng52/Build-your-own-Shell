import sys
import re
import os
import subprocess
import shlex
from builtin import *

def find_executable(command_name):
    """Check if a command exists in current directory and is executable"""
    file_path = os.path.join(".", command_name)
    return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

def handle_command(command):
    if False:
        pass  
    elif re.match(r'.+>.+', command):
        #redirect output to a file
        print("redirecting output to a file")
        left_part, right_part = command.split('>', 1)
        left_part = left_part.strip()
        right_part = right_part.strip()
        left_node = handle_command(left_part)
        print(f"left_node: {left_node}")
        if left_node:
            try:
                with open(right_part, 'w') as file:
                    file.write(left_node)
            except IOError as e:
                return f"Error writing to {right_part}: {e}"
        return ""
    elif re.match(r'^\s*pwd\s*$', command):
            # Print current working directory
        return pwd()
    elif re.match(r'^\s*cd\s*(.*)$', command):
            # Change directory
        match = re.search(r'^\s*cd\s*(.*)$', command)
        path = match.group(1).strip()
        change_directory(path)
        return ""
    elif re.match(r'^\s*echo\s+(.+)$', command):
            # Extract everything after "echo " (handles leading/trailing spaces)
        match = re.search(r'^\s*echo\s+(.+)$', command)
        text = match.group(1)
        return echo_command(text)

    elif re.match(r'^\s*exit\s*( \d+)?$', command):
            # Extract the exit code if provided, default to last_exit_code
        match = re.search(r'^\s*exit\s*( \d+)?$', command)
        exit_shell(int(match.group(1)) if match.group(1) else 0)
    elif re.match(r'^\s*type\s+(.+)$', command):
        args = command.split()
        for arg in args[1:]:
            if type_command(arg):
                return f"{arg} is a shell built-in command"
            else:
                return f"{arg} : not found"
    elif re.match(r'^\s*cat\s+(.+)$', command):
        # Extract file arguments from "cat" command
        match = re.search(r'^\s*cat\s+(.+)$', command)
        file_args = match.group(1).split()
        return concatenate_files(file_args)

    else:
        # Check if it's an executable in current directory
        try:
            # Use shlex to properly parse quoted arguments
            input_args = shlex.split(command)
            if input_args and find_executable(input_args[0]):
                try:
                        # Execute the local executable
                    executable_path = os.path.join(".", input_args[0])
                    result = subprocess.run([executable_path] + input_args[1:], 
                                            capture_output=True, text=True)
                    if result.stdout:
                        return result.stdout.strip()
                    if result.stderr:
                        return f"Error: {result.stderr.strip()}"
                    last_exit_code = result.returncode
                except Exception as e:
                    return f"Error executing {input_args[0]}: {e}"
                    last_exit_code = 1
            else:
                return f"{command}: command not found"
        except ValueError as e:
            # Handle malformed quotes
            return f"shell: {e}"
            last_exit_code = 1

def main():
    # Wait for user input
    while True:
        sys.stdout.write("$ ")
        command = input()
        
        if not command:
            continue
            
        result = handle_command(command)
        if result:
            print(result)
if __name__ == "__main__":
    main()
