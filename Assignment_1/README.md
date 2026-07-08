<div align="center">

# Identity Echo Interface

### A polished Streamlit transmission portal built for the MIRAI Internship Programme

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PEP-8](https://img.shields.io/badge/Code%20Style-PEP--8-green?style=for-the-badge)](https://peps.python.org/pep-0008/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

</div>

---

## Description

**Identity Echo Interface** is a modern, minimal web application built with **Python** and **Streamlit**. It collects a user's name and message, validates the inputs with clear error feedback, and echoes a personalised transmission response — complete with token analytics and an animated success celebration.

Designed as an internship assignment project, it demonstrates clean code organisation, beginner-friendly Python practices, and a polished Streamlit UI.

---

## Features

| Feature | Details |
|---|---|
| **Transmission Console** | Dual `st.text_input()` fields for Name and Message |
| **Input Validation** | Sequential `if / elif / else` guards with contextual feedback |
| **Success Response** | F-string personalised success message via `st.success()` |
| **Token Analytics** | Character count & estimated token consumption |
| **Metric Cards** | `st.metric()` display for Character Count and Estimated Tokens |
| **Balloons** | Animated celebration on successful transmission |
| **Sidebar** | Project info, objective, tech stack, and author section |
| **Custom Styling** | Gradient button, metric card accents via injected CSS |
| **PEP-8 Compliant** | Clean, commented, modular code |

---

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Core programming language |
| Streamlit | 1.35+ | Web UI framework |
| PEP-8 | — | Code style standard |

> **No external UI libraries.** Only Streamlit is used — keeping dependencies minimal.

---

## Project Structure

```
Identity-Echo-Interface/
│
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
├── README.md           ← Project documentation (this file)
├── .gitignore          ← Files excluded from version control
│
└── assets/
    └── preview.png     ← Application screenshot (add after first run)
```

---

## Installation & Setup

### 1 · Clone the Repository

```bash
git clone https://github.com/<your-username>/identity-echo-interface.git
cd identity-echo-interface
```

### 2 · Create a Virtual Environment

It is strongly recommended to use a virtual environment to isolate project dependencies.

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prepended to your terminal prompt.

### 3 · Install Requirements

```bash
pip install -r requirements.txt
```

### 4 · Run the Application

```bash
streamlit run app.py
```

Streamlit will automatically open the app at **http://localhost:8501** in your default browser.

---

## Learning Outcomes

Working through this project develops the following skills:

- ✅ Initialising and configuring a **Streamlit** application
- ✅ Using `st.title()`, `st.write()`, `st.text_input()`, `st.button()` correctly
- ✅ Implementing **input validation** with `if / elif / else` logic
- ✅ Displaying conditional feedback with `st.success()`, `st.error()`, `st.warning()`
- ✅ Using **f-strings** for dynamic, personalised output
- ✅ Computing **character counts** with `len()` and estimating **token counts**
- ✅ Presenting analytics with `st.metric()` and `st.info()`
- ✅ Organising code into **modular functions** following **PEP-8**
- ✅ Enhancing UX with `st.set_page_config()`, sidebar, dividers, and balloons

---

## Assignment Objectives Covered

| # | Requirement | Status |
|---|---|---|
| 1 | Initialise a Streamlit application | ✅ Done |
| 2 | `st.title()` for application title | ✅ Done |
| 3 | `st.write()` to explain the application | ✅ Done |
| 4 | Two `st.text_input()` fields (Name & Message) | ✅ Done |
| 5 | Single **Transmit** button | ✅ Done |
| 6 | Processing logic runs only after button click | ✅ Done |
| 7 | `if / elif / else` validation with correct messages | ✅ Done |

---

## Advanced Challenge

| Item | Implementation |
|---|---|
| Character count | `len(clean_message)` |
| Token estimation | `round(len(clean_message) / 4, 2)` |
| Display | `st.info()` with 2-decimal-place token count |
| Metric cards | `st.metric()` for Character Count & Estimated Tokens |

---

## Professional Improvements Included

- `st.set_page_config()` with page icon 🛰️ and centered layout  
- Sidebar with Project Info, Objective, Tech Stack, and Author sections   
- Dividers between logical sections   
- Placeholder text inside `text_input()` fields  
- `strip()` applied before all validation  
- Clean comments and proper variable naming  
- Modular code: `apply_custom_styles()`, `main()`   

---

## Future Improvements

- [ ] Add a **message history log** using `st.session_state`
- [ ] Support **multi-line messages** with a toggle between `st.text_input` / `st.text_area`
- [ ] Export transmission log as a **CSV download**
- [ ] Add a **character limit** with a live progress bar
- [ ] Deploy to **Streamlit Community Cloud** for public access
- [ ] Add **dark / light theme toggle**
- [ ] Internationalise with multi-language support

---

## Author

| Field | Value |
|---|---|
| **Name** | *(Hemendra Sharma)* |
| **Programme** | MIRAI Internship |
| **Assignment** | 1 — Identity Echo Interface |
| **Year** | 2026 |

---

## License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute it for educational purposes.

---

<div align="center">

Made with ❤️ and 🐍 · MIRAI Internship Programme · 2026

</div>
