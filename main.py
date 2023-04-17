import os
import shutil
import logging
import time
import cv2 as cv

logging.basicConfig(filename="main.log", filemode="a", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)


def find_video_with_move_object(video_dir, target_dir=None, sensitive_threshold=128, object_size_threshold=5000, fps_gap=20):
    begin = time.time()
    record_file = "record"
    if os.path.exists(record_file):
        with open(record_file, "r") as f:
            if f"{video_dir}\n" in f.readlines():
                return
    logging.info(f"Start detecting {video_dir}")
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
    logging.info(f"Finish detecting {video_dir} cost {end - begin:.2f}s")
    with open(record_file, "a") as f:
        f.write(video_dir + "\n")


if __name__ == "__main__":
    import sys
    from optparse import OptionParser

    optParser = OptionParser()
    optParser.add_option('-v', '--video_dir', type="string", dest='video_dir')
    optParser.add_option("-t", "--target_dir", type="string", dest="target_dir")
    opts, args = optParser.parse_args(sys.argv)
    find_video_with_move_object(video_dir=opts.video_dir, target_dir=opts.target_dir)

    # find_video_with_move_object("2023041300")
