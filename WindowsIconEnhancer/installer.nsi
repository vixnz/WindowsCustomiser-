; NSIS Installer Script for Windows Icon Enhancer Pro
; To build: makensis installer.nsi

; Include Modern UI
!include "MUI2.nsh"

; General
Name "Windows Icon Enhancer Pro"
OutFile "releases\WindowsIconEnhancer_Setup.exe"
InstallDir "$PROGRAMFILES\WindowsIconEnhancer"
InstallDirRegKey HKCU "Software\WindowsIconEnhancer" ""

; Request application privileges (for admin operations)
RequestExecutionLevel admin

; MUI Settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "README.md"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

; Installer sections
Section "Install Application"
    SetOutPath "$INSTDIR"
    
    ; Copy executable and files
    File "dist\WindowsIconEnhancer\WindowsIconEnhancer.exe"
    File "README.md"
    File "USER_GUIDE.md"
    File "CONFIG.md"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\Windows Icon Enhancer Pro"
    CreateShortcut "$SMPROGRAMS\Windows Icon Enhancer Pro\Windows Icon Enhancer.lnk" "$INSTDIR\WindowsIconEnhancer.exe"
    CreateShortcut "$SMPROGRAMS\Windows Icon Enhancer Pro\Uninstall.lnk" "$INSTDIR\uninstall.exe"
    CreateShortcut "$DESKTOP\Windows Icon Enhancer.lnk" "$INSTDIR\WindowsIconEnhancer.exe"
    
    ; Write registry
    WriteRegStr HKCU "Software\WindowsIconEnhancer" "" "$INSTDIR"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsIconEnhancer" "DisplayName" "Windows Icon Enhancer Pro"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsIconEnhancer" "DisplayVersion" "1.0.0"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsIconEnhancer" "UninstallString" "$INSTDIR\uninstall.exe"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

; Uninstaller
Section "Uninstall"
    ; Remove files
    Delete "$INSTDIR\WindowsIconEnhancer.exe"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\USER_GUIDE.md"
    Delete "$INSTDIR\CONFIG.md"
    Delete "$INSTDIR\uninstall.exe"
    
    ; Remove shortcuts
    Delete "$SMPROGRAMS\Windows Icon Enhancer Pro\Windows Icon Enhancer.lnk"
    Delete "$SMPROGRAMS\Windows Icon Enhancer Pro\Uninstall.lnk"
    Delete "$DESKTOP\Windows Icon Enhancer.lnk"
    RMDir "$SMPROGRAMS\Windows Icon Enhancer Pro"
    
    ; Remove registry
    DeleteRegKey HKCU "Software\WindowsIconEnhancer"
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsIconEnhancer"
    
    ; Remove directory
    RMDir "$INSTDIR"
SectionEnd
