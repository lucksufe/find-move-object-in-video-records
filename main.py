import cv2 as cv
import time
import os
import shutil


def find_video_with_move_object(video_dir, target_dir=None, sensitive_threshold=128, object_size_threshold=5000, fps_gap=20):
    begin = time.time()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(begin)), video_dir)
    record_file = "record"
    if os.path.exists(record_file):
        with open(record_file, "r") as f:
            if video_dir in f.readlines():
                return

    k_e = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    k_d = cv.getStructuringElement(cv.MORPH_ELLIPSE, (20, 20))

    for root, dirs, files in os.walk(video_dir):
        for f in files:
            video = cv.VideoCapture(os.path.join(root, f))
            background = None
            wanted = False
            frame_num = 0
            while True:
                flag = video.grab()
                if not flag:
                    break
                if frame_num % fps_gap == 0:
                    frame_num += 1
                    _, frame = video.retrieve()
                else:
                    frame_num += 1
                    continue

                frame_gray = cv.cvtColor(frame[100:, ...], cv.COLOR_BGR2GRAY)
                if background is None:
                    background = frame_gray
                diff = cv.absdiff(frame_gray, background)
                _, diff = cv.threshold(diff, sensitive_threshold, 255, cv.THRESH_BINARY)
                diff = cv.erode(diff, k_e, iterations=1)
                diff = cv.dilate(diff, k_d, iterations=1)
                contours, _ = cv.findContours(diff, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    if cv.contourArea(c) > object_size_threshold:
                        if target_dir:
                            dir_name = os.path.basename(video_dir)
                            if not os.path.isdir(target_dir):
                                os.makedirs(target_dir, exist_ok=True)
                            target = os.path.join(target_dir, dir_name)
                            os.makedirs(target, exist_ok=True)
                            shutil.copy2(os.path.join(root, f), target)
                        # cv.imwrite(f"{f}_{frame_num}.jpg", frame)
                        # cv.imwrite(f"{f}_diff.jpg", diff)
                        wanted = True
                        break
                if wanted:
                    break
            video.release()

    end = time.time()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), video_dir, f"cost {end - begin:.2f}s")
    # with open(record_file, "w") as f:
    #     f.write(video_dir + "\n")


if __name__ == "__main__":
    start = time.time()
    find_video_with_move_object("fail")
    print(time.time() - start)
