import cv2
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)  

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    volume = cast(interface, POINTER(IAudioEndpointVolume))

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Couldn't capture a frame.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                thumb_x, thumb_y = landmarks.landmark[4].x, landmarks.landmark[4].y
                index_x, index_y = landmarks.landmark[8].x, landmarks.landmark[8].y

                distance = ((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2) ** 0.5

                min_distance = 0.02  
                max_distance = 0.2   

                if distance < min_distance:
                    volume.SetMasterVolumeLevelScalar(0, None)
                elif distance > max_distance:
                    volume.SetMasterVolumeLevelScalar(1, None)
                else:
                    normalized_distance = (distance - min_distance) / (max_distance - min_distance)
                    volume.SetMasterVolumeLevelScalar(normalized_distance, None)

        cv2.imshow("Hand Gesture Volume Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
