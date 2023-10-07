# Hand Gesture Volume Control

This Python script uses computer vision with MediaPipe to control the system's audio volume based on hand gestures. It detects the distance between your thumb and index finger and adjusts the system volume accordingly.

## Prerequisites

Before running the script, ensure you have the following Python packages installed:

- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- comtypes (`comtypes`)
- pycaw (`pycaw`)

You can install these packages using `pip` by running:

pip install opencv-python mediapipe comtypes pycaw


## Usage

1. Make sure your computer has a webcam.

2. Run the script by executing the following command:

python hand_gesture_volume_control.py


3. A window will open, showing the camera feed and the hand gesture control.

4. Perform hand gestures to control the volume:
   - Bring your thumb and index finger close to increase the volume.
   - Separate your thumb and index finger to decrease the volume.

5. Press the 'q' key to exit the application.

## Configuration

You can adjust the following parameters in the script to customize the volume control behavior:

- `min_distance`: Minimum distance to set volume to 0.
- `max_distance`: Maximum distance to set volume to 100%.

Feel free to modify these parameters to suit your preferences.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- This code uses the MediaPipe library for hand gesture detection.
- It also relies on the pycaw library to control the system's audio volume.

## Author

- Pritam Singh
