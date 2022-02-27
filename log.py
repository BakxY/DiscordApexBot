# logs go brrrrrrr
import datetime
import shutil

def LogFile_Create():
    LATEST_LOG_FILE = open('src/log/latest.log', 'w')
    LATEST_LOG_FILE.write(str(datetime.date.today()) + '\n')
    LATEST_LOG_FILE.close()

def LogFile_CheckDate():
    LATEST_LOG_FILE = open('src/log/latest.log', 'r')
    Date = LATEST_LOG_FILE.readline()
    Date = Date.replace('\n', '')
    LATEST_LOG_FILE.close()
    if Date != str(datetime.date.today()):
        shutil.copy('src/log/latest.log', 'src/log/' + Date + '.log')
        LogFile_Create()

def LogFile_WriteLog(Error):
    LATEST_LOG_FILE = open('src/log/latest.log', 'a')
    LATEST_LOG_FILE.write('[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ']: ' + Error + '\n')
    LATEST_LOG_FILE.close()