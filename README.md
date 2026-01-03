# 🚀 Ultimate Web Stack Auto-Installer

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A powerful, automated **CLI tool** built with Python to effortlessly bootstrap your favorite web projects. Say goodbye to repetitive setup commands and hello to instant coding!

---

## ✨ Features

- **⚡ Blazing Fast Setup**: Uses modern build tools like **Vite** for frontend frameworks.
- **📂 Smart Organization**: Automatically creates and organizes projects into categorized subfolders (e.g., `projects/reactjs`, `projects/laravel`).
- **🧠 Intelligent Dependency Management**: 
  - Checks for `npm`, `npx`, and `php` before running.
  - **Auto-fetches Composer**: If you don't have Composer installed globally, the tool automatically downloads `composer.phar` locally to install Laravel without hassle.
- **🤖 Zero-Friction**:
  - Bypasses interactive prompts for **Next.js**, **Angular**, and **NestJS** (pre-configured with best practices like TypeScript, Tailwind, etc.).
  - Handles common errors (like PHP extension checks) automatically.
- **💎 Always Updated**: Forces the installation of the **@latest** versions for all frameworks.

## 🛠 Supported Frameworks

| Framework | Type | Installer / Method |
| :--- | :--- | :--- |
| **⚛️ React.js** | Frontend | `Vite` |
| **🟢 Vue.js** | Frontend | `Vite` |
| **🔥 Svelte** | Frontend | `Vite` |
| **▲ Next.js** | Fullstack | `create-next-app` (TypeScript, Tailwind, ESLint auto-configured) |
| **🅰️ Angular** | Frontend | `@angular/cli` |
| **🦁 NestJS** | Backend | `@nestjs/cli` |
| **🚂 Express.js** | Backend | `express-generator` |
| **🔴 Laravel** | Backend | `Composer` (Local or Global) |

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- **[Python 3.x](https://www.python.org/downloads/)**
- **[Node.js & npm](https://nodejs.org/)** (Required for JS/TS frameworks)
- **[PHP](https://www.php.net/downloads)** (Required for Laravel)

### Installation & Usage

1.  **Clone or Download** this repository.
2.  Open your terminal/command prompt in the project folder.
3.  Run the tool:
    ```bash
    python main.py
    ```
4.  **Select** your desired framework from the beautiful CLI menu.
5.  **Enter** your project name.
6.  **Done!** Your project is ready in the `projects/` directory.

## 📂 Project Structure

The tool keeps your workspace clean:

```text
├── 📂 bin/              # Stores local tools (e.g., composer.phar)
├── 📂 src/              # Source code modules
│   ├── installers.py    # Logic for installing each framework
│   ├── menu.py          # Interactive CLI UI
│   └── utils.py         # Helper functions (colors, system checks)
├── 📂 projects/         # YOUR GENERATED PROJECTS GO HERE
│   ├── 📂 reactjs/
│   ├── 📂 laravel/
│   ├── 📂 nextjs/
│   └── ...
├── main.py              # Entry point script
└── README.md            # You are reading this!
```

## 🖼 Preview

```text
   ___         __           ___          __        
  / _ | __ _  / /__  ___   / _ \ ___  _ / /_       
 / __ |/  ' \/ __/ \/ _ \ / // // _ \/ // __/       
/_/ |_/_/_/_/\__/ \___//____/ \___/\__\__/       
                                                 
      --- AUTO INSTALLER TOOL ---
        
 Select an option:
 [1] Install React.js (Vite)
 [2] Install Laravel
 ...
```

---

<p align="center">
  Made with ❤️ for denoyey.
</p>
