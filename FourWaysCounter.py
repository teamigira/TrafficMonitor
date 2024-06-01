import cv2
from ultralytics import YOLO
from tracker import Tracker
from backupfiles.get_video_file import get_latest_file_path
from datetime import datetime
import pandas as pd

model = YOLO('yolov8s.pt')
# Initialize file to store timestamp and car count


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

def process_video(latest_file_path,file_path):
    print(latest_file_path + file_path)
    cap = cv2.VideoCapture(latest_file_path)

    my_file = open("coco.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")

    count = 0
    tracker = Tracker()

    cy1 = 371
    cy2 = 371  # Corrected value
    offset = 10
    vh_down = {}
    vh_up = {}
    counter = []
    counter1 = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 3 != 0:
            continue
        frame = cv2.resize(frame, (1020, 500))
        results = model.predict(frame)
        a = results[0].boxes.data
        car_list = []

        for index, row in pd.DataFrame(a).astype("float").iterrows():
            x1, y1, x2, y2, _, d = map(int, row)
            c = class_list[d]
            if 'car' in c:
                car_list.append([x1, y1, x2, y2])

        bbox_id = tracker.update(car_list)

        for bbox in bbox_id:
            x3, y3, x4, y4, id = map(int, bbox)
            cx = (x3 + x4) // 2
            cy = (y3 + y4) // 2

            if (cy1 + offset) > cy > (cy1 - offset):
                vh_down[id] = cy

            if id in vh_down:
                if (cy2 + offset) > cy > (cy2 - offset):
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1)
                if counter.count(id) == 0:
                    counter.append(id)
                print(f"Counter updated: {counter}")

            if (cy2 + offset) > cy > (cy2 - offset):
                vh_up[id] = cy
            if id in vh_up:
                if (cy1 + offset) > cy > (cy1 - offset):
                    print("Vehicle crossing Lane 1")
                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                    cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1)
                if id not in counter1:
                    counter1.append(id)
                print(f"Counter1 updated: {counter1}")

        car_count = len(counter)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Append timestamp and car count to file
        with open(file_path, 'a') as f:
            f.write(f"{timestamp}, {car_count}\n")

        cv2.line(frame, (135, cy1), (921, cy1), (255, 255, 255), 1)
        cv2.putText(frame, 'Lane 1', (655, 370), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1)

        cv2.line(frame, (99, cy2), (951, cy2), (255, 255, 255), 1)
        cv2.putText(frame, 'Lane 2', (173, 394), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1)

        d = len(counter)
        u = len(counter1)
        cv2.putText(frame, 'Going Mwenge: ' + str(d), (60, 40), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1)
        cv2.putText(frame, 'Going Posta: ' + str(u), (60, 130), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1)

        print(vh_down)

        cv2.imshow("RGB", frame)
        # Here you freeze the frames so as to draw the lines
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     folder_path = 'cctv_footages'
#     latest_file_path = get_latest_file_path(folder_path)
#     process_video(latest_file_path)
