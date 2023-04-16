from main import find_video_with_move_object
import multiprocessing
import os
import time

video_root = "\\\\WDMyCloud\\Public\\xiaomi_camera_videos\\94f8272471d5"
target_root = "F:\\xiaomi_camera_videos"


def pool_realize():
    """实测没效果，多任务每个任务会变慢，实际还是单任务速度，cpu占用会增加"""
    start = time.time()
    # threads_num = multiprocessing.cpu_count()
    threads_num = 2
    pool = multiprocessing.Pool(threads_num)
    for job in os.listdir(video_root):
        if not os.path.exists(os.path.join(target_root, job)):
            result = pool.apply_async(find_video_with_move_object, args=(os.path.join(video_root, job), target_root))
    pool.close()
    pool.join()
    print(f"{time.time() - start:.2f} s")


if __name__ == "__main__":
    start = time.time()
    # threads_num = multiprocessing.cpu_count()
    threads_num = 2
    pool = multiprocessing.Pool(threads_num)
    for job in os.listdir(video_root):
        if not os.path.exists(os.path.join(target_root, job)):
            result = pool.apply_async(find_video_with_move_object, args=(os.path.join(video_root, job), target_root))
    pool.close()
    pool.join()
    print(f"{time.time() - start:.2f} s")