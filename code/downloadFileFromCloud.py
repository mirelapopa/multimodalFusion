from lib import S3FileManager

#def downloadFile_Cloud(pathFile,fileName):    
#	fileManager = S3FileManager.S3FileManger('mf/out','ehr/out/mf')
#    fileManager.download_file(pathFile,fileName)
#    print 'Finished downloading the file'
	
def downloadFile_CloudEHR(pathFile):
    fileManager = S3FileManager.S3FileManger('mf/out','mf/in/ehr')
    #fileManager.download_file(pathFile,fileName)
    fileManager.latest_document(pathFile) 
    print 'Finished downloading the EHR file'

def downloadFile_CloudHETRA(pathFile):    
    fileManager = S3FileManager.S3FileManger('mf/out','mf/in/hetra')
    #fileManager.download_file(pathFile,fileName)
    fileManager.latest_document(pathFile)  
    print 'Finished downloading the HETRA file'

