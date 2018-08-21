import subprocess
import tail
import os
import time
import configparser
import threading

class UnityCommandLine:

    InstallPath=''
    ProjectPath=''
    logFold=''
    resultFold=''

    def __init__(self,installPath,projectPath,logFold):
        self.InstallPath = installPath
        self.ProjectPath = projectPath
        self.logFold = logFold
        self.resultFold = logFold+'/result'

    def __initLogName(self):

        dayFold = time.strftime('%y%m%d', time.localtime())
        dayTime=time.strftime('%H%M%S', time.localtime())
        operationID=dayFold+dayTime
        return str.format("{0}/{1}/{2}.txt",self.logFold,dayFold,dayTime),operationID,dayFold

    #执行方法
    def excuteMethod(self,md,paramters):

        log,oID,dayStr=self.__initLogName()

        preTime=time.time()
        command = '\"{0}\" -quit -batchmode -projectPath \"{1}\" -executeMethod {2} {3} -logFile \"{4}\"'\
            .format(self.InstallPath, self.ProjectPath, md,paramters,log)

        print(command)
        #return
        curProcess = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.startConsole(log)
        returnCode = curProcess.wait()

        costTime=time.time()-preTime

        #write result in resultlog
        self.__writeResultLog(returnCode==0,oID,costTime,log,dayStr)

        if returnCode != 0:
            return False
        return True


    def startConsole(self,log):
        threading._start_new_thread(self.__tail_thread, (log,))

    def __tail_thread(self,tail_file):

        print("wait for tail file ... %s" % tail_file)

        while True:
            if os.path.exists(tail_file):
                print("Start tail file..... %s" % tail_file)
                break

        t = tail.Tail(tail_file)
        t.register_callback(self.__unity_log_tail)
        t.follow(s=1)

    def __unity_log_tail(self,txt):
        msg=str.strip(txt)
        if len(msg)>0:
            print('unity:',msg)




    def __writeResultLog(self,success,id,costTime,logpath,day):

        if os.path.exists(self.resultFold) == False:
            os.makedirs(self.resultFold)

        resultLog = str.format("{0}/{1}.ini",self.resultFold,day)

        cfg = configparser.ConfigParser()

        # must use str cause must be turn Unicode whether couldn't read right
        cfg.read(str(resultLog))

        #add section
        cfg.add_section(id)
        cfg.set(id,'success',str(success))#must be strings
        cfg.set(id,'costTime', str(costTime))
        cfg.set(id,'logpath', logpath)

        #write in log
        with open(resultLog,"w+") as fp:
            cfg.write(fp)
            fp.close()