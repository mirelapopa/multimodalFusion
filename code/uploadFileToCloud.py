from lib import S3FileManager

def uploadFile_Cloud(pathFile,fileName):
    try: 
        fileManager = S3FileManager.S3FileManger('ehr/out/dst','mf/in/ehr')
        f=fileManager.upload_file(pathFile,fileName)
        if f:
            print 'Finished uploading the file to the cloud'
    except ValueError:
        print ValueError
    
    
   
