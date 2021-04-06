# TODO: replace this module with normal file operation before submitting

from minio import Minio
from tqdm.auto import tqdm, trange

from . import config
import os
import pathlib


class StorageError(Exception):
    pass


client = Minio(config.ENDPOINT,
               access_key=config.ACCESS_KEY,
               secret_key=config.SECRET_KEY)


def put_object(key, path):
    with open(path, 'rb') as file_data:
        file_stat = os.stat(path)
        client.put_object(config.BUCKET, key, file_data, file_stat.st_size)


def get_object(key):
    '''
    Returns the file in object storage. This is done by first checking if the file
    is in cache. If not, download it from object storage.
        Returns:
            Path string of the object cached on disk
    '''
    cache_obj = data_dir() / key
    if cache_obj.exists():
        return str(cache_obj)
    key = f"data/personal/data/{key}"
    print(f"not found in cache, fetching from {key}")
    data = client.get_object(config.BUCKET, key)
    try:
        cache_obj.parent.mkdir(parents=True)
    except:
        pass
    with open(str(cache_obj) + ".tmp", 'wb') as file_data:
        for d in tqdm(data.stream(1024), unit='KB'):
            file_data.write(d)
    pathlib.Path(str(cache_obj) + ".tmp").rename(cache_obj)
    return str(cache_obj)


def run_dir():
    '''
    Returns the directory for saving runtime info such as model data.
        Returns:
            path (Path): the path object of run directory. If you need to get
                         string of the path, use `str(run_dir())`
    '''
    return pathlib.Path(__file__).parent.absolute().parent.parent / "cache" / "run"


def data_dir():
    '''
    Returns the directory for saving immutable data such as train set. Note that
    data dir is immutuble and managed by object storage. You should always get an
    object (or file) using `get_object`, instead of directly providing the data path.
        Returns:
            path (Path): the path object of data directory. If you need to get
                         string of the path, use `str(data_dir())`
    '''
    return pathlib.Path(__file__).parent.absolute().parent.parent / "cache" / "data"
