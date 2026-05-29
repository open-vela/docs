# mediatool测试资源和测试步骤

## 测试资源

附件：[测试资源.zip](测试资源.zip)

## 测试步骤

| 测试项 | 测试步骤 | 期望结果 | 测试结果 | 测试验证 |
|---|---|---|---|---|
| video H264 解码播放 (视频height < 1080) | 1.将测试文件"media_file_h264.mp4"上传至开发板中（比如存放在/data/media_file_h264.mp4）<br/>2.执行mediatool 进入测试工具命令shell窗口<br/>3.在"mediatool>"下依次执行如下命令：<br/>    3.1）open Video<br/>    3.2）prepare 0 url /data/media_file_h264.mp4<br/>    3.3）start 0<br/>4.关闭播放 执行 close 0<br/>5.退出mediatool工具命令界面输入 q | 3.3)视频播放正常；视频中的声音输出正常；无黑屏现象；无crash现象； | 验证解码显示正常即可（AV同步问题暂时忽略）<br/>无crash<br/>无黑屏 | PASS |
| video H265 解码播放 (视频height < 1080) | 1.将测试文件"media_file_h265.mp4"上传至开发板中（比如存放在/data/media_file_h265.mp4）<br/>2.执行mediatool 进入测试工具命令shell窗口<br/>3.在"mediatool>"下依次执行如下命令：<br/>    3.1）open Video<br/>    3.2）prepare 0 url /data/media_file_h265.mp4<br/>    3.3）start 0<br/>4.关闭播放 执行 close 0<br/>5.退出mediatool工具命令界面输入 q | 3.3)视频播放正常；视频中的声音输出正常；无黑屏现象；无crash现象； | 验证解码显示正常即可（AV同步问题暂时忽略）<br/>无crash<br/>无黑屏 | PASS |
| Audio mp3 解码播放 | 1.将测试文件"audio_file.mp3"上传至开发板中（比如存放在/data/audio_file.mp3）<br/>2.执行mediatool 进入测试工具命令shell窗口<br/>3.在"mediatool>"下依次执行如下命令：<br/>    3.1）open Music<br/>    3.2）prepare 0 url /data/audio_file.mp3<br/>    3.3）start 0<br/>4.关闭播放 执行 close 0<br/>5.退出mediatool工具命令界面输入 q | 3.3)音乐播放正常无卡顿；无crash现象 | 播放声音正常<br/>无crash | PASS |
| Audio opus 解码播放 | 1.将测试文件"audio_file.opus"上传至开发板中（比如存放在/data/audio_file.opus）<br/>2.执行mediatool 进入测试工具命令shell窗口<br/>3.在"mediatool>"下依次执行如下命令：<br/>    3.1）open Music<br/>    3.2）prepare 0 url /data/audio_file.opus<br/>    3.3）start 0<br/>4.关闭播放 执行 close 0<br/>5.退出mediatool工具命令界面输入 q | 3.3)音乐播放正常无卡顿；无crash现象 | 播放声音正常<br/>无crash | PASS |
| Audio aac 解码播放 | 1.将测试文件"audio_file.aac"上传至开发板中（比如存放在/data/audio_file.aac）<br/>2.执行mediatool 进入测试工具命令shell窗口<br/>3.在"mediatool>"下依次执行如下命令：<br/>    3.1）open Music<br/>    3.2）prepare 0 url /data/audio_file.aac<br/>    3.3）start 0<br/>4.关闭播放 执行 close 0<br/>5.退出mediatool工具命令界面输入 q | 3.3)音乐播放正常无卡顿；无crash现象 | 播放声音正常<br/>无crash | PASS |
| Audio wav 解码播放 | 1.将测试文件"audio_file.wav"上传至开发板中（比如存放在/data/audio_file.wav）<br/>2.执行mediatool 进入测试工具命令shell窗口<br/>3.在"mediatool>"下依次执行如下命令：<br/>    3.1）open Music<br/>    3.2）prepare 0 url /data/audio_file.wav<br/>    3.3）start 0<br/>4.关闭播放 执行 close 0<br/>5.退出mediatool工具命令界面输入 q | 3.3)音乐播放正常无卡顿；无crash现象 | 播放声音正常<br/>无crash | PASS |
