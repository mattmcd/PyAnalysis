import os

dataLoc = os.environ.get('MDA_DATA_DIR')


def data_dir(*args):
    if args == []:
        return dataLoc
    else:
        return os.path.join(dataLoc, *args)
