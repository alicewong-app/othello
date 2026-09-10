# Othello (Reversi) Flask App

A web-based implementation of the classic board game **Othello (Reversi)** built using Python and the Flask framework. Players can take turns making moves on a dynamic board following standard game rules.

---

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3, JavaScript
* **Environment Management:** Python Virtual Environment (`.venv`)

---

## 🚀 Getting Started

Follow these steps to run the application locally on your machine.

### Prerequisites
Make sure you have **Python 3.x** installed on your system.

### Installation & Setup

1. **Clone the repository** (if downloading on another machine):
   ```bash
   git clone https://github.com
   cd othello
   ```

2. **Create and activate a virtual environment**:
   * **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   * **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application**:
   ```bash
   python app.py
   ```
   *(Note: Change `app.py` to `main.py` or your specific entry point filename if it differs).*

5. **Open your browser** and navigate to:
   ```text
   http://127.0.0.1:5000
   ```

---

## 🎮 Game Rules & Features
* **Standard Othello Logic:** Valid moves, piece flipping, and score tracking.
* **Turn Indicator:** Clearly displays whether it is Black's or White's turn.
* **Game Over Detection:** Automatically determines the winner when the board is full or no valid moves remain.
