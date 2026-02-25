# Eye Tracking Smart Wheelchair

An innovative IoT project designed to assist mobility-impaired individuals by controlling a wheelchair using eye gaze movements. This project leverages computer vision for eye tracking and Arduino for motor control.

## Overview

The system captures real-time video via a webcam, processes it using **MediaPipe Face Mesh** to detect eye movements, and translates these movements into navigation commands. These commands are then transmitted via serial communication to an **Arduino**, which drives the wheelchair's motors.

## Components

### Hardware
- **Arduino (Uno/Nano/Mega)**
- **L298N Motor Driver**
- **DC Geared Motors** (x2)
- **Webcam** (for tracking)
- **Chassis/Wheelchair Frame**
- **Jumper Wires & Power Supply**

### Software
- **Python 3.x**
- **MediaPipe** (Face Mesh)
- **OpenCV** (Video processing)
- **PySerial** (Serial communication)
- **Arduino IDE** (Motor control logic)

## Control Mapping

| Eye/Face Movement | Serial Command | Wheelchair Action |
|-------------------|----------------|-------------------|
| Look Right        | `R`            | Turn Right        |
| Look Left         | `L`            | Turn Left         |
| Look Up           | `F`            | Move Forward      |
| Look Down         | `B`            | Move Backward     |
| Center/Neutral    | `S`            | Stop              |

## Project Structure

- `Eye_tracker.py`: Python script for real-time eye tracking and command transmission.
- `Smart_Wheel_Chair.ino`: Arduino sketch to receive commands and drive the L298N motor controller.

## Setup & Installation

### 1. Arduino Setup
1. Connect the L298N motor driver to the Arduino pins as follows:
   - `ENA` -> Pin 9
   - `IN1` -> Pin 8
   - `IN2` -> Pin 7
   - `ENB` -> Pin 10
   - `IN3` -> Pin 12
   - `IN4` -> Pin 11
2. Upload `Smart_Wheel_Chair.ino` to your Arduino using the Arduino IDE.

### 2. Python Environment Setup
1. Install the required libraries:
   ```bash
   pip install opencv-python mediapipe pyserial
   ```
2. Identify your Arduino's COM port (e.g., `COM12` on Windows) and update it in `Eye_tracker.py`:
   ```python
   arduino = serial.Serial('COM12', 9600, timeout=1)
   ```

### 3. Running the Project
1. Connect the Arduino to your PC.
2. Ensure your webcam is connected.
3. Run the Python script:
   ```bash
   python Eye_tracker.py
   ```
4. A window will open showing the tracking. Move your eyes to control the wheelchair. Press `ESC` to quit.

## Troubleshooting
- **Serial Connection**: Ensure the correct COM port is selected and no other program (like Serial Monitor) is using it.
- **Tracking Sensitivity**: If the movement detection is too sensitive or slow, adjust the thresholds in `Eye_tracker.py` (e.g., `dx > 35` or `ly < ny - 20`).
- **Lighting**: Proper lighting is crucial for MediaPipe to detect facial landmarks accurately.

---
*Created as an IoT Healthcare Solution.*
