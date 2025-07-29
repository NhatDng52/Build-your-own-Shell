# implement built-in shell commands
import os
import sys
import re
import subprocess
import shlex  # Use shlex for parsing shell-like syntax


shell_buildin_commands = ["echo", "exit", "type", "pwd", "cd", "cat"]

def echo_command(text):
    """Handle the echo command."""
    if not text:
        print()  # Just print a newline if no arguments
    else:
        # Join arguments with a single space and print
        text = shlex.split(text, posix=True)  # Use shlex to handle quotes and spaces
        return " ".join(text)  # Join the parts with a single space and print
def pwd():
    """Print the current working directory."""
    return os.getcwd()
def change_directory(path):
    """Change the current working directory."""

    if not path or path == "~":
        # cd with no arguments or ~ goes to home directory
        path = os.path.expanduser("~")
    elif path == "..":
        # cd .. goes to parent directory
        path = os.path.dirname(os.getcwd())
    elif not os.path.isabs(path):
        # Relative path - make it absolute
        path = os.path.join(os.getcwd(), path)
                
    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: {path}: No such file or directory")
    except PermissionError:
        print(f"cd: {path}: Permission denied")
    except NotADirectoryError:
        print(f"cd: {path}: Not a directory")
def concatenate_files(file_args):
    result = ""
    for filename in file_args:
        try:
            with open(filename, 'r') as file:
                content = file.read()
                result += content
        except FileNotFoundError:
            print(f"cat: {filename}: No such file or directory")
        except PermissionError:
            print(f"cat: {filename}: Permission denied")
        except IsADirectoryError:
            print(f"cat: {filename}: Is a directory")
        except Exception as e:
            print(f"cat: {filename}: {e}")
    return result

def exit_shell(exit_code = 0):
    sys.exit(exit_code)
def type_command(name):
    if name in shell_buildin_commands:
        return True
    else:
        return False