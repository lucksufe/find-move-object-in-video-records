# find-move-object-in-video-records
自用的从小米摄像头保存录像中检测有活动物体的视频，截取活动内容帧，并把对应视频保存到指定位置。

main.py中是单任务版本，做了一点优化，默认20帧比对一次，可以修改fps_gap参数调整

multi.py是多线程版本，自动检测cpu线程数，批量跑，修改video_root为日期文件夹上一级目录
