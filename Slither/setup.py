import cx_Freeze
import os

executables = [cx_Freeze.Executable('snake.py')]
os.environ['TCL_LIBRARY'] = r'C:\Users\morel\AppData\Local\Programs\Python\Python37\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\morel\AppData\Local\Programs\Python\Python37\tcl\tk8.6'


cx_Freeze.setup(
    name='Slither',
    options={'build_exe':{'packages':['pygame'],
                          'include_files':['red_apple.png', 'snake_head.png', 'snake_icon.png']}},
    description='Slither Game Tutorial',
    executables=executables
)