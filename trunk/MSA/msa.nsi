;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Instalador de MSA
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

# Opciones del instalador
!include "MUI.nsh"
SetCompressor lzma
!define mui_abortwarning

# Versión
!define VERSION "0.4.0"

# Direcciones
!define PYTHON_URL "http://www.python.org/ftp/python/2.5.4/python-2.5.4.msi"
!define NUMPY_URL "http://downloads.sourceforge.net/sourceforge/numpy/numpy-1.3.0-win32-superpack-python2.5.exe"
!define MATPLOTLIB_URL "http://downloads.sourceforge.net/sourceforge/matplotlib/matplotlib-0.98.5.3.win32-py2.5.exe"

# Páginas del instalador
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.TXT"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
;!define MUI_FINISHPAGE_RUN "$SMPROGRAMS\MSA\MSA.lnk"
!insertmacro MUI_PAGE_FINISH
  
# Páginas del desintalador
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH
  
# Idioma
!insertmacro MUI_LANGUAGE "Spanish"

# Configuration General
;Nuestro instalador se llamara si la version fuera la 1.0: MSA-1.0-win32.exe
OutFile MSA-${VERSION}-win32.exe

;Nombre de la aplicación
Name "MSA"
Caption "MSA ${VERSION} para Win32 Setup"
;Icon icono.ico

;Comprobacion de integridad del fichero activada
CRCCheck on
;Estilos visuales del XP activados
XPStyle on

# Declaracion de variables a usar	

Var PATH

;Directorio de instalación por defecto
InstallDir "$PROGRAMFILES\MSA"

; check if the program has already been installed, if so, take this dir
; as install dir
InstallDirRegKey HKLM SOFTWARE\MSA "Install_Dir"
;Mensaje que mostraremos para indicarle al usuario que seleccione un directorio
DirText "Elija un directorio donde instalar la aplicación:"

;En caso de encontrarse los ficheros se sobreescriben
SetOverwrite on
;Optimizamos nuestro paquete en tiempo de compilación, es áltamente recomendable habilitar siempre esta opción
SetDatablockOptimize on
;Habilitamos la compresión de nuestro instalador
SetCompress auto
;Personalizamos el mensaje de desinstalación
UninstallText "Este es el desinstalador de MSA."

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Install settings                                                    ;
; En esta sección añadimos los ficheros que forman nuestra aplicación ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

Section "Programa"
    # Obtiene e instala Python
    Call GetPython

    # Archivos de programa
    SetOutPath $INSTDIR
    File  MSA.py
    File  LICENSE.TXT
    File  README.TXT
    SetOutPath $INSTDIR\msa
    File  msa\*.py
    File  msa\input.csv
    File  msa\input.xls
    SetOutPath $INSTDIR\msa\icons
    File  msa\icons\*.gif
    SetOutPath $INSTDIR\msa\data
    File  msa\data\properties.csv
    SetOutPath $INSTDIR\msa\output
    File  msa\output\style.css
    SetOutPath $INSTDIR

;Hacemos que la instalación se realice para todos los usuarios del sistema
    SetShellVarContext all

    # Creactión de accesos directos
    StrCpy $PATH "MSA"
    CreateDirectory "$SMPROGRAMS\$PATH"
    CreateShortCut "$SMPROGRAMS\$PATH\MSA.lnk" "$INSTDIR\MSA.py"
    CreateShortCut "$SMPROGRAMS\$PATH\Desinstalar.lnk" "$INSTDIR\uninstall.exe"

    # Claves de registro
    WriteRegStr HKLM SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$PATH \
            "DisplayName" "MSA ${VERSION}"
    WriteRegStr HKLM SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$PATH \
            "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteUninstaller "uninstall.exe"
    WriteRegStr HKLM SOFTWARE\$PATH "InstallDir" $INSTDIR
    WriteRegStr HKLM SOFTWARE\$PATH "Version" "${VERSION}"

    ;Exec "explorer $SMPROGRAMS\$PATH\"
    ;ExecShell "" "$INSTDIR\MSA.py"
SectionEnd

Section "Ejemplos"
	SetOutPath $INSTDIR\msa\examples
	File  msa\examples\*.csv
SectionEnd

;;;;;;;;;;;;;;;;;;;;;;
; Uninstall settings ;
;;;;;;;;;;;;;;;;;;;;;;

Section "Uninstall"
	StrCpy $PATH "MSA"
        SetShellVarContext all
	RMDir /r $SMPROGRAMS\$PATH
	RMDir /r $INSTDIR
	DeleteRegKey HKLM SOFTWARE\$PATH
        DeleteRegKey HKLM Software\Microsoft\Windows\CurrentVersion\Uninstall\$PATH
SectionEnd

# Obtención e instalación de Python, Numpy y matplotlib
Function GetPython
    MessageBox MB_OKCANCEL "Se requiere Python, Numpy y matplotlib, si todavía no los ha instalado pulse Aceptar, sino pulse Cancelar." IDOK OK IDCANCEL CANCEL

    OK:
        nsisdl::download /TIMEOUT=30000 ${PYTHON_URL} "$TEMP\Python.msi"
        ExecWait "msiexec.exe /i $TEMP\Python.msi"
        Delete "$TEMP\Python.exe"
        nsisdl::download /TIMEOUT=30000 ${NUMPY_URL} "$TEMP\Numpy.exe"
        ExecWait "$TEMP\Numpy.exe"
        Delete "$TEMP\Numpy.exe"
        nsisdl::download /TIMEOUT=30000 ${MATPLOTLIB_URL} "$TEMP\matplotlib.exe"
        ExecWait "$TEMP\matplotlib.exe"
        Delete "$TEMP\matplotlib.exe"
    CANCEL:
FunctionEnd