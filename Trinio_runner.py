from tred.MainUI import MainUI
import sys

from PySide.QtGui import QApplication
from PySide.QtCore import Qt

uifile = './tred/ui_files/main.ui'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainUI(uifile, app, None)
    main.show()
    exit(app.exec_())
