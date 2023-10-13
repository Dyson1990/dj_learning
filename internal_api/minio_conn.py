# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 17:10:25 2022

@author: Weave

单独通用脚本
"""

import minio

import os
import traceback
import pathlib
import io
from tqdm import tqdm
from datetime import timedelta

# official: sudo docker run -p 9000:9000 --name minio   -v /var/lib/minio/data:/data   -v /var/lib/minio/config:/root/.minio   minio/minio server /data
# T430: docker run -p 9000:9000 -p 9090:9090 --net=host --name minio -d --restart=always -v /var/lib/minio/data:/data -v /var/lib/minio/config:/root/.minio minio/minio server /data --console-address ":19090" -address ":19000"
# h3: docker run -p 19000:9000 -p 19090:9090 --net=host --name minio -d --restart=always -v /mnt/data/minio:/data -v /var/lib/minio/config:/root/.minio minio/minio server /data --console-address ":19090" -address ":19000"
minio_cli = minio.Minio('192.168.1.23:19000',
                        access_key='minioadmin',
                        secret_key='minioadmin',
                        secure=False,
                        # http_client=httpClient
                        )

# buckets = minio_cli.list_buckets()
# print(buckets)

# bucket = minio_cli.bucket('test')
# minio_cli.fput_object('test', 'outter/a77999643350818e138c5093e3a2ebf3.html', r'C:\Users\Weave\crawler\opencorporates\content\a77999643350818e138c5093e3a2ebf3.html')

def put_string(content, object_name, bucket_name='crawler', app_type='crawler', chr_set='utf-8'):
    object_name = pathlib.Path(object_name)
    
    b0 = content.encode(chr_set)
    minio_cli.put_object(bucket_name
                         , object_name.as_posix()
                         , io.BytesIO(b0)
                         , len(b0)
                         , content_type=f'application/{app_type}'
                         )

def put_one_file(file_path, inner_dir, bucket_name='crawler', app_type='crawler'):
    """
    上传一整个文件夹的内容到minio
    Parameters
    ----------
    file_dir : TYPE
        本地文件夹的路劲.
    inner_dir : TYPE
        minio中，bucket内部的路径.
    bucket_name : TYPE, optional
        bucket名称. The default is 'crawler'.
    app_type : TYPE, optional
        应用类型. The default is 'crawler'.
    """
    file_path = pathlib.Path(file_path)
    inner_dir = pathlib.Path(inner_dir)
    
    object_name = inner_dir.joinpath(file_path.name)
    minio_cli.fput_object(bucket_name
                          , object_name.as_posix()
                          , str(file_path)
                          , content_type=f'application/{app_type}'
                          )
    
def put_all_files(file_dir, inner_dir, bucket_name='crawler', app_type='crawler'):
    """
    上传一整个文件夹的内容到minio
    Parameters
    ----------
    file_dir : TYPE
        本地文件夹的路劲.
    inner_dir : TYPE
        minio中，bucket内部的路径.
    bucket_name : TYPE, optional
        bucket名称. The default is 'crawler'.
    app_type : TYPE, optional
        应用类型. The default is 'crawler'.

    Returns
    -------
    None.

    """
    file_dir = pathlib.Path(file_dir)
    inner_dir = pathlib.Path(inner_dir)
    for file_path in tqdm(list(file_dir.iterdir())):
        object_name = inner_dir.joinpath(file_path.name)

        minio_cli.fput_object(bucket_name
                              , object_name.as_posix()
                              , str(file_path)
                              , content_type=f'application/{app_type}'
                              )
        
def get_file(object_name, bucket_name='crawler'):
    """
    由于读取不存在的obj会报错，这里增加一个读取的函数
    """
    try:
        obj = minio_cli.get_object(bucket_name, object_name)
        return obj.read().decode('utf-8')
    except minio.error.S3Error as e:
        if e.code == 'NoSuchKey':
            return None
        else:
            raise minio.error.S3Error(str(e))
            
def get_url(object_name, expiry=timedelta(days=1), bucket_name='crawler'):
    """
    由于读取不存在的obj会报错，这里增加一个读取的函数
    """
    try:
        obj = minio_cli.presigned_get_object(bucket_name, object_name)
        print(dir(obj))
        return obj
    except minio.error.S3Error as e:
        if e.code == 'NoSuchKey':
            return None
        else:
            raise minio.error.S3Error(str(e))
            
def empty_bucket(bucket_name='crawler'):
    warning = input('真的要清空：'+bucket_name+'?【Y/N】')
    if warning == 'Y':
        for obj in minio_cli.list_objects(bucket_name, prefix='opencorporates/html/content'):
            print('正在删除：', obj.object_name)
            # break
            minio_cli.remove_object(obj.bucket_name, obj.object_name)
    
if __name__ == '__main__':
    # help(minio_cli.fput_object)
    # put_all_files(r'C:\Users\Weave\crawler\opencorporates\catalog'
    #               , 'opencorporates/html/catalog'
    #               )
    
    # put_all_files(r'C:\Users\Weave\crawler\opencorporates\content'
    #               , 'opencorporates/html/content'
    #               )
    # obj = get_file('opencorporates/html/content\f66c6dd53e09b3df42a9fb219635312f.html')
    # print(obj)
    # p0 = pathlib.Path('opencorporates/html/content')
    # print()
    # empty_bucket()
    # minio_cli.remove_objects('crawler', minio_cli.list_objects('crawler', prefix='opencorporates/html/catalog/'))
    # help(minio_cli.put_object)
    # output = Stream('abc')
    # minio_cli.put_object('test', 'p/abc.txt', io.BytesIO(b"hello"), len(b"hello"))
    # resp = put_string('dsafsadfsd', 'p1/https://blog.csdn.net/wsjslient/article/details/109743495', bucket_name='test')
    # print('resp', resp)
    print(get_url('opencorporates/html/catalog/00000447d9398d84f2747d80a411875b.html'))
    
    
    