Attribute VB_Name = "modMain"
  Type BROWSEINFO
  hWndOwner       As Long
  pIDLRoot        As Long
  pszDisplayName  As Long
  lpszTitle       As String
  ulFlags         As Long
  lpfnCallback    As Long
  lParam          As Long
  iImage          As Long
End Type
  Declare Function SHBrowseForFolder Lib "SHELL32.DLL" Alias "SHBrowseForFolderA" _
        (lpBrowseInfo As BROWSEINFO) As Long
  Declare Function SHGetPathFromIDList Lib "SHELL32.DLL" Alias "SHGetPathFromIDListA" _
        (ByVal pidl As Long, ByVal pszPath As String) As Long
  Declare Function SetFileAttributes Lib "kernel32" Alias "SetFileAttributesA" _
        (ByVal lpFileName As String, ByVal dwFileAttributes As Long) As Long
  Const FileAttributeArchive = &H20, FileAttributeReadonly = &H1
  Const FileAttributeSystem = &H4, FileAttributeHidden = &H2
  Const FileAttributeDirectory = &H10
  Const BIF_RETURNONLYFSDIRS = &H1, BIF_DONTGOBELOWDOMAIN = &H2
 

Declare Function GetPrivateProfileString Lib "kernel32" Alias "GetPrivateProfileStringA" (ByVal lpApplicationName As String, ByVal lpKeyName As Any, ByVal lpDefault As String, ByVal lpReturnedString As String, ByVal nSize As Long, ByVal lpFileName As String) As Long
  Declare Function WritePrivateProfileString Lib "kernel32" Alias "WritePrivateProfileStringA" (ByVal lpApplicationName As String, ByVal lpKeyName As String, ByVal lpString As String, ByVal lpFileName As String) As Long
  
Public Function BrowseFolder(hWnd As Long, szDialogTitle As String) As String
On Local Error Resume Next
    Dim X As Long, BI As BROWSEINFO, dwIList As Long, szPath As String, wPos As Integer
    BI.hWndOwner = hWnd
    BI.lpszTitle = szDialogTitle
    BI.ulFlags = BIF_RETURNONLYFSDIRS + BIF_DONTGOBELOWDOMAIN
    dwIList = SHBrowseForFolder(BI)
    szPath = Space$(512)
    X = SHGetPathFromIDList(ByVal dwIList, ByVal szPath)
    If X Then
        wPos = InStr(szPath, Chr(0))
        BrowseFolder = Trim(Left$(szPath, wPos - 1))
    Else
        BrowseFolder = vbNullString
    End If
End Function
Public Function CheckIfFolderIsSystem(ByVal FolderName As String) As Boolean
    Dim fs, f, FolderAttribute As Integer
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set f = fs.GetFolder(FolderName)
    FolderAttribute = f.Attributes - FileAttributeDirectory
If FolderAttribute = FileAttributeSystem + FileAttributeHidden _
        Or FolderAttribute = FileAttributeSystem + FileAttributeReadonly _
        Or FolderAttribute = FileAttributeSystem + FileAttributeArchive _
        Or FolderAttribute = FileAttributeSystem + FileAttributeReadonly + FileAttributeHidden _
        Or FolderAttribute = FileAttributeSystem + FileAttributeReadonly + FileAttributeArchive _
        Or FolderAttribute = FileAttributeSystem + FileAttributeHidden + FileAttributeArchive _
        Or FolderAttribute = FileAttributeSystem + FileAttributeHidden + FileAttributeReadonly + FileAttributeArchive _
        Or FolderAttribute = FileAttributeSystem Then
CheckIfFolderIsSystem = True
Else
CheckIfFolderIsSystem = False
End If
End Function
Public Sub setFolderRead(folderspec)
Dim f, fs
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set f = fs.GetFolder(folderspec)
f.Attributes = FileAttributeDirectory + FileAttributeReadonly
End Sub
Public Function IsFolderExists(ByVal FolderName As String) As Boolean
Dim fs
Set fs = CreateObject("Scripting.FileSystemObject")
IsFolderExists = fs.FolderExists(FolderName)
End Function
Public Sub FileAttribHide(ByVal FileName As String)
Dim vResult As Long: On Local Error Resume Next
vResult = SetFileAttributes(FileName, FileAttributeHidden + FileAttributeSystem)
End Sub
Public Function bFileExists(ByVal sFileName As String) As Boolean
On Error Resume Next: Dim I As Integer
I = Len(Dir$(sFileName))
bFileExists = IIf(Err Or I = 0, False, True)
If Trim(sFileName) = vbNullString Then bFileExists = False
End Function


''''' Ö÷Èë¿Ú

Sub Main()
 
 If Command <> "" Then
    argsf = Split(Command, " ")
    For Each arg In argsf
       If Trim(arg) <> "" Then
         'MsgBox (arg)
         FolderName = CStr(argsf(0))
         IconFile = CStr(argsf(1))
         'MsgBox (FolderName + vbCrLf + IconFile)
         Call WritePrivateProfileString(".ShellClassInfo", "IconFile", IconFile, FolderName & "\Desktop.ini")
        Call WritePrivateProfileString(".ShellClassInfo", "IconIndex", "0", FolderName & "\Desktop.ini")
        Call FileAttribHide(FolderName & "\Desktop.ini")
        Call setFolderRead(FolderName)
         Exit For
       End If
    Next
    
    
 End If
 
End Sub
