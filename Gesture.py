import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Set up the screen dimensions
screen_width, screen_height = pyautogui.size()

# Video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe Hand module
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Normalize coordinates
            thumb_x, thumb_y = int(thumb_tip.x * screen_width), int(thumb_tip.y * screen_height)
            index_x, index_y = int(index_finger_tip.x * screen_width), int(index_finger_tip.y * screen_height)
            middle_x, middle_y = int(middle_finger_tip.x * screen_width), int(middle_finger_tip.y * screen_height)
            ring_x, ring_y = int(ring_finger_tip.x * screen_width), int(ring_finger_tip.y * screen_height)
            pinky_x, pinky_y = int(pinky_tip.x * screen_width), int(pinky_tip.y * screen_height)

            # Check for gestures
            distance_thumb_index = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5
            distance_thumb_middle = ((thumb_tip.x - middle_finger_tip.x) ** 2 + (thumb_tip.y - middle_finger_tip.y) ** 2) ** 0.5
            distance_thumb_ring = ((thumb_tip.x - ring_finger_tip.x) ** 2 + (thumb_tip.y - ring_finger_tip.y) ** 2) ** 0.5
            distance_thumb_pinky = ((thumb_tip.x - pinky_tip.x) ** 2 + (thumb_tip.y - pinky_tip.y) ** 2) ** 0.5

            # Set thresholds for the minimum distance to consider it a gesture
            threshold = 0.1

            if distance_thumb_index > threshold:
                print("Gesture: Scroll Down")
                pyautogui.scroll(-3)  # Scroll Down

            if distance_thumb_middle > threshold:
                print("Gesture: Scroll Left")
                pyautogui.scroll(-3, x=middle_x, y=middle_y)  # Scroll Left

            if distance_thumb_ring > threshold:
                print("Gesture: Scroll Right")
                pyautogui.scroll(3, x=ring_x, y=ring_y)  # Scroll Right

            if distance_thumb_pinky > threshold:
                print("Gesture: Pressing")
                pyautogui.click(pinky_x, pinky_y)  # Perform clicking

            # Check for vertical movement between thumb and index finger
            if thumb_tip.y > index_finger_tip.y:
                print("Gesture: Scroll Up")
                pyautogui.scroll(3)  # Scroll Up

    # Display the frame
    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
