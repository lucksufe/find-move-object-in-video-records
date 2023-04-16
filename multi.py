from main import find_video_with_move_object
import multiprocessing
import os

video_root = "\\\\WDMyCloud\\Public\\xiaomi_camera_videos\\94f8272471d5"
target_root = "F:\\xiaomi_camera_videos"


def pool_realize():
    """实测没效果，多任务每个任务会变慢，实际还是单任务速度，cpu占用会增加"""
    # threads_num = multiprocessing.cpu_count()
    threads_num = 2
    pool = multiprocessing.Pool(threads_num)
    for job in os.listdir(video_root):
        if not os.path.exists(os.path.join(target_root, job)):
            pool.apply_async(find_video_with_move_object, args=(os.path.join(video_root, job), target_root))
    pool.close()
    pool.join()


def normal_realize():
    """分析之后发现瓶颈在videocapture的处理中grab、retrieve占用时间随任务数变多提升占比很大，dilate、erode也相应提升占比较小，循环内cv方法都会相应增加。"""
    for job in os.listdir(video_root):
        if not os.path.exists(os.path.join(target_root, job)):
            find_video_with_move_object(os.path.join(video_root, job), target_root)


def test():  # can only run under __main__
    job = "2023041300"
    cProfile.run(statement=f"find_video_with_move_object('{job}')", filename="cprofile.txt")
    pstats.Stats("cprofile.txt").sort_stats("cumulative").print_stats()


if __name__ == "__main__":
    import time
    import cProfile
    import pstats

    start = time.time()
    normal_realize()
    print(f"{time.time() - start:.2f} s")
