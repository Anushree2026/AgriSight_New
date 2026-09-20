import cv2
import time

for index in range(5):
    print(f"\nChecking Camera {index}...")

    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print(f"❌ Camera {index} not available")
        continue

    ret, frame = cap.read()

    if ret:
        print(f"✅ Camera {index} is working")
        cv2.imshow(f"Camera {index}", frame)
        cv2.waitKey(3000)   # Show for 3 seconds
        cv2.destroyAllWindows()
    else:
        print(f"⚠ Camera {index} opened but no frame")

    cap.release()

print("\nCamera test completed.")