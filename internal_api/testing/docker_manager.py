# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 16:59:37 2022

@author: Weave
"""
import sys
from pathlib import Path
py_dir = Path(__file__).parent
app_dir = py_dir.parent
sys.path.append(app_dir.as_posix())

# h4上tesseract运行命令
# docker run --rm -it  -e "TESSDATA_PREFIX=/usr/share/tesseract/tesdata" -v /usr/share/tesseract:/usr/share/tesseract -v {img_dir}:/app -w /app clearlinux/tesseract-ocr:5.0 tesseract {img_name} stdout --oem 1
# example
# docker run --rm -it  -e "TESSDATA_PREFIX=/usr/share/tesseract/tesdata" -v /usr/share/tesseract:/usr/share/tesseract -v /root/Downloads:/app -w /app clearlinux/tesseract-ocr:5.0 tesseract getCapchaImage.jpg stdout --oem 1
# docker run --rm -it  -e "TESSDATA_PREFIX=/usr/share/tesseract/tesdata" -v C:\Program Files\Tesseract-OCR:/usr/share/tesseract -v C:\Users\Weave\Downloads:/app -w /app clearlinux/tesseract-ocr:5.0 tesseract getCapchaImage.jpg stdout --oem 1

import docker
client = docker.from_env()


print(dir(client))
print(client.images.list())
print(client.containers.list(all=True))
client.containers.run('clearlinux/tesseract-ocr:5.0',   # image_name 是我们docker镜像的name 
                      # detach=True,   # detach=True,是docker run -d 后台运行容器
                      remove=True,  # 容器如果stop了，会自动删除容器
                      tty=True,      # 分配一个tty  docker run -t
                      volumes=['/usr/share/tesseract:/usr/share/tesseract'
                               , '/root/Downloads:/app'], # 与宿主机的共享目录， docker run -v /var/:/opt
                      command='/bin/bash')  # The command to run in the container

if __name__ == "__main__":
    pass