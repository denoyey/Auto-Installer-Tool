import os
import shutil
import urllib.request
from .utils import Utils


class InstallerManager:
    def __init__(self, projects_dir="projects"):
        self.projects_dir = os.path.abspath(projects_dir)
        self.bin_dir = os.path.abspath("bin")
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)
        if not os.path.exists(self.bin_dir):
            os.makedirs(self.bin_dir)

    def _ensure_category_dir(self, category):
        category_path = os.path.join(self.projects_dir, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        return category_path

    def _get_composer_command(self):
        if shutil.which("composer"):
            return ["composer"]

        composer_phar = os.path.join(self.bin_dir, "composer.phar")
        if not os.path.exists(composer_phar):
            Utils.print_colored(
                "[*] Global Composer not found. Downloading composer.phar...", "WARNING"
            )
            try:
                url = "https://getcomposer.org/composer.phar"
                urllib.request.urlretrieve(url, composer_phar)
                Utils.print_colored(
                    "[+] composer.phar downloaded successfully.", "OKGREEN"
                )
            except Exception as e:
                Utils.print_colored(
                    f"[!] Failed to download composer.phar: {e}", "FAIL"
                )
                return None

        return ["php", composer_phar]

    def install_react_vite(self):
        Utils.print_colored("\n--- Install React (via Vite) ---", "HEADER")
        if not Utils.check_dependency("npm", "Node.js/npm"):
            return

        project_name = input("Enter project name: ").strip()
        if not project_name:
            return

        target_dir = self._ensure_category_dir("reactjs")
        cmd = [
            "npm",
            "create",
            "vite@latest",
            project_name,
            "--",
            "--template",
            "react",
        ]

        if Utils.run_command(cmd, cwd=target_dir):
            Utils.print_colored(
                f"\n[+] React project '{project_name}' created successfully!", "OKGREEN"
            )
            self._print_post_install_instructions(
                "reactjs", project_name, ["npm install", "npm run dev"]
            )

    def install_laravel(self):
        Utils.print_colored("\n--- Install Laravel ---", "HEADER")

        if not Utils.check_dependency("php", "PHP"):
            Utils.print_colored(
                "[!] PHP is required but not installed/in PATH.", "FAIL"
            )
            return

        composer_cmd = self._get_composer_command()
        if not composer_cmd:
            return

        project_name = input("Enter project name: ").strip()
        if not project_name:
            return

        target_dir = self._ensure_category_dir("laravel")

        full_cmd = composer_cmd + [
            "create-project",
            "laravel/laravel",
            project_name,
            "--ignore-platform-req=ext-fileinfo",
        ]

        if Utils.run_command(full_cmd, cwd=target_dir):
            Utils.print_colored(
                f"\n[+] Laravel project '{project_name}' created successfully!",
                "OKGREEN",
            )
            self._print_post_install_instructions(
                "laravel", project_name, ["php artisan serve"]
            )

    def install_nextjs(self):
        Utils.print_colored("\n--- Install Next.js ---", "HEADER")
        if not Utils.check_dependency("npx", "npx"):
            return

        project_name = input("Enter project name: ").strip()
        if not project_name:
            return

        target_dir = self._ensure_category_dir("nextjs")
        cmd = [
            "npx",
            "create-next-app@latest",
            project_name,
            "--use-npm",
            "--yes",
            "--typescript",
            "--tailwind",
            "--eslint",
            "--app",
            "--src-dir",
            "--import-alias",
            "@/*",
        ]

        if Utils.run_command(cmd, cwd=target_dir):
            Utils.print_colored(
                f"\n[+] Next.js project '{project_name}' created successfully!",
                "OKGREEN",
            )
            self._print_post_install_instructions(
                "nextjs", project_name, ["npm run dev"]
            )

    def install_vue_vite(self):
        Utils.print_colored("\n--- Install Vue (via Vite) ---", "HEADER")
        if not Utils.check_dependency("npm", "Node.js/npm"):
            return

        project_name = input("Enter project name: ").strip()
        if not project_name:
            return

        target_dir = self._ensure_category_dir("vuejs")
        cmd = ["npm", "create", "vite@latest", project_name, "--", "--template", "vue"]

        if Utils.run_command(cmd, cwd=target_dir):
            Utils.print_colored(
                f"\n[+] Vue project '{project_name}' created successfully!", "OKGREEN"
            )
            self._print_post_install_instructions(
                "vuejs", project_name, ["npm install", "npm run dev"]
            )

    def install_svelte_vite(self):
        Utils.print_colored("\n--- Install Svelte (via Vite) ---", "HEADER")
        if not Utils.check_dependency("npm", "Node.js/npm"):
            return

        project_name = input("Enter project name: ").strip()
        if not project_name:
            return

        target_dir = self._ensure_category_dir("svelte")
        cmd = [
            "npm",
            "create",
            "vite@latest",
            project_name,
            "--",
            "--template",
            "svelte",
        ]

        if Utils.run_command(cmd, cwd=target_dir):
            Utils.print_colored(
                f"\n[+] Svelte project '{project_name}' created successfully!",
                "OKGREEN",
            )
            self._print_post_install_instructions(
                "svelte", project_name, ["npm install", "npm run dev"]
            )

    def install_nestjs(self):
        Utils.print_colored("\n--- Install NestJS ---", "HEADER")
        if not Utils.check_dependency("npx", "npx"):
            return

        project_name = input("Enter project name: ").strip()
        if not project_name:
            return

        target_dir = self._ensure_category_dir("nestjs")

        cmd = [
            "npx",
            "-y",
            "@nestjs/cli@latest",
            "new",
            project_name,
            "--package-manager",
            "npm",
        ]

        if Utils.run_command(cmd, cwd=target_dir):
            Utils.print_colored(
                f"\n[+] NestJS project '{project_name}' created successfully!",
                "OKGREEN",
            )
            self._print_post_install_instructions(
                "nestjs", project_name, ["npm run start:dev"]
            )

    def install_angular(self):
        Utils.print_colored("\n--- Install Angular ---", "HEADER")
        if not Utils.check_dependency("npx", "npx"):
            return

        project_name = input("Enter project name: ").strip()
        if not project_name:
            return

        target_dir = self._ensure_category_dir("angular")
        cmd = [
            "npx",
            "-y",
            "-p",
            "@angular/cli@latest",
            "ng",
            "new",
            project_name,
            "--skip-git",
            "--defaults",
        ]

        if Utils.run_command(cmd, cwd=target_dir):
            Utils.print_colored(
                f"\n[+] Angular project '{project_name}' created successfully!",
                "OKGREEN",
            )
            self._print_post_install_instructions(
                "angular", project_name, ["npm start"]
            )

    def install_express(self):
        Utils.print_colored("\n--- Install Express.js ---", "HEADER")
        if not Utils.check_dependency("npx", "npx"):
            return

        project_name = input("Enter project name: ").strip()
        if not project_name:
            return

        target_dir = self._ensure_category_dir("express")
        cmd = ["npx", "-y", "express-generator@latest", project_name, "--no-view"]

        if Utils.run_command(cmd, cwd=target_dir):
            Utils.print_colored(
                f"\n[+] Express project '{project_name}' created successfully!",
                "OKGREEN",
            )
            self._print_post_install_instructions(
                "express", project_name, ["npm install", "npm start"]
            )

    def _print_post_install_instructions(self, category, project_name, commands):
        Utils.print_colored("\nTo get started, run:", "BOLD")
        print(f"  cd projects/{category}/{project_name}")
        for cmd in commands:
            print(f"  {cmd}")
        print()
