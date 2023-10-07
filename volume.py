import cv2
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    # Initialize the camera
    cap = cv2.VideoCapture(0)  # Use the default camera (usually the built-in webcam)

    # Get the default audio playback device
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    volume = cast(interface, POINTER(IAudioEndpointVolume))

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Error: Couldn't capture a frame.")
            break

        # Convert the frame to RGB format (required by mediapipe)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Use Mediapipe to detect hands
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                # Draw landmarks (finger joints and palm)
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the position of the thumb and index finger
                thumb_x, thumb_y = landmarks.landmark[4].x, landmarks.landmark[4].y
                index_x, index_y = landmarks.landmark[8].x, landmarks.landmark[8].y

                # Calculate the distance between thumb and index finger
                distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5

                # Map the hand gesture to volume control
                min_distance = 0.02  # Adjust this threshold as needed
                max_distance = 0.2   # Adjust this threshold as needed

                if distance < min_distance:
                    volume.SetMasterVolumeLevelScalar(0, None)
                elif distance > max_distance:
                    volume.SetMasterVolumeLevelScalar(1, None)
                else:
                    normalized_distance = (distance - min_distance) / (max_distance - min_distance)
                    volume.SetMasterVolumeLevelScalar(normalized_distance, None)

        # Display the segmented hand region
        cv2.imshow("Hand Gesture Volume Control", frame)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
