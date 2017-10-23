from lib import S3FileManager


def downloadFile_Cloud(pathFile,fileName):
    #fileManager = S3FileManager.S3FileManger('mf/out/ehr','mf/in/hetra')
    fileManager = S3FileManager.S3FileManger('mf/out','ehr/out/mf')
    fileManager.download_file(pathFile,fileName)
    print 'Finished downloading the file'

