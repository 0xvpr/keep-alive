"""
Project: keep-alive.py

Creator: VPR
Created: April 23, 2022
Updated: April 23, 2022

Description:
    This is a simple program that will automatically press and release the caps lock key
    in order to keep a session alive.

"""
import ctypes

from time import sleep

### Globals ###
KEYEVENTF_KEYUP = 0x0002

### Imports ###
SendInput = ctypes.windll.user32.SendInput

### C struct redefinitions ###
class KeyBdInput(ctypes.Structure):
    """
    typedef struct tagKEYBDINPUT {
        WORD      wVk;
        WORD      wScan;
        DWORD     dwFlags;
        DWORD     time;
        ULONG_PTR dwExtraInfo;
    } KEYBDINPUT, *PKEYBDINPUT, *LPKEYBDINPUT;
    """

    _fields_ = [
        ("wVk",         ctypes.c_ushort),
        ("wScan",       ctypes.c_ushort),
        ("dwFlags",     ctypes.c_ulong),
        ("time",        ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class HardwareInput(ctypes.Structure):
    """
    typedef struct tagHARDWAREINPUT {
        DWORD uMsg;
        WORD  wParamL;
        WORD  wParamH;
    } HARDWAREINPUT, *PHARDWAREINPUT, *LPHARDWAREINPUT;
    """

    _fields_ = [
        ("uMsg",        ctypes.c_ulong),
        ("wParamL",     ctypes.c_short),
        ("wParamH",     ctypes.c_ushort)
    ]

class MouseInput(ctypes.Structure):
    """
    typedef struct tagMOUSEINPUT {
        LONG      dx;
        LONG      dy;
        DWORD     mouseData;
        DWORD     dwFlags;
        DWORD     time;
        ULONG_PTR dwExtraInfo;
    } MOUSEINPUT, *PMOUSEINPUT, *LPMOUSEINPUT;
    """
    _fields_ = [
        ("dx",          ctypes.c_long),
        ("dy",          ctypes.c_long),
        ("mouseData",   ctypes.c_ulong),
        ("dwFlags",     ctypes.c_ulong),
        ("time",        ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class Input_I(ctypes.Union):
    """
    union {
        MOUSEINPUT    mi;
        KEYBDINPUT    ki;
        HARDWAREINPUT hi;
    } DUMMYUNIONNAME;
    """

    _fields_ = [
        ("ki",          KeyBdInput),
        ("mi",          MouseInput),
        ("hi",          HardwareInput)
    ]

class Input(ctypes.Structure):
    """
    typedef struct tagINPUT {
        DWORD type;
        union {
            MOUSEINPUT    mi;
            KEYBDINPUT    ki;
            HARDWAREINPUT hi;
        } DUMMYUNIONNAME;
    } INPUT, *PINPUT, *LPINPUT;
    """
    _fields_ = [
        ("type",        ctypes.c_ulong),
        ("ii",          Input_I)
    ]

### Functions ###
def PressKey(vkey: int) -> None:
    ii_ = Input_I()
    ii_.ki = KeyBdInput()
    ii_.ki.wVk = ctypes.c_ushort(vkey)

    input_ = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(input_), ctypes.sizeof(input_))

def ReleaseKey(vkey: int) -> None:
    ii_ = Input_I()
    ii_.ki = KeyBdInput()
    ii_.ki.wVk = ctypes.c_ushort(vkey)
    ii_.ki.dwFlags = ctypes.c_ulong(KEYEVENTF_KEYUP)

    input_ = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(input_), ctypes.sizeof(input_))

### Main ###

if __name__ == "__main__":
    virtual_key = 0x14 # Caps Lock
    interval = 60 * 12 # 12 minutes
    delay = 0.001

    while True:
        PressKey(virtual_key)
        sleep(delay)
        ReleaseKey(virtual_key)
        sleep(delay)
        PressKey(virtual_key)
        sleep(delay)
        ReleaseKey(virtual_key)

        sleep(interval)