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


def check_for_conda() -> bool:
    # ha conda környezet van akkor másképp néz ki a fájlstruktúra ahol az exe van
    return os.path.exists(os.path.join(sys.prefix, 'conda-meta'))


if __name__ == '__main__':
    # telepités


    installer('PyQt6-6.1.0-py3-none-win_amd64.whl')
    installer('pyqt6_plugins-6.1.0.2.2-py3-none-win_amd64.whl')
    installer('pyqt6-tools')

    # workaround

    ##create desktop shortcut

    qt_designer_location = sys.executable
    # sys.executable
    # A string giving the absolute path of the executable binary for the Python interpreter, on systems where this makes sense.
    # If Python is unable to retrieve the real path to its executable, sys.executable will be an empty string or None
    conda = check_for_conda()
    hossz = len(qt_designer_location) - 18 if not conda else len(qt_designer_location) - 10
    qt_designer_location = qt_designer_location[:hossz]
    # a sys.executeable által visszaadott stringből levágjuk a "Scripts\python.exe" vagy a "python.exe"-t
    # conda estében a "python.exe"-t kell csak levágni
    qt_designer_location = qt_designer_location + 'Lib\site-packages\qt6_applications\Qt\\bin\\designer.exe'
    print(qt_designer_location)

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
