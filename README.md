# Rock Paper Scissors Hand Gesture Detection

This project implements a **Rock Paper Scissors** game using Python, OpenCV, and MediaPipe. It allows a user to play the game against the computer by showing hand gestures that are recognized in real time.

---

## Features

- **Hand Gesture Detection**: Uses MediaPipe to detect hand gestures and classify them as `rock`, `paper`, or `scissors`.
- **Real-Time Gameplay**: Processes webcam input to detect gestures and compare them against a random choice by the computer.
- **Scoring System**: Tracks user and computer scores during the game.
- **Interactive Interface**:
  - Countdown before detecting gestures.
  - Display results after each round.
  - Option to reset the game.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/RonMordo/rock_paper_scissors_visual_app.git
   ```
2. **Chane directory to the cloned repository**:
   ```bash
   cd rock_paper_scissors_visual_app
   ```
3. **Create the virtual environment using the setup script**:
   ```bash
   ./setup_env.sh
   ```

   ---

   ## Usage

   **Make sure your activating the virtual environment in every new terminal session**:
   ```bash
   source venv/bin/activate
   ```
   **Run the app**:
   ```bash
   python3 rock_paper_scissors_app.py
   ```
   **How to play**:  
   Press S to start the countdown or Q to quit.  
   You have 3 seconds to decide Paper, Rock or Scissors, the final gesture will be taken as your choice.  
   In the result screen you can press R to play again or Q to quit.
