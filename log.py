# logs go brrrrrrr
import datetime
import shutil

class LogFile():
    # create log file
    def Create():
        LATEST_LOG_FILE = open('src/log/latest.log', 'w')
        LATEST_LOG_FILE.write(str(datetime.date.today()) + '\n')
        LATEST_LOG_FILE.close()

    # check if current log file is outdated and store outdated log file
    def CheckDate():
        LATEST_LOG_FILE = open('src/log/latest.log', 'r')
        Date = LATEST_LOG_FILE.readline()
        Date = Date.replace('\n', '')
        LATEST_LOG_FILE.close()
        if Date != str(datetime.date.today()):
            shutil.copy('src/log/latest.log', 'src/log/' + Date + '.log')
            LogFile.Create()

    # write to log file in append mode and with timestamp
    def WriteLog(Error):
        LogFile.CheckDate()
        LATEST_LOG_FILE = open('src/log/latest.log', 'a')
        LATEST_LOG_FILE.write('[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ']: ' + Error + '\n')
        LATEST_LOG_FILE.close()