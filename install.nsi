!include "MUI2.nsh"

;--------------------------------
; Window Title
Caption "PyForge Setup"
Name "PyForge"

;--------------------------------
; Set welcome text and logo
; !define MUI_WELCOMEPAGE_TITLE $(WELCOME_TITLE)
; !define MUI_WELCOMEPAGE_TEXT $(WELCOME_TEXT)
; !define MUI_WELCOMEFINISHPAGE_BITMAP "installer_logo.bmp"

;--------------------------------
; Installer UI
!insertmacro MUI_PAGE_WELCOME
; !insertmacro MUI_PAGE_LICENSE "license.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
; Languages
!insertmacro MUI_LANGUAGE "English"
; LangString WELCOME_TITLE ${LANG_ENGLISH} "Welcome to the PyForge Setup"
; LangString WELCOME_TEXT ${LANG_ENGLISH} "This wizard will guide you through the installation of PyForge.$\r$\n$\r$\nClick Next to continue."

;--------------------------------
; Installer Info
RequestExecutionLevel admin
OutFile "pyforge-setup.exe"
InstallDir $PROGRAMFILES\PyForge

;--------------------------------
; Sections

Section "Core Files" SEC01
  SectionIn RO  ; always selected

  SetOutPath $INSTDIR\deps
  SetOverwrite off
  File /r .\deps\*.*

  SetOutPath $INSTDIR
  SetOverwrite on
  File /r .\.build\dist\pyforge\*.*  ; created by pyinstaller
  File .\manifest.json
SectionEnd

Section "Readme" SEC02
  SetOutPath $INSTDIR
  SetOverwrite on
  File .\README.md
SectionEnd

;--------------------------------
; Write Uninstaller

Section -PostInstall
  WriteUninstaller $INSTDIR\uninstall.exe
SectionEnd

Section "Uninstall"
  RMDir /r $INSTDIR
SectionEnd

;--------------------------------
; Section Descriptions

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC01} "Installs the PyForge core application and dependencies"
  !insertmacro MUI_DESCRIPTION_TEXT ${SEC02} "Installs README.md"
!insertmacro MUI_FUNCTION_DESCRIPTION_END
