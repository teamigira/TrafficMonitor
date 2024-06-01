from FourWaysCounter import process_video
from backupfiles.get_video_file import get_latest_file_path
from threading import Thread
import os

output_files = [
    os.path.join('TrafficLogs', 'car_count_data1.txt'),
    os.path.join('TrafficLogs', 'car_count_data2.txt'),
    os.path.join('TrafficLogs', 'car_count_data3.txt'),
    os.path.join('TrafficLogs', 'car_count_data4.txt')
]

def process_video_thread(file_path, output_file):
    process_video(file_path, output_file)

def count_and_list_contents(path):
    threads = []
    
    try:
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                print(f"Dir: {os.path.join(root, dir)}")
            
            i = 0
            for file in files:
                if i >= len(output_files):
                    print("More files than output destinations. Skipping extra files.")
                    break
                file_path = os.path.join(root, file)
                print(f"File: {file_path}")
                
                thread = Thread(target=process_video_thread, args=(file_path, output_files[i]))
                threads.append(thread)
                thread.start()
                i += 1
        
        for thread in threads:
            thread.join()
             
    except FileNotFoundError:
        print(f"The directory {path} was not found.")
    except PermissionError:
        print(f"Permission denied to access {path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

count_and_list_contents('cctv_footages')
