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

                router_choice = (
                    input(
                        "Do you want to install and setup React Router (react-router-dom)? (y/n): "
                    )
                    .lower()
                    .strip()
                )
                if router_choice == "y":
                    self._setup_react_router(project_path)

                tailwind_choice = (
                    input("Do you want to install and setup Tailwind CSS? (y/n): ")
                    .lower()
                    .strip()
                )
                if tailwind_choice == "y":
                    self._setup_tailwind(project_path)

                framer_choice = (
                    input("Do you want to install and setup Framer Motion? (y/n): ")
                    .lower()
                    .strip()
                )
                if framer_choice == "y":
                    self._setup_framer_motion(project_path)

            self._print_post_install_instructions(
                "reactjs", project_name, ["npm install", "npm run dev"]
            )

    def _clean_react_project(self, project_path):
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
                    f.write(
                        "@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');\n\nbody {\n  font-family: 'Poppins', sans-serif;\n  margin: 0;\n  padding: 0;\n  box-sizing: border-box;\n}\n"
                    )
                print("Configured: index.css (with Poppins)")

            Utils.print_colored("[+] Project cleanup complete!", "OKGREEN")

        except Exception as e:
            Utils.print_colored(f"[!] Error during cleanup: {e}", "FAIL")

    def _setup_react_router(self, project_path):
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
    <div className="p-5 min-h-[80vh]">
      <h1 className="text-3xl font-bold mb-4">Home Page</h1>
      <p className="text-gray-600">Welcome to your new React app with Routing!</p>
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
    <div className="p-5 min-h-[80vh]">
      <h1 className="text-3xl font-bold mb-4">About Page</h1>
      <p className="text-gray-600">This is the clean About page.</p>
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
    <nav className="flex items-center gap-6 p-4 border-b border-gray-100">
      <h3 className="text-xl font-bold m-0">My App</h3>
      <Link to="/" className="text-gray-800 hover:text-blue-500 no-underline transition-colors">Home</Link>
      <Link to="/about" className="text-gray-800 hover:text-blue-500 no-underline transition-colors">About</Link>
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
    <footer className="p-5 border-t border-gray-100 text-center mt-auto">
      <p className="m-0 text-gray-500">&copy; {new Date().getFullYear()} My Application. All rights reserved.</p>
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
    <div className="p-12 text-center min-h-[80vh] flex flex-col items-center justify-center">
      <h1 className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-orange-500 m-0 mb-4">404</h1>
      <h2 className="text-2xl font-semibold mb-4 text-gray-800">Page Not Found</h2>
      <p className="mb-8 text-gray-500">The page you are looking for does not exist.</p>
      <Link to="/" className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors no-underline">
        Go back to Home
      </Link>
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
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-1">
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
        try:
            Utils.print_colored(
                "\n[*] Installing Tailwind CSS dependencies (PostCSS approach)...",
                "WARNING",
            )

            cmd = [
                "npm",
                "install",
                "-D",
                "tailwindcss",
                "@tailwindcss/postcss",
                "postcss",
                "autoprefixer",
            ]
            if not Utils.run_command(cmd, cwd=project_path):
                Utils.print_colored("[!] Failed to install Tailwind CSS", "FAIL")
                return

            Utils.print_colored(
                "[*] Configuring Tailwind CSS with PostCSS...", "WARNING"
            )

            tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
}"""
            with open(os.path.join(project_path, "tailwind.config.js"), "w") as f:
                f.write(tailwind_config)

            postcss_config = """export default {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
}"""
            with open(os.path.join(project_path, "postcss.config.js"), "w") as f:
                f.write(postcss_config)

            index_css_path = os.path.join(project_path, "src", "index.css")

            # Best practice: Import font first, then directives, then base layer assignment
            css_content = """@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    font-family: 'Poppins', sans-serif;
    scroll-behavior: smooth;
  }
}
"""
            with open(index_css_path, "w") as f:
                f.write(css_content)

            Utils.print_colored("[+] Tailwind CSS setup complete!", "OKGREEN")

        except Exception as e:
            Utils.print_colored(f"[!] Error during Tailwind setup: {e}", "FAIL")

        except Exception as e:
            Utils.print_colored(f"[!] Error during Tailwind setup: {e}", "FAIL")

    def _setup_framer_motion(self, project_path):
        try:
            Utils.print_colored("\n[*] Installing Framer Motion...", "WARNING")

            if not Utils.run_command(
                ["npm", "install", "framer-motion"], cwd=project_path
            ):
                Utils.print_colored("[!] Failed to install Framer Motion", "FAIL")
                return

            Utils.print_colored(
                "[*] Setting up Framer Motion best practices...", "WARNING"
            )

            os.makedirs(os.path.join(project_path, "src", "components"), exist_ok=True)

            # Create a reusable PageTransition component (Best Practice)
            transition_component = """import { motion } from 'framer-motion';

const PageTransition = ({ children }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
};

export default PageTransition;"""

            with open(
                os.path.join(project_path, "src", "components", "PageTransition.jsx"),
                "w",
            ) as f:
                f.write(transition_component)

            Utils.print_colored(
                "[+] Framer Motion setup complete! (Added PageTransition.jsx)",
                "OKGREEN",
            )

        except Exception as e:
            Utils.print_colored(f"[!] Error during Framer Motion setup: {e}", "FAIL")

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
