# Rocky Desktop Pet

A desktop pet featuring Rocky from **Project Hail Mary** — a pixel-art alien companion that roams your screen, asks questions, accepts gifts, and gives motivational quotes in Rocky-speak.

> "Good good good! You are best human! I know many human. Just you. But you are best!"

## Features

- **Desktop roaming** — Rocky walks around your screen as a transparent overlay, bouncing off edges
- **Questions** — Movie trivia, personal check-ins, and fun prompts — drag your answer to Rocky
- **Gift giving** — Drag items like Astrophage, Xenonite, and a Friendship Badge to Rocky
- **Rocky reactions** — Happy, sad, curious, and excited animations with synthesized musical chords
- **Motivational quotes** — 22 quotes written in Rocky's broken-English style
- **System tray** — Show/Hide, customizable hotkey, volume control, and quit
- **Intro sequence** — Rocky introduces himself on first launch

## Quick Start

### From source

```bash
git clone https://github.com/AnujCtrl/rocky-pet.git
cd rocky-pet
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .
python -m rocky_pet.main
```

### Windows executable

Download `RockyPet.exe` from [Releases](https://github.com/AnujCtrl/rocky-pet/releases) and double-click to run.

## How It Works

Rocky appears on your screen as a small pixel-art character. He roams freely — you can click through the transparent areas to interact with your desktop normally.

- **Click Rocky** to trigger a question or gift panel
- **Drag items** from the panel to Rocky to interact
- **Wait** and Rocky will occasionally ask you things or share quotes on his own
- **Right-click the tray icon** to access settings or quit

## Tech Stack

- Python + PyQt6 (transparent frameless windows, drag-and-drop)
- numpy (musical chord synthesis)
- PyInstaller (single-file .exe packaging)

## Building the Windows .exe

```bash
pip install pyinstaller
pyinstaller rocky.spec --clean
# Output: dist/RockyPet.exe
```

## License

MIT
