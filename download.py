import hashlib  # 计算SHA1哈希值
import os  # 与操作系统进行交互
import tarfile  # 处理.tar文件
import zipfile  # 处理.zip文件
import requests  # 发送HTTP请求

# @save
DATA_HUB = dict()  # 创建一个字典，用于存储数据集的URL和SHA1哈希值
DATA_URL = 'http://d2l-data.s3-accelerate.amazonaws.com/'

def download(name, cache_dir=os.path.join('..', 'data')):  #@save
    """下载一个DATA_HUB中的文件，返回本地文件名"""
    # name: 要下载的数据集的名称；cache_dir: 下载文件的缓存目录
    assert name in DATA_HUB, f"{name} 不存在于 {DATA_HUB}"  # 断言：判断为false的时候触发异常，直接报错
    url, sha1_hash = DATA_HUB[name]  # SHA-1曾广泛用于确保数据完整性（文件传输或存储前后的值来对比）
    os.makedirs(cache_dir, exist_ok=True)  # 创建缓存目录，如果目录已存在则忽略
    fname = os.path.join(cache_dir, url.split('/')[-1])  # 构建完整的本地文件路径
    if os.path.exists(fname):  # 如果文件已存在于本地
        sha1 = hashlib.sha1()  # 创建一个SHA1哈希对象
        with open(fname, 'rb') as f:  # 打开文件
            while True:
                data = f.read(1048576)  # 读取文件内容，每次读取1MB
                if not data:  # 如果读取到文件末尾
                    break
                sha1.update(data)  # 更新哈希对象
        if sha1.hexdigest() == sha1_hash:  # 如果计算出的哈希值与预期的哈希值匹配
            return fname  # 返回文件名，表示命中缓存
    print(f'正在从{url}下载{fname}...')  # 输出下载信息
    r = requests.get(url, stream=True, verify=True)  # 发送GET请求下载文件
    with open(fname, 'wb') as f:  # 以二进制写入模式打开文件
        f.write(r.content)  # 将下载的内容写入文件
    return fname  # 返回下载后的文件名


def download_extract(name, folder=None):  # @save
    """下载并解压zip/tar文件"""
    fname = download(name)  # 调用之前定义的download函数来下载文件
    base_dir = os.path.dirname(fname)  # 获取下载文件所在的目录
    data_dir, ext = os.path.splitext(fname)  # 分离文件名和扩展名
    if ext == '.zip':
        fp = zipfile.ZipFile(fname, 'r')  # 如果是.zip文件，则创建一个ZipFile对象用于解压
    elif ext in ('.tar', '.gz'):
        fp = tarfile.open(fname, 'r')  # 如果是.tar或.gz文件，则创建一个tarfile对象用于解压
    else:
        assert False, '只有zip/tar文件可以被解压缩'  # 如果文件既不是.zip也不是.tar或.gz，则抛出异常
    fp.extractall(base_dir)  # 解压文件到base_dir目录
    # 如果提供了folder参数，则返回base_dir与folder的组合路径，否则返回data_dir
    return os.path.join(base_dir, folder) if folder else data_dir


def download_all():  # @save
    """下载DATA_HUB中的所有文件"""
    for name in DATA_HUB:
        download(name)  # 对DATA_HUB字典中的每个数据集名称，调用download函数下载文件