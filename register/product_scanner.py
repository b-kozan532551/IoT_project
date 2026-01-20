import cv2
import time

# Initialize the camera (0 is usually the default webcam)
cap = cv2.VideoCapture(0)

# Initialize OpenCV's barcode detector
barcode_detector = cv2.barcode.BarcodeDetector()

# Track last detection time to avoid duplicate readings
last_detection_time = 0
cooldown_period = 2  # seconds

while True:
    # Capture a single frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Use OpenCV barcode detector to find barcodes in the current frame
    ret_bc, decoded_info, decoded_type = barcode_detector.detectAndDecode(frame)
    
    current_time = time.time()
    if ret_bc and (current_time - last_detection_time) >= cooldown_period:
        # ret_bc contains the actual barcode string(s)
        # decoded_info contains the corner point coordinates
        print(f"Found barcode: {ret_bc}")
        if decoded_type:
            print(f"Barcode type: {decoded_type}")
        last_detection_time = current_time

    cv2.imshow('video', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()