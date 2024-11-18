# modules/command_executor.py
import subprocess
import shlex
import os
import time


class CommandExecutor:
    def execute(self, command):
        """Execute system command and return output"""
        try:
            # Clean up command to prevent double sudo
            command = command.replace("sudo sudo", "sudo")
            if command.startswith("nmap") and not command.startswith("sudo"):
                command = f"sudo {command}"

            print(f"Executing command: {command}")

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

            output = []
            start_time = time.time()

            while True:
                # Check if process has finished
                return_code = process.poll()

                # Read output
                for line in process.stdout:
                    print(f"Output: {line.strip()}")
                    output.append(line)

                # Read errors
                for line in process.stderr:
                    print(f"Error: {line.strip()}")
                    output.append(f"ERROR: {line}")

                # Show elapsed time every 30 seconds
                if int(time.time() - start_time) % 30 == 0:
                    elapsed = int(time.time() - start_time)
                    print(f"Scan in progress... ({elapsed} seconds elapsed)")

                # Check if process has finished
                if return_code is not None:
                    break

                time.sleep(1)

            # Get any remaining output
            stdout, stderr = process.communicate()
            if stdout:
                output.append(stdout)
            if stderr:
                output.append(f"ERROR: {stderr}")

            if return_code != 0:
                raise subprocess.CalledProcessError(return_code, command)

            result = "\n".join(output).strip()
            if not result:
                raise Exception("Command produced no output")

            return result

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            raise Exception(f"Command execution failed: {error_msg}")
        except Exception as e:
            raise Exception(f"Error executing command: {str(e)}")
