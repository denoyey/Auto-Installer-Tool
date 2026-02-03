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
- **✨ React Superpowers**:
  - **"Clean Slate" Mode**: Option to automatically remove all default boilerplate (assets, minimal App.jsx, empty CSS) for a fresh start.
  - **Auto-Configured Routing**: One-click installation of `react-router-dom` with a pre-built, best-practice flat folder structure (`src/pages`, `src/components`, `src/routes`).
  - **Tailwind CSS Ready (Fixed & Optimized)**:
    - Automatically installs **Tailwind CSS v4-ready** configuration using `@tailwindcss/postcss` to prevent Vite plugin errors.
    - Sets **Poppins** as the default font family (via Google Fonts) automatically.
    - Generates all starter components (`Navbar`, `Footer`, `Home`, `NotFound`) using **Utility Classes** instead of inline styles.
  - **Animation Ready**: Option to install **Framer Motion** and automatically creates a reusable `PageTransition` component for smooth page transitions.

---

## 🔴 Laravel Superpowers (NEW!)

Laravel installation now comes with **optional add-ons** to supercharge your backend development:

### 🎨 Tailwind CSS via Vite

Get beautiful, utility-first styling out of the box!

| Feature | Description |
|---------|-------------|
| **One-Click Install** | Just answer "y" when prompted |
| **Vite Integration** | Uses `@tailwindcss/vite` plugin for blazing fast HMR |
| **Auto-Configuration** | `vite.config.js` and `app.css` are automatically configured |
| **Latest Version** | Always installs the newest Tailwind CSS |

**What gets configured:**
```javascript
// vite.config.js (auto-generated)
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.js'],
            refresh: true,
        }),
        tailwindcss(),
    ],
});
```

```css
/* resources/css/app.css (auto-generated) */
@import "tailwindcss";
```

### 🛡️ Filament Admin Panel

Build stunning admin dashboards in minutes with **Filament v3**!

| Feature | Description |
|---------|-------------|
| **Latest Version** | Automatically installs Filament v3.x |
| **Admin Panel Ready** | Pre-configured panel at `/admin` |
| **User Management** | Create admin users with one command |
| **Full Documentation** | Links provided after installation |

**After installation, you'll get:**
- 📍 Admin Panel URL: `http://localhost:8000/admin`
- 👤 Create admin user: `php artisan make:filament-user`
- 📚 Documentation: [filamentphp.com/docs](https://filamentphp.com/docs)

### 📋 Laravel Installation Flow

```
┌─────────────────────────────────────────────────────────┐
│  1. Create Laravel Project (via Composer)               │
├─────────────────────────────────────────────────────────┤
│  2. ⚡ AUTO: npm install (frontend dependencies)        │
├─────────────────────────────────────────────────────────┤
│  3. 🎨 "Install Tailwind CSS (via Vite)?" [y/n]         │
│     └─ If yes: install packages + configure vite        │
├─────────────────────────────────────────────────────────┤
│  4. 🛡️ "Install Filament Admin Panel?" [y/n]            │
│     └─ If yes: composer require + artisan install       │
├─────────────────────────────────────────────────────────┤
│  5. ✅ Done! Post-install commands displayed            │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠 Supported Frameworks

| Framework | Type | Installer / Method | Optional Add-ons |
| :--- | :--- | :--- | :--- |
| **⚛️ React.js** | Frontend | `Vite` | Cleanup, Router, Tailwind, Framer Motion |
| **🟢 Vue.js** | Frontend | `Vite` | - |
| **🔥 Svelte** | Frontend | `Vite` | - |
| **▲ Next.js** | Fullstack | `create-next-app` | TypeScript, Tailwind, ESLint (auto) |
| **🅰️ Angular** | Frontend | `@angular/cli` | - |
| **🦁 NestJS** | Backend | `@nestjs/cli` | - |
| **🚂 Express.js** | Backend | `express-generator` | - |
| **🔴 Laravel** | Backend | `Composer` | **Tailwind CSS, Filament Admin** |

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- **[Python 3.x](https://www.python.org/downloads/)**
- **[Node.js & npm](https://nodejs.org/)** (Required for JS/TS frameworks & Tailwind in Laravel)
- **[PHP](https://www.php.net/downloads)** (Required for Laravel)

### Installation & Usage

1.  **Clone or Download** this repository.
    ```bash
    git clone https://github.com/denoyey/Auto-Installer-Tool.git
    cd Auto-Installer-Tool
    ```
2.  Run the tool:
    ```bash
    python main.py
    ```
3.  **Select** your desired framework from the beautiful CLI menu.
4.  **Enter** your project name.
5.  **Answer prompts** for optional add-ons (if available).
6.  **Done!** Your project is ready in the `projects/` directory.

---

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
│   ├── 📂 laravel/      # With optional Tailwind + Filament!
│   ├── 📂 nextjs/
│   └── ...
├── main.py              # Entry point script
└── README.md            # You are reading this!
```

---

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

### Laravel with Add-ons Example:

```text
--- Install Laravel ---
Enter project name: my-admin-app
[+] Laravel project 'my-admin-app' created successfully!

[*] Running npm install (Laravel frontend dependencies)...
added 1 package, and audited 2 packages in 3s

Do you want to install Tailwind CSS (via Vite)? (y/n): y
[*] Installing Tailwind CSS via Vite...
[+] Tailwind CSS (via Vite) installed successfully!

📋 Tailwind CSS Setup Info:
  • Run: npm run dev (development)
  • Run: npm run build (production)
  • Documentation: https://tailwindcss.com/docs

Do you want to install Filament Admin Panel (latest version)? (y/n): y
[*] Installing Filament Admin Panel (this may take a moment)...
[*] Installing Filament panels...
[+] Filament Admin Panel installed successfully!

📋 Filament Setup Info:
  • Admin Panel URL: http://localhost:8000/admin
  • Create admin user: php artisan make:filament-user
  • Documentation: https://filamentphp.com/docs

To get started, run:
  cd projects/laravel/my-admin-app
  php artisan migrate
  php artisan make:filament-user
  php artisan serve
```

---

## 📦 What's New

### v1.1.0 (Latest)
- ✨ **Laravel Tailwind CSS Integration** - Install Tailwind CSS via Vite with one prompt
- ✨ **Laravel Filament Admin Panel** - Build admin dashboards instantly
- 🔧 Improved post-install instructions based on selected add-ons
- 📚 Updated documentation with detailed feature explanations

### v1.0.0
- 🚀 Initial release with 8 framework installers
- ⚛️ React.js with cleanup, routing, Tailwind, and Framer Motion options
- 🔴 Laravel with auto Composer download

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/denoyey">denoyey</a>
</p>

<p align="center">
  <b>⭐ Star this repo if you find it useful! ⭐</b>
</p>
