import cv2
def load_video(video_source):
    """Loads a video from a file or webcam.

    Args:
        video_source: The path to the video file or the webcam index (e.g., 0 for the default webcam).

    Returns:
        The video capture object (cv2.VideoCapture). Returns None on failure.
    """
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"Error: Could not open video source: {video_source}")
        return None  # Important: Return None for error handling
    return cap

def read_frame(cap):
    """Reads a single frame from the video capture.

    Args:
        cap: The cv2.VideoCapture object.

    Returns:
        A tuple containing:
        - ret: True if a frame was successfully read, False otherwise.
        - frame: The captured frame (a NumPy array), or None if no frame was read.
    """
    if cap is None:
        return False, None  # Handle the case where cap is None
    ret, frame = cap.read()
    return ret, frame

def release_video(cap):
    """Releases the video capture object."""
    if cap is not None and cap.isOpened():  # Check if cap is valid
        cap.release()