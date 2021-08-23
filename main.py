import shutil, os
import win32api
import win32con
import win32event
import win32process
from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon
import ctypes
import enum
import getpass
import sys
import admin
import traceback
import types
from subprocess import call

def isUserAdmin():

    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            logging.debug("User already admin")
            return ctypes.windll.shell32.IsUserAnAdmin()

            # log_warn("debug.log", "isUserAdmin", "User already admin")
        except:
            logging.warn("Admin check failed, assuming not an admin.")
            traceback.print_exc()
            print("Admin check failed, assuming not an admin.")

            return False
    elif os.name == 'posix':
        logging.info("Checked root for Posix.")

        # Check for root on Posix
        return os.getpid() == 0
    else:
        logging.error("Unsupported orperating system for the module")
        raise RuntimeError(
            "Unsupported operating system for this module: %s" % (os.name,))


def runAsAdmin(cmdLine=None, wait=True):

    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType, types.ListType):
        raise ValueError("cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdLine[0],)
    # XXX TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    #showCmd = win32con.SW_HIDE
    lpVerb = 'runas'  # causes UAC elevation prompt.

    # print "Running", cmd, params

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.

    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        # print "Process handle %s returned code %s" % (procHandle, rc)
    else:
        rc = None

    return rc


def test():
    rc = 0
    if not isUserAdmin():
        print("You're not an admin.", os.getpid(), "params: ", sys.argv)
        #rc = runAsAdmin(["c:\\Windows\\notepad.exe"])
        rc = runAsAdmin()
    else:
        print("You are an admin!", os.getpid(), "params: ", sys.argv)
        rc = 0
    x = input('Press Enter to exit.')
    return rc


class SW(enum.IntEnum):

    HIDE = 0
    MAXIMIZE = 3
    MINIMIZE = 6
    RESTORE = 9
    SHOW = 5
    SHOWDEFAULT = 10
    SHOWMAXIMIZED = 3
    SHOWMINIMIZED = 2
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    SHOWNOACTIVATE = 4
    SHOWNORMAL = 1


class ERROR(enum.IntEnum):

    ZERO = 0
    FILE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    BAD_FORMAT = 11
    ACCESS_DENIED = 5
    ASSOC_INCOMPLETE = 27
    DDE_BUSY = 30
    DDE_FAIL = 29
    DDE_TIMEOUT = 28
    DLL_NOT_FOUND = 32
    NO_ASSOC = 31
    OOM = 8
    SHARE = 26


def main():
    print(" ")


def bootstrap():
    if ctypes.windll.shell32.IsUserAnAdmin():
        main()
    else:
        hinstance = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, sys.argv[0], None, SW.SHOWNORMAL
        )
        if hinstance <= 32:
            raise RuntimeError(ERROR(hinstance))

def AddToStartUp():
    Path = "C:\\Users\\USER\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\main.py"
    if os.path.exists(Path) == True:
        print("File already in startup dude, chill and Netflix!")
    else:
        shutil.copy("main.py", "C:\\Users\\USER\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")



if __name__ == '__main__':
    bootstrap()
    AddToStartUp()
    del_dir = r'C:\Users\USER\AppData\Local\Temp'
    shutil.rmtree(del_dir, ignore_errors=True)
    print("Deleted Files")
    print("\nULTRA SUPER IMPORTANT NOTE: Some files may not be deleted because they are being used by the system. SO, stop blaming me!")
    # recreate the deleted parent dir in case it get deleted
    # os.makedirs(del_dir)