from storages.backends.s3 import S3Storage


#class StaticFileStorage(S3Storage):
#    #helpers.cloudr2.storages.MediaFileStorage
#    location = "static"


class MediaFileStorage(S3Storage):
    #helpers.cloudr2.storages.MediaFileStorage
    location = "media"