import cv2
import time
import json
import sys
import os

from video_processing import load_video, read_frame, release_video
from object_detection import detect_vehicles
from traffic_analysis import count_vehicles, calculate_speed, detect_congestion
from traffic_statistics import generate_detailed_stats


def visualize_traffic_data(frame, boxes, vehicle_count, speeds, congestion):
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.putText(frame, f"Vehicles: {vehicle_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if speeds:
        avg_speed = sum(speeds.values()) / len(speeds)
        cv2.putText(frame, f"Avg Speed: {avg_speed:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if congestion:
        cv2.putText(frame, "Congestion Detected!", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return frame


def analyze_and_suggest(vehicle_count, congestion):
    if congestion:
        return [
            "Traffic congestion detected.",
            "Adaptive signal timing recommended.",
            "Consider traffic redistribution."
        ]
    else:
        return ["Traffic flow is normal."]


def main(input_video_path, output_video_path, data_output_path):
    cap = load_video(input_video_path)
    if cap is None:
        print("Error loading video.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(
        output_video_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (frame_width, frame_height)
    )

    prev_frame_time = time.time()
    prev_boxes = []
    vehicle_count = 0
    congestion = False
    speeds = {}

    while True:
        ret, frame = read_frame(cap)
        if not ret:
            break

        current_time = time.time()
        elapsed_time = current_time - prev_frame_time
        prev_frame_time = current_time

        boxes = detect_vehicles(frame)
        vehicle_count = count_vehicles(boxes)
        speeds = calculate_speed(prev_boxes, boxes, elapsed_time)
        congestion = detect_congestion(vehicle_count, frame_width, frame_height)

        output_frame = visualize_traffic_data(
            frame, boxes, vehicle_count, speeds, congestion
        )

        out.write(output_frame)
        prev_boxes = boxes

    release_video(cap)
    out.release()
    cv2.destroyAllWindows()

    suggestions = analyze_and_suggest(vehicle_count, congestion)

    detailed_stats = generate_detailed_stats(
        vehicle_count=vehicle_count,
        speeds=list(speeds.values()) if speeds else []
    )

    analysis_data = {
        "vehicle_count": vehicle_count,
        "congestion_level": "High" if congestion else "Low",
        "detailed_statistics": detailed_stats,
        "suggestions": suggestions
    }

    os.makedirs(os.path.dirname(data_output_path), exist_ok=True)
    with open(data_output_path, "w") as f:
        json.dump(analysis_data, f, indent=4)

    print("Analysis complete. Data saved.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <input> <output> <data>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
