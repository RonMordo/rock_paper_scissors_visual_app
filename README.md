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

![Hand landmarks image](assets/hand-landmarks.png)

---

## Logic

To determine whether the user has chosen Rock, Paper, or Scissors, we analyze the hand landmarks represented as x, y coordinates, as shown in the image above. Each choice is identified by interpreting whether a finger is flexed or stretched based on the positions of its joints.

### Identifying Flexed or Stretched Fingers

We use Euclidean distance to measure the geometry of each finger. Here’s the process:

1. **Measure Total Finger Length**:  
   - Calculate the distances between the fingertip, the two middle joints, and the base of the finger.  
   - Sum these distances to find the total finger length.

2. **Measure Tip-to-Base Distance**:  
   - Compute the straight-line distance from the fingertip to the base of the finger.

3. **Determine Flexion or Extension**:  
   - Divide the tip-to-base distance by the total finger length to get a ratio.  
   - If this ratio is equal to or greater than **0.9**, the finger is considered stretched (nearly straight). Otherwise, it is flexed.

### Applying Rock-Paper-Scissors Logic

Based on the flexion or extension of specific fingers, the user’s hand gesture is classified as Rock, Paper, or Scissors:

- **Rock**: All fingers are flexed.
- **Paper**: All fingers are stretched.
- **Scissors**: Only the index and middle fingers are stretched, while the rest are flexed.

Using this logic, we can determine the user’s choice and evaluate the winner of the Rock-Paper-Scissors game.

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
