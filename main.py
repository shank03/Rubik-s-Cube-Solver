import cv2  # Import opencv library

# Create a camera object
# The `0` in the VideoCapture param denotes the camera ID
# In case of laptop, it's usually 0
camera = cv2.VideoCapture(0)

# Check if camera is accessible
if camera.isOpened():

    # Start indefinite loop
    while True:
        # `ret` is boolean stating if frame retrieval was success
        # `frame` is the cv2.Mat object which contains the frame in the form
        # of matrix of RGB values
        ret, frame = camera.read()

        # Create a window named "Capture" and display the retrieved `frame`
        cv2.imshow("Capture", frame)

        # Listen for key
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break  # Break the loop if key hit is 'q'

    # Release camera
    camera.release()
    # Destroy the window we created
    cv2.destroyAllWindows()
