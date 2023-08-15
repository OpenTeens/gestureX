import cv2
import numpy as np

# Function to handle keyboard events
def keyboard_callback(event, x, y, flags, param):
    global text, img

    if event == cv2.EVENT_LBUTTONDOWN:
        user_input = cv2.waitKey(0)

        if user_input == 13:  # ASCII code for Enter key
            pass  # Do something with the entered text
        else:
            text += chr(user_input)

        img.fill(255)
        cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("Text Pad", img)


img = 255 * np.ones((200, 400, 3), dtype=np.uint8)
text = ""

# Create a window to display the text pad
cv2.namedWindow("Text Pad")
cv2.setMouseCallback("Text Pad", keyboard_callback)

while True:
    cv2.imshow("Text Pad", img)

    # Wait for the user to press the Esc key to exit
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()