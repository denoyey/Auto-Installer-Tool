from .utils import Utils
from .installers import InstallerManager
import sys


class Menu:
    def __init__(self):
        self.installer = InstallerManager()
        self.options = {
            "1": ("Install React.js (Vite)", self.installer.install_react_vite),
            "2": ("Install Laravel", self.installer.install_laravel),
            "3": ("Install Next.js", self.installer.install_nextjs),
            "4": ("Install Vue.js (Vite)", self.installer.install_vue_vite),
            "5": ("Install Svelte (Vite)", self.installer.install_svelte_vite),
            "6": ("Install NestJS", self.installer.install_nestjs),
            "7": ("Install Angular", self.installer.install_angular),
            "8": ("Install Express.js", self.installer.install_express),
            "0": ("Exit", self.exit_tool),
        }

    def display_logo(self):
        Utils.clear_screen()
        logo = r"""
   ___         __           ___          __        
  / _ | __ _  / /__  ___   / _ \ ___  _ / /_       
 / __ |/  ' \/ __/ \/ _ \ / // // _ \/ // __/       
/_/ |_/_/_/_/\__/ \___//____/ \___/\__\__/       
                                                 
      --- AUTO INSTALLER TOOL ---
        """
        Utils.print_colored(logo, "OKCYAN")

    def show_menu(self):
        Utils.print_colored("Select an option:", "BOLD")
        for key, value in self.options.items():
            print(f" [{key}] {value[0]}")
        print()

    def run(self):
        while True:
            self.display_logo()
            self.show_menu()
            choice = input("Enter choice: ").strip()

            if choice in self.options:
                action = self.options[choice][1]
                action()
                input("\nPress Enter to continue...")
            else:
                Utils.print_colored("Invalid option, try again.", "FAIL")
                input("\nPress Enter to continue...")

    def exit_tool(self):
        Utils.print_colored("\nExiting... Goodbye!", "OKBLUE")
        sys.exit(0)
