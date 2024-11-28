import cv2
import numpy as np
import mediapipe as mp
import random
import time
import math

# Initialize Mediapipe Hand Landmarker
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
mp_draw = mp.solutions.drawing_utils

# Define gestures and scores
gestures = {0: 'rock', 1: 'paper', 2: 'scissors'}
user_score = 0
computer_score = 0

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two Mediapipe landmarks."""
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def is_finger_extended(landmarks, mcp_idx, pip_idx, dip_idx, tip_idx):
    """
    Determine if a finger is extended based on its landmarks.
    Args:
        landmarks: List of landmarks for the hand.
        mcp_idx: Index of the MCP joint.
        pip_idx: Index of the PIP joint.
        dip_idx: Index of the DIP joint.
        tip_idx: Index of the fingertip.

    Returns:
        True if the finger is extended, False otherwise.
    """
    # Calculate distances between adjacent landmarks
    mcp_to_pip = calculate_distance(landmarks[mcp_idx], landmarks[pip_idx])
    pip_to_dip = calculate_distance(landmarks[pip_idx], landmarks[dip_idx])
    dip_to_tip = calculate_distance(landmarks[dip_idx], landmarks[tip_idx])

    # Total length of the finger (sum of segments)
    total_length = mcp_to_pip + pip_to_dip + dip_to_tip

    # Direct distance from MCP to TIP
    mcp_to_tip = calculate_distance(landmarks[mcp_idx], landmarks[tip_idx])

    # Compare MCP-to-TIP distance with total length
    ratio = mcp_to_tip / total_length

    # Threshold for determining if the finger is extended
    return ratio > 0.9  # Adjust this threshold if needed

def classify_gesture(landmarks):
    """
    Classify the hand gesture based on the state of the fingers.
    Returns 'rock', 'paper', or 'scissors'.
    """
    # Indices for finger landmarks
    finger_indices = {
        "index": [5, 6, 7, 8],  # MCP, PIP, DIP, TIP for the index finger
        "middle": [9, 10, 11, 12],  # MCP, PIP, DIP, TIP for the middle finger
        "ring": [13, 14, 15, 16],  # MCP, PIP, DIP, TIP for the ring finger
        "pinky": [17, 18, 19, 20]  # MCP, PIP, DIP, TIP for the pinky finger
    }

    # Check the state of each finger
    extended_fingers = []
    for finger, (mcp, pip, dip, tip) in finger_indices.items():
        extended_fingers.append(is_finger_extended(landmarks, mcp, pip, dip, tip))

    # Logic for determining gestures
    if not any(extended_fingers):  # All fingers curled
        return 'rock'
    elif all(extended_fingers):  # All fingers extended
        return 'paper'
    elif extended_fingers[0] and extended_fingers[1] and not extended_fingers[2] or extended_fingers[3]:
        return 'scissors'  # Index and middle fingers extended
    else:
        return None  # Gesture not recognized

# Function to determine the winner
def determine_winner(user_gesture, computer_gesture):
    if user_gesture == computer_gesture:
        return "It's a draw!"
    elif (user_gesture == 'rock' and computer_gesture == 'scissors') or \
         (user_gesture == 'scissors' and computer_gesture == 'paper') or \
         (user_gesture == 'paper' and computer_gesture == 'rock'):
        return "User wins!"
    else:
        return "Computer wins!"

# Initialize OpenCV webcam input
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

countdown_active = False
countdown_start_time = None
result_screen_active = False
user_gesture = None
computer_gesture = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Flip frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert BGR frame to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with Mediapipe
    results = hands.process(rgb_frame)

    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            # Classify gesture during the countdown
            if countdown_active:
                user_gesture = classify_gesture(hand_landmarks.landmark)

    # Display the menu
    if not countdown_active and not result_screen_active:
        cv2.putText(frame, "Press 's' to start, 'q' to quit", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Handle countdown overlay
    if countdown_active:
        elapsed_time = time.time() - countdown_start_time
        countdown_value = 3 - int(elapsed_time)  # Countdown from 3 to 0
        if countdown_value >= 0:
            cv2.putText(frame, f"Get Ready: {countdown_value}", (200, 250),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        else:
            # Stop countdown
            countdown_active = False

            # Computer's random choice
            computer_gesture = random.choice(['rock', 'paper', 'scissors'])

            # Determine winner
            result = determine_winner(user_gesture, computer_gesture)
            if "User wins" in result:
                user_score += 1
            elif "Computer wins" in result:
                computer_score += 1

            # Prepare result screen
            result_screen = np.ones((600, 800, 3), dtype=np.uint8) * 255  # White background
            cv2.putText(result_screen, f"User: {user_gesture}", (50, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
            cv2.putText(result_screen, f"Computer: {computer_gesture}", (50, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
            cv2.putText(result_screen, result, (50, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
            cv2.putText(result_screen, f"User Score: {user_score}  Computer Score: {computer_score}", (50, 500),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
            cv2.putText(result_screen, "Press 'r' to return, 'q' to quit", (50, 550),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            result_screen_active = True

    # Show result screen if active
    if result_screen_active:
        cv2.imshow("Result", result_screen)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):  # Return to stream
            result_screen_active = False
            cv2.destroyWindow("Result")
        elif key == ord('q'):  # Quit
            break
        continue

    # Show the webcam feed
    cv2.imshow("Rock Paper Scissors", frame)

    # Handle key presses for menu
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') and not countdown_active:  # Start countdown
        countdown_active = True
        countdown_start_time = time.time()
        user_gesture = None
        computer_gesture = None
    elif key == ord('q'):  # Quit application
        break

# Release webcam and destroy OpenCV windows
cap.release()
cv2.destroyAllWindows()