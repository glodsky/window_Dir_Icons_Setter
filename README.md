# window_Dir_Icons_Setter
window's directory default icons are  poor , so I write some codes to handle them. The routine is read dirName and download icons from the Web with using the dirName as keyword  ...  When I calling function win32api.WriteProfileSection  to set Desktop.ini , I'm camed in trouble , How to pass the args kargs , I check all win32api source code to find some lights but failtured. So I turned to write anthoer tool to reach my Target . Using the old IDE to write VB code , is a wonderful feeling.  ...... I found the road by reading the Help docs Python how to use the ctypes to call DLL'api  . Details information is at  ctypes_call_dll_setIcons201902180207   Happy when pass

    prototype2 = WINFUNCTYPE(c_int,LPCWSTR,LPCWSTR,LPCWSTR,LPCWSTR)
    paramflags2 = (1,"sectionName",".ShellClassInfo"), (1, "keyName", "IconFile"), \
                  (1, "keyValue", "%SystemRoot%\\system32\\SHELL32.dll,186"), (1, "fileName", "You must have setted")
    WritePrivateProfileString = prototype2(("WritePrivateProfileStringW",windll.kernel32),paramflags2) 
    WritePrivateProfileString(keyValue= icon ,fileName=desktop_ini)
    WritePrivateProfileString(keyName="IconIndex",keyValue="0",fileName=desktop_ini)
