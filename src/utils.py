import shutil
import subprocess
import os
import sys


class Utils:
    COLORS = {
        "HEADER": "\033[95m",
        "OKBLUE": "\033[94m",
        "OKCYAN": "\033[96m",
        "OKGREEN": "\033[92m",
        "WARNING": "\033[93m",
        "FAIL": "\033[91m",
        "ENDC": "\033[0m",
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m",
    }

    @staticmethod
    def print_colored(text, color="ENDC"):
        if os.name == "nt":
            os.system("color")
        print(
            f"{Utils.COLORS.get(color, Utils.COLORS['ENDC'])}{text}{Utils.COLORS['ENDC']}"
        )

    @staticmethod
    def check_dependency(command, name):
        if shutil.which(command) is None:
            Utils.print_colored(f"[!] {name} is NOT installed or not in PATH.", "FAIL")
            return False
        return True

    @staticmethod
    def run_command(command, cwd=None):
        try:
            Utils.print_colored(f"[*] Running: {' '.join(command)}", "OKCYAN")
            subprocess.run(command, check=True, cwd=cwd, shell=True)
            Utils.print_colored("[+] Command executed successfully.", "OKGREEN")
            return True
        except subprocess.CalledProcessError as e:
            Utils.print_colored(f"[!] Error executing command: {e}", "FAIL")
            return False
        except Exception as e:
            Utils.print_colored(f"[!] Unexpected error: {e}", "FAIL")
            return False

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")
