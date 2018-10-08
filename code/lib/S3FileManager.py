import boto3


class S3FileManger:
    BUCKET_NAME = 'ict4life-exchanges'

    def __init__(self, out_dir, in_dir):
        self.params = dict(out_dir=out_dir, in_dir=in_dir)

    #
    def latest_document(self, destination):
        try:
            s3 = boto3.client("s3")
            print 'Bucket: ' + self.BUCKET_NAME
            print 'Dir: ' + self.params.get("in_dir")
            response = s3.list_objects_v2(Bucket=self.BUCKET_NAME, Prefix=self.params.get("in_dir"))
            last_modified = sorted(response.get("Contents"), key=lambda content: content.get("LastModified"),
                                   reverse=True)
            s3.download_file(self.BUCKET_NAME, destination, last_modified[0].get("Key"))
            return 1
        except Exception as e:
            print e
            return 0

    def upload_file(self, origin, filename):
        try:
            s3 = boto3.client("s3")
            s3.upload_file(origin, self.BUCKET_NAME, self.params.get("out_dir") + '/' + filename)
            return 1
        except Exception as e:
            print e
            return 0

    def download_file(self, destination, filename):
        try:
            s3 = boto3.client("s3")
            print 'Go into download file with params: ' + self.params.get("in_dir")
            print 'Filename coming is:' + filename
            print 'Target destination:' + destination
            s3.download_file(self.BUCKET_NAME, self.params.get("in_dir") + '/' + filename, destination)
            return 1
        except Exception as e:
            print e
            return 0
