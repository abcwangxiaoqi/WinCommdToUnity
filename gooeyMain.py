from gooey import Gooey,GooeyParser
import UnityCommandLine

@Gooey(program_name="Client Package")
def start():

    parser = GooeyParser(description='setting about package client')

    #unity setting

    parser.add_argument('UnityInstallDir',
                             help='unity安装路径',
                             type=str, widget='DirChooser'
                            )

    parser.add_argument('ProjectDir',
                            help='Project路径',
                            type=str, widget='DirChooser'
                            )

    parser.add_argument('Method',
                            help='执行方法'
                            )

    parser.add_argument('-p','--Parameters',
                            help='方法参数'
                            )

    parser.add_argument('-l','--LogDir',
                            help='日志路径,默认为项目根路径',
                        type = str, widget = 'DirChooser'
                            )

    args = parser.parse_args()


    logDir = args.LogDir
    if logDir == None:
        logDir = args.ProjectDir+'/Log'

    UInstallDir = args.UnityInstallDir + '/Unity.exe'

    cmd = UnityCommandLine.UnityCommandLine(UInstallDir,args.ProjectDir,logDir)
    cmd.excuteMethod(args.Method,args.Parameters)

    return

if __name__ == '__main__':

    #install = u'E:/Unity2017.2.0P1/Editor/Unity.exe'
    #project = u'F:/PyProject/CmdUnityTest'
    #log = u'F:/PyProject/CmdUnityTest/Log'
    #method = u'CommandLine.Test'
    #para = u'p1:string p2:int'


    #cmd = UnityCommandLine.UnityCommandLine(install,project,log)
    #cmd.excuteMethod(method,para)

    start()
