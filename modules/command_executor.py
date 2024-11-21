# modules/command_executor.py
import subprocess
import time


class CommandExecutor:
    def __init__(self):
        """Initialize command executor"""
        self.verbose = False

    def set_verbose(self, verbose):
        """Set verbose mode"""
        self.verbose = verbose

    def execute(self, command):
        """Execute system command and return output"""
        try:
            # Clean up command to prevent double sudo
            command = command.replace("sudo sudo", "sudo")
            if command.startswith("nmap") and not command.startswith("sudo"):
                command = f"sudo {command}"

            # Start process
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            # Collect output
            stdout, stderr = process.communicate()

            # Check return code
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command, stderr)

            # Combine stdout and stderr if there are any errors
            output = stdout
            if stderr:
                output += f"\nERRORS:\n{stderr}"

            if not output.strip():
                raise Exception("Command produced no output")

            return output.strip()

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            raise Exception(f"Command execution failed: {error_msg}")
        except Exception as e:
            raise Exception(f"Error executing command: {str(e)}")
