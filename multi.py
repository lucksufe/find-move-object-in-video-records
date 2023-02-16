from main import find_video_with_move_object
import multiprocessing
import os
import time

video_root = "\\\\WDMyCloud\\Public\\xiaomi_camera_videos\\94f8272471d5"
target_root = "F:\\xiaomi_camera_videos"

if __name__ == "__main__":
    start = time.time()
    threads_num = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(threads_num)
    for job in os.listdir(video_root):
        pool.apply_async(find_video_with_move_object, args=(os.path.join(video_root, job), target_root))
    pool.close()
    pool.join()
    print(time.time() - start)
