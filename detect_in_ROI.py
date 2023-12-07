import os
import cv2
import argparse

from ultralytics import YOLO
import supervision as sv
import numpy as np
from utils.Detector import Detector

# def parse_arguments() -> argparse.Namespace:
#     parser = argparse.ArgumentParser(description="YOLOv8 live")
#     parser.add_argument(
#         "--webcam-resolution", 
#         default=[1280, 720], 
#         nargs=2, 
#         type=int
#     )
#     args = parser.parse_args()
#     return args


def main():
    # args = parse_arguments()
    # frame_width, frame_height = args.webcam_resolution


    cap = cv2.VideoCapture("./test/test_data_0.MOV")
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(frame_width, frame_height)

    model = YOLO("best.pt")

    roi_txt = os.path.abspath("save_roi.txt")

    detector = Detector(model, frame_width, frame_height, roi_txt)

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame, 1)

        if ret:
            try:
                frame = detector.detect_fruit_in_box(frame)
            except Exception as error:
                print(type(error).__name__, "–", error)
                continue
            
            cv2.imshow("yolov8", frame)

            if (cv2.waitKey(30) == 27):
                break
        
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()