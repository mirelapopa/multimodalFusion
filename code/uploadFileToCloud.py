from lib import S3FileManager

def uploadFile_Cloud(pathFile,fileName):
    fileManager = S3FileManager.S3FileManger('mf/out','ehr/out/mf')
    fileManager.upload_file(pathFile,fileName)
    print 'Finished uploading the file to the cloud'
    
    
   
