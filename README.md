# 🧪 Dhara Netra 1.0 – Soil Classification Tool

> **Dhara Netra 1.0** is an advanced, open-source, GUI-based Soil Classification Tool following **IS 1498:1970**. Effortlessly analyze, visualize, classify, and report fine and coarse-grained soils — all in one modern Python app.

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/License-Free%20%26%20Open--Source-brightgreen" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20MacOS-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/GUI-tkinter%20%7C%20matplotlib-blueviolet" alt="GUI">
  <img src="https://img.shields.io/badge/Status-Active-important" alt="Status">
  <img src="https://img.shields.io/badge/PRs-Welcome-blue" alt="PRs">
  <img src="https://img.shields.io/badge/Issues-Report%20Here-orange" alt="Issues">
</p>

---

## 📚 Table of Contents
- [Introduction](#-introduction)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Advanced Usage](#-advanced-usage)
- [Screenshots](#-screenshots)
- [FAQ](#-faq)
- [Support](#-support)
- [Data Privacy & Offline Use](#-data-privacy--offline-use)
- [Changelog](#-changelog)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)
- [Community & Feedback](#-community--feedback)

---

## 🌍 Introduction

**Dhara Netra 1.0** empowers civil engineers, students, and researchers to classify soils with precision and ease. Built for modern workflows, it supports batch processing, interactive charts, and rich reporting — all with a beautiful, customizable interface.

---

## 🚀 Features

- 🏷️ **IS 1498:1970-compliant soil classification**
- 🧪 Fine & coarse-grained soil support
- 📊 Interactive grain size & plasticity charts
- 🧠 Auto-computed indices: LL, PL, PI, CI, LI, SI, Activity
- 📈 Statistical & correlation analysis
- 📁 Import/export: JSON, PDF, TXT, CSV
- 🗂 Project database for field data management
- 🛠 Batch processing & trend analysis
- 🧾 PDF reporting (ReportLab-based)
- 🎨 Multiple color themes (default, dark, earth, blue) & **custom theme editor**
- 🖼️ **3D visualization** of soil properties
- 🔄 **Export/import** of settings, results, and plots (PNG, PDF, SVG)
- 🏛️ Integrated soil guide & IS code reference
- 🧑‍💻 **Logging** and session management
- ⚙️ **Preferences** and persistent user settings
- 📺 **Video tutorials** and in-app user guide
- 🔒 **No internet required** — works fully offline
- 🐍 Built with: `tkinter`, `matplotlib`, `numpy`, `reportlab`, `Pillow`, `streamlit`

---

## 🏗️ Tech Stack
- **Python 3.11+**
- **tkinter** (GUI)
- **matplotlib** (plots, 3D visualization)
- **numpy** (calculations)
- **reportlab** (PDF export)
- **Pillow** (image handling)
- **streamlit** (optional web features)
- **sqlite3** (project database)

---

## 📦 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/dhara-netra-soil-classification.git
   cd dhara-netra-soil-classification
   ```
2. **Install dependencies:**
   ```bash
   pip install matplotlib numpy reportlab streamlit Pillow
   ```
   Or, using the provided requirements file:
   ```bash
   pip install -r Dhara\ Netra\ 1.O/requirements.txt
   ```
3. **Run the application:**
   ```bash
   python "Dhara Netra 1.O/Dhara Netra 1.O.py"
   ```

---

## ⚡ Quick Start

- Launch the app and follow the intuitive GUI to:
  - Input soil data (fine/coarse-grained)
  - Visualize grain size distribution and Atterberg limits
  - Classify soils per IS 1498:1970
  - Export results and reports (PDF, CSV, JSON, TXT)
  - Explore project database, batch tools, and more

---

## 🧑‍🔬 Advanced Usage

- **Batch Processing:** Import multiple CSV/Excel files for automated analysis and reporting.
- **Trend Analysis:** Visualize changes in soil properties over time.
- **3D Visualization:** Explore soil data in three dimensions (requires at least 3 samples).
- **Custom Themes:** Create, save, and apply your own color themes for the GUI.
- **Export/Import:** Save and load settings, results, and plots in various formats.
- **Project Database:** Manage multiple soil projects and sessions with persistent storage.
- **Logging:** All actions and errors are logged for troubleshooting (`soil_classification.log`).
- **Preferences:** Autosave, default formats, and font size are customizable (`preferences.json`).
- **Video Tutorials:** Access in-app video guides for both basic and advanced features.

---

## 📸 Screenshots

> _Add screenshots of the main interface, charts, 3D plots, and reports here for maximum appeal._

---

## ❓ FAQ

**Q: Is Dhara Netra 1.0 free and open-source?**  
A: Yes! Use, modify, and share it without restriction.

**Q: Does it work offline?**  
A: 100% offline. No data leaves your device.

**Q: Can I import/export my data?**  
A: Yes, supports CSV, JSON, PDF, TXT, and more.

**Q: How do I customize the look?**  
A: Use the built-in theme editor or create your own themes.

**Q: Where is my data stored?**  
A: Locally, in project/session files and a SQLite database.

**Q: How do I get help?**  
A: See the in-app user guide, video tutorials, or open an issue.

---

## 🆘 Support
- [Open an Issue](https://github.com/SuneeLAbbireddY/Dhara-Netra-1.O/issues)
- [Submit a Pull Request](https://github.com/SuneeLAbbireddY/Dhara-Netra-1.O/pulls)
- Email: suneelabbireddy2031@gmail.com

---

## 🔒 Data Privacy & Offline Use
- All data is processed and stored **locally**.
- No internet connection is required for any feature.
- No telemetry, tracking, or ads.

---

## 🚧 Roadmap
- [ ] Web-based interface (Streamlit)
- [ ] More export formats (Excel, images)
- [ ] Cloud sync (optional, privacy-first)
- [ ] Plugin/extension system
- [ ] More advanced statistical tools
- [ ] Community-contributed themes

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork, submit pull requests, or open issues for bugs, features, or enhancements.

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🪪 License

This project is **open-source and license-free**. You are free to use, modify, and distribute it for any purpose, without restriction. Attribution is appreciated but not required.

---

## 🙏 Acknowledgements

- IS 1498:1970 – Indian Standard for Soil Classification
- Python, tkinter, matplotlib, numpy, reportlab, Pillow, streamlit
- All contributors and the open-source community

---

## 🌐 Community & Feedback
- Star ⭐ this repo to support the project
- Join the discussion in [Issues](https://github.com/SuneeLAbbireddY/Dhara-Netra-1.O/issues)
- Suggest features or report bugs
- Share your use cases and screenshots!

<p align="center">
  <b>Made with ❤️ for the civil engineering community.</b>
</p>
