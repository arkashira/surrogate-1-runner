import cv2
import numpy as np

class MediaPlayer:
    def __init__(self):
        self.brightness = 1.0  # Default brightness
        self.auto_adjust = True  # Default to automatic brightness adjustment

    def set_brightness(self, brightness):
        """Manually set the brightness level."""
        self.brightness = brightness
        self.auto_adjust = False

    def auto_adjust_brightness(self, frame):
        """Automatically adjust the brightness based on the frame content."""
        if not self.auto_adjust:
            return frame

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate the average brightness
        avg_brightness = np.mean(gray)

        # Adjust the brightness based on the average brightness
        if avg_brightness < 50:
            self.brightness = 1.5
        elif avg_brightness < 100:
            self.brightness = 1.2
        else:
            self.brightness = 1.0

        # Apply the brightness adjustment
        frame = cv2.convertScaleAbs(frame, alpha=self.brightness, beta=0)
        return frame

    def play(self, video_path):
        """Play the video with the current brightness settings."""
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if self.auto_adjust:
                frame = self.auto_adjust_brightness(frame)
            else:
                frame = cv2.convertScaleAbs(frame, alpha=self.brightness, beta=0)

            cv2.imshow('Media Player', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()