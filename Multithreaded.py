import cv2
import concurrent.futures
from ultralytics import YOLO
from tracker import Tracker
from datetime import datetime
import pandas as pd
import os

model = YOLO('yolov8s.pt')
# Initialize file to store timestamp and car count
output_dir = 'TrafficLogs'
os.makedirs(output_dir, exist_ok=True)

def process_video(video_path, output_file):
    try:
        tracker = Tracker()
        cy1, cy2, offset = 371, 371, 10
        vh_down, vh_up, counter, counter1 = {}, {}, [], []
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Unable to open video file {video_path}")
            return

        frame_count, frame_skip = 0, 2  # Process every 5th frame to reduce load

        with open(output_file, 'a') as f:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1
                if frame_count % frame_skip != 0:
                    continue

                frame = cv2.resize(frame, (640, 360))  # Smaller frame size to reduce processing load

                results = model.predict(frame, verbose=False)
                car_list = []

                for index, row in pd.DataFrame(results[0].boxes.data).astype("float").iterrows():
                    x1, y1, x2, y2, _, d = map(int, row)
                    c = 'car'
                    if 'car' in c:
                        car_list.append([x1, y1, x2, y2])

                bbox_id = tracker.update(car_list)

                for bbox in bbox_id:
                    x3, y3, x4, y4, id = map(int, bbox)
                    cx, cy = (x3 + x4) // 2, (y3 + y4) // 2

                    if (cy1 + offset) > cy > (cy1 - offset):
                        vh_down[id] = cy
                    if id in vh_down and (cy2 + offset) > cy > (cy2 - offset):
                        counter.append(id)
                        vh_down.pop(id, None)

                    if (cy2 + offset) > cy > (cy2 - offset):
                        vh_up[id] = cy
                    if id in vh_up and (cy1 + offset) > cy > (cy1 - offset):
                        counter1.append(id)
                        vh_up.pop(id, None)

                car_count = len(counter)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                f.write(f"{timestamp}, {car_count}\n")

                # Display results
                for bbox in bbox_id:
                    x3, y3, x4, y4, id = map(int, bbox)
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
                    cv2.putText(frame, str(id), (x3, y3 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # Draw counting lines
                cv2.line(frame, (0, cy1), (frame.shape[1], cy1), (255, 255, 255), 2)
                cv2.line(frame, (0, cy2), (frame.shape[1], cy2), (255, 255, 255), 2)

                cv2.imshow(f"Video {video_path}", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        cap.release()
        print(f"Finished processing {video_path}")

    except Exception as e:
        print(f"Error processing video {video_path}: {e}")


if __name__ == '__main__':
    video_paths = [
        './cctv_footages/veh2.mp4',
        './cctv_footages/vehicle-counting.mp4',
        './cctv_footages/2103099-uhd_3840_2160_30fps.mp4',
        './cctv_footages/854745-hd_1280_720_50fps.mp4'
    ]

    output_files = [
        os.path.join(output_dir, 'car_count_data1.txt'),
        os.path.join(output_dir, 'car_count_data2.txt'),
        os.path.join(output_dir, 'car_count_data3.txt'),
        os.path.join(output_dir, 'car_count_data4.txt')
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_video, video_paths[i], output_files[i]) for i in range(len(video_paths))]
        concurrent.futures.wait(futures)

    print("All videos processed.")
    cv2.destroyAllWindows()
