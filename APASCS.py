import serial
from pynput.keyboard import Controller, Key, Listener

serial_port = serial.Serial('COM6', 9600)
keyboard = Controller()

paused = False  # Flag to control whether to process keyboard inputs

def on_key_release(key):
    global paused
    if key == Key.esc:
        paused = not paused
        print("Toggled pausing/unpausing input processing.")

with Listener(on_release=on_key_release) as listener:
    while True:
        try:
            data = serial_port.readline()
            if data:
                try:
                    data_str = data.decode().strip()

                    # Check for the pause/unpause signal 'P' from Arduino
                    if data_str == "P":
                        paused = not paused
                        print("Toggled pausing/unpausing input processing.")
                        continue

                    # Check for the reset button signal '1' from Arduino
                    if data_str == "1":
                        print("Reset button pressed. Pausing/resuming connection.")
                        paused = not paused  # Toggle the paused state
                        # You can add code here to perform any action when the reset button is pressed

                    # Assuming you have 8 data values: gyro_x, gyro_y, gyro_z, pot, joystickX, joystickY, fireButtonState, resetButtonState
                    inputs = data_str.split("|")
                    if len(inputs) == 8:
                        _, _, _, pot, joystickX, joystickY, fireButtonState, resetButtonState = inputs  # Ignore gyro data

                        # Convert data to appropriate values
                        pot = int(pot)
                        joystickX = int(joystickX)
                        joystickY = int(joystickY)
                        fireButtonState = True if fireButtonState == "1" else False
                        resetButtonState = True if resetButtonState == "1" else False

                        # Print input values
                        print(f"Pot: {pot} | JoyX: {joystickX} | JoyY: {joystickY} | Fire: {fireButtonState} | Reset: {resetButtonState}")

                        # Simulate keyboard inputs based on data values
                        # Modify this section to match your desired behavior
                        if not paused:
                            if joystickX < 400:
                                print("Turning left")
                                keyboard.press('a')
                                keyboard.release('d')
                            elif joystickX > 600:
                                print("Turning right")
                                keyboard.press('d')
                                keyboard.release('a')
                            else:
                                print("Stopped turning")
                                keyboard.release('a')
                                keyboard.release('d')

                            if joystickY < 400:
                                print("Moving forward")
                                keyboard.press('w')
                                keyboard.release('s')
                            elif joystickY > 600:
                                print("Moving backward")
                                keyboard.press('s')
                                keyboard.release('w')
                            else:
                                print("Stopped moving")
                                keyboard.release('w')
                                keyboard.release('s')

                            if pot < 400:
                                print("Turning left with potentiometer")
                                keyboard.press('q')
                                keyboard.release('e')
                            elif pot > 800:
                                print("Turning right with potentiometer")
                                keyboard.press('e')
                                keyboard.release('q')
                            else:
                                print("Stopped moving")
                                keyboard.release('e')
                                keyboard.release('q')

                            if fireButtonState:
                                print("Firing!")
                                keyboard.press('r')
                                keyboard.release('r')

                except UnicodeDecodeError:
                    pass
        except KeyboardInterrupt:
            break

serial_port.close()
