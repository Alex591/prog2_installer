import subprocess
import os
from subprocess import Popen
import sys


# Ugyanaz mint az installer.py,csak mivel jelenleg a pyqt6-tools nincs frissítve python 3.10-re, plusz lépéseket kell tenni
# https://github.com/altendky/pyqt-tools/issues/98


def installer(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


def uninstaller(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', package])


def run_batch_file(file_path):
    Popen(file_path, creationflags=subprocess.CREATE_NEW_CONSOLE)



if __name__ == '__main__':
    # telepités


    installer('PyQt6-6.1.0-py3-none-win_amd64.whl')
    installer('pyqt6_plugins-6.1.0.2.2-py3-none-win_amd64.whl')
    installer('pyqt6-tools')
    installer('PySide6')

    # workaround

    ##create desktop shortcut

    try:
        import qt6_applications as _
        qt_designer_location=_.__path__[0]+"\\Qt\\bin\\designer.exe"

        script = open("script.bat", "w")
        print("@echo off", file=script)
        print('set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"', file=script)
        print('echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%', file=script)
        print('echo sLinkFile = "%USERPROFILE%\Desktop\QT Designer.lnk" >> %SCRIPT%', file=script)
        print('echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%', file=script)
        print(f'echo oLink.TargetPath = "{qt_designer_location}" >> %SCRIPT%', file=script)
        print('echo oLink.Save >> %SCRIPT%', file=script)
        print('cscript /nologo %SCRIPT%', file=script)
        print('del %SCRIPT%', file=script)
        print('DEL "%~f0"', file=script)
        script.close()
        scriptdir = os.getcwd() + "\script.bat"
        run_batch_file('script.bat')
    except Exception as e: print(e)
        

