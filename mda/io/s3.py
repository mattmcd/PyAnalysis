import os
import boto3


def copy_to_s3(files=None, src_loc=None, dest_loc=None, dest_bucket=None):
    """Copy downloaded files to S3
    :return: <none> Creates files on S3
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(dest_bucket)
    if dest_bucket not in map(lambda b: b.name, s3.buckets.all()):
        bucket.create(CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    for fname in files:
        bucket.upload_file(os.path.join(src_loc, fname), dest_loc + fname)


def copy_from_s3(files=None, src_loc=None, dest_loc=None, src_bucket=None):
    """Copy files from S3 to local directory

    Parameters
    ----------
    files: list of files to download, optional.  Default: all under src_loc
    src_loc: key prefix in S3, including trailing /
    dest_loc: full path to destination directory
    src_bucket: source bucket

    Returns
    -------
    <none> Downloads files to dest_loc directory
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(src_bucket)
    if not os.path.isdir(dest_loc):
        os.makedirs(dest_loc)
    if not files:
        file_objs = bucket.objects.filter(Prefix=src_loc)
    for obj in file_objs:
        fname = obj.key
        bucket.download_file(
            fname,
            os.path.join(dest_loc,
                         os.path.join(dest_loc, fname.replace(src_loc, ''))))


class S3Proxy(object):
    def __init__(self, download_date=None, bucket=None, local_dir=None, prefix=None):
        self.download_date = download_date
        self.bucket = bucket
        self.local_dir = local_dir
        self.prefix = prefix

    def get(self):
        copy_from_s3(src_loc=self.prefix,
                     dest_loc=self.local_dir,
                     src_bucket=self.bucket)

    def put(self):
        files = os.listdir(self.local_dir)
        copy_to_s3(files=files,
                   src_loc=self.local_dir,
                   dest_loc=self.prefix,
                   dest_bucket=self.bucket)