from cx_Freeze import setup, Executable
 
buildOptions = dict(packages = [], excludes = [])
 
import sys
base = 'Win32GUI' if sys.platform=='win32' else None
 
executables = [
    Executable('Controller.py', base=base, icon='icon.ico')
]
 
setup(
    name='TejasThermal',
    version = '1.0.1',
    description = 'GUI to configure distillation process.',
    options = dict(build_exe = buildOptions),
    executables = executables
)