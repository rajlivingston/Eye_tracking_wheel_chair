import cv2
import mediapipe as mp
import serial
import time

# Initialize serial communication with Arduino
# Change 'COM3' to your Arduino's port
arduino = serial.Serial('COM12', 9600, timeout=1)
time.sleep(2)
print(" Connected to Arduino")

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)

# Helper function to send commands
def send_command(cmd):
    arduino.write(cmd.encode())
    print(f" Command sent: {cmd}")

# Previous command to avoid repetition
prev_cmd = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    h, w, _ = frame.shape
    command = 'S'  # Default stop

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get important eye landmarks
            left_eye = face_landmarks.landmark[33]   # Left eye iris
            right_eye = face_landmarks.landmark[263] # Right eye iris
            nose_tip = face_landmarks.landmark[1]    # Nose center

            lx, ly = int(left_eye.x * w), int(left_eye.y * h)
            rx, ry = int(right_eye.x * w), int(right_eye.y * h)
            nx, ny = int(nose_tip.x * w), int(nose_tip.y * h)

            # Calculate gaze direction
            eye_center_x = (lx + rx) // 2
            dx = eye_center_x - nx

            # Draw points
            cv2.circle(frame, (lx, ly), 3, (0, 255, 0), -1)
            cv2.circle(frame, (rx, ry), 3, (0, 255, 0), -1)
            cv2.circle(frame, (nx, ny), 3, (255, 0, 0), -1)

            # Determine direction based on horizontal movement
            if dx > 35:
                command = 'R'   # Look Right
                cv2.putText(frame, "→ RIGHT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            elif dx < -35:
                command = 'L'   # Look Left
                cv2.putText(frame, "← LEFT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            else:
                # Check vertical direction
                if ly < ny - 20:
                    command = 'F'   # Look Up
                    cv2.putText(frame, "↑ FORWARD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                elif ly > ny + 20:
                    command = 'B'   # Look Down
                    cv2.putText(frame, "↓ BACKWARD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                else:
                    command = 'S'   # Stop
                    cv2.putText(frame, "⏹ STOP", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # Send command only if it changes
    if command != prev_cmd:
        send_command(command)
        prev_cmd = command

    cv2.imshow("Eye Tracking Wheelchair", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        send_command('S')
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
