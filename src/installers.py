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

            # Ask for cleanup
            clean_choice = (
                input(
                    "Do you want to clean up the default React boilerplate code? (y/n): "
                )
                .lower()
                .strip()
            )
            if clean_choice == "y":
                project_path = os.path.join(target_dir, project_name)
                self._clean_react_project(project_path)

                # Ask for React Router
                router_choice = (
                    input(
                        "Do you want to install and setup React Router (react-router-dom)? (y/n): "
                    )
                    .lower()
                    .strip()
                )
                if router_choice == "y":
                    self._setup_react_router(project_path)

                # Ask for Tailwind CSS
                tailwind_choice = (
                    input("Do you want to install and setup Tailwind CSS? (y/n): ")
                    .lower()
                    .strip()
                )
                if tailwind_choice == "y":
                    self._setup_tailwind(project_path)

            self._print_post_install_instructions(
                "reactjs", project_name, ["npm install", "npm run dev"]
            )

    def _clean_react_project(self, project_path):
        """Cleans up default artifacts from a Vite React project"""
        try:
            Utils.print_colored("\n[*] Cleaning up project files...", "WARNING")

            files_to_remove = [
                os.path.join(project_path, "src", "assets", "react.svg"),
                os.path.join(project_path, "public", "vite.svg"),
                os.path.join(project_path, "src", "App.css"),
            ]

            for file_path in files_to_remove:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Removed: {os.path.basename(file_path)}")

            app_jsx_path = os.path.join(project_path, "src", "App.jsx")
            minimal_app_jsx = """function App() {
  return (
    <div>
      <h1>React App</h1>
    </div>
  )
}

export default App
"""
            with open(app_jsx_path, "w") as f:
                f.write(minimal_app_jsx)
            print("Reset: App.jsx")

            index_css_path = os.path.join(project_path, "src", "index.css")
            if os.path.exists(index_css_path):
                with open(index_css_path, "w") as f:
                    f.write("")
                print("Cleared: index.css")

            Utils.print_colored("[+] Project cleanup complete!", "OKGREEN")

        except Exception as e:
            Utils.print_colored(f"[!] Error during cleanup: {e}", "FAIL")

    def _setup_react_router(self, project_path):
        """Sets up React Router with best practices"""
        try:
            Utils.print_colored(
                "\n[*] Installing react-router-dom (this may take a moment)...",
                "WARNING",
            )

            if not Utils.run_command(
                ["npm", "install", "react-router-dom"], cwd=project_path
            ):
                Utils.print_colored("[!] Failed to install react-router-dom", "FAIL")
                return

            Utils.print_colored(
                "[*] Setting up folder structure and files...", "WARNING"
            )

            os.makedirs(os.path.join(project_path, "src", "pages"), exist_ok=True)
            os.makedirs(os.path.join(project_path, "src", "components"), exist_ok=True)
            os.makedirs(os.path.join(project_path, "src", "routes"), exist_ok=True)

            with open(os.path.join(project_path, "src", "pages", "Home.jsx"), "w") as f:
                f.write(
                    """const Home = () => {
  return (
    <div style={{ padding: '20px', minHeight: '80vh' }}>
      <h1>Home Page</h1>
      <p>Welcome to your new React app with Routing!</p>
    </div>
  );
};
export default Home;"""
                )

            with open(
                os.path.join(project_path, "src", "pages", "About.jsx"), "w"
            ) as f:
                f.write(
                    """const About = () => {
  return (
    <div style={{ padding: '20px', minHeight: '80vh' }}>
      <h1>About Page</h1>
      <p>This is the clean About page.</p>
    </div>
  );
};
export default About;"""
                )

            with open(
                os.path.join(project_path, "src", "components", "Navbar.jsx"), "w"
            ) as f:
                f.write(
                    """import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav style={{ padding: '15px', borderBottom: '1px solid #eee', display: 'flex', gap: '20px', alignItems: 'center' }}>
      <h3 style={{ margin: 0 }}>My App</h3>
      <Link to="/" style={{ textDecoration: 'none', color: '#333' }}>Home</Link>
      <Link to="/about" style={{ textDecoration: 'none', color: '#333' }}>About</Link>
    </nav>
  );
};
export default Navbar;"""
                )

            with open(
                os.path.join(project_path, "src", "components", "Footer.jsx"), "w"
            ) as f:
                f.write(
                    """const Footer = () => {
  return (
    <footer style={{ padding: '20px', borderTop: '1px solid #eee', textAlign: 'center', marginTop: 'auto' }}>
      <p style={{ margin: 0, color: '#666' }}>&copy; {new Date().getFullYear()} My Application. All rights reserved.</p>
    </footer>
  );
};
export default Footer;"""
                )

            with open(
                os.path.join(project_path, "src", "pages", "NotFound.jsx"), "w"
            ) as f:
                f.write(
                    """import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div style={{ padding: '50px', textAlign: 'center', minHeight: '80vh' }}>
      <h1 style={{ fontSize: '3rem', margin: '0 0 20px 0', color: '#e74c3c' }}>404</h1>
      <h2 style={{ margin: '0 0 20px 0' }}>Page Not Found</h2>
      <p style={{ marginBottom: '30px', color: '#666' }}>The page you are looking for does not exist.</p>
      <Link to="/" style={{ 
        padding: '10px 20px', 
        backgroundColor: '#3498db', 
        color: 'white', 
        textDecoration: 'none', 
        borderRadius: '5px' 
      }}>Go back to Home</Link>
    </div>
  );
};
export default NotFound;"""
                )

            with open(
                os.path.join(project_path, "src", "routes", "AppRoutes.jsx"), "w"
            ) as f:
                f.write(
                    """import { createBrowserRouter } from 'react-router-dom';
import App from '../App';
import Home from '../pages/Home';
import About from '../pages/About';
import NotFound from '../pages/NotFound';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <NotFound />,
    children: [
      {
        path: '/',
        element: <Home />,
      },
      {
        path: '/about',
        element: <About />,
      },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  }
]);"""
                )

            with open(os.path.join(project_path, "src", "App.jsx"), "w") as f:
                f.write(
                    """import { Outlet } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <main style={{ flex: 1 }}>
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}

export default App;"""
                )

            with open(os.path.join(project_path, "src", "main.jsx"), "w") as f:
                f.write(
                    """import React from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import { router } from './routes/AppRoutes'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)"""
                )

            Utils.print_colored("[+] React Router setup complete!", "OKGREEN")

        except Exception as e:
            Utils.print_colored(f"[!] Error during router setup: {e}", "FAIL")

    def _setup_tailwind(self, project_path):
        """Installs and configures Tailwind CSS"""
        try:
            Utils.print_colored(
                "\n[*] Installing Tailwind CSS dependencies...", "WARNING"
            )

            cmd = ["npm", "install", "-D", "tailwindcss", "postcss", "autoprefixer"]
            if not Utils.run_command(cmd, cwd=project_path):
                Utils.print_colored("[!] Failed to install Tailwind CSS", "FAIL")
                return

            Utils.print_colored("[*] Configuring Tailwind CSS...", "WARNING")

            tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}"""
            with open(os.path.join(project_path, "tailwind.config.js"), "w") as f:
                f.write(tailwind_config)

            postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}"""
            with open(os.path.join(project_path, "postcss.config.js"), "w") as f:
                f.write(postcss_config)

            index_css_path = os.path.join(project_path, "src", "index.css")
            existing_content = ""
            if os.path.exists(index_css_path):
                with open(index_css_path, "r") as f:
                    existing_content = f.read()

            tailwind_directives = """@tailwind base;
@tailwind components;
@tailwind utilities;

"""
            with open(index_css_path, "w") as f:
                f.write(tailwind_directives + existing_content)

            Utils.print_colored("[+] Tailwind CSS setup complete!", "OKGREEN")

        except Exception as e:
            Utils.print_colored(f"[!] Error during Tailwind setup: {e}", "FAIL")

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
