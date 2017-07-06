import os

os.environ['QT_API'] = 'pyside'
import sys

from pyqode.qt import QtWidgets
from pyqode.python.backend import server
from pyqode.python.widgets import PyCodeEdit

from pyqode.core.widgets import SplittableCodeEditTabWidget

from pyqode.python.panels import QuickDocPanel

# from pyqode.python.modes import
from pyqode.python.panels import SymbolBrowserPanel

from .RunConsole import Console, ConsolePanel


class TabbedEditor(SplittableCodeEditTabWidget):
    def __init__(self, parent=None, root=True, qsettings=None):
        super(TabbedEditor, self).__init__(parent, root, qsettings)
        if parent:
            self.app = parent.app
        else:
            self.app = None
        self.openConsole()  # this must be called on 'Run Script'

    def openConsole(self):
        self.consolePanel = ConsolePanel(self)
        # self.panels.append(self.consolePanel, ConsolePanel.Position.BOTTOM)

    def _create_code_edit(self, mimetype, *args, **kwargs):
        return CodeEditor(self)


class CodeEditor(PyCodeEdit):
    def __init__(self, parent, server_script=server.__file__, interpreter=sys.executable, args=None,
                 create_default_actions=True, color_scheme='monokai', reuse_backend=False):
        super(CodeEditor, self).__init__(parent=parent, server_script=server.__file__, interpreter=sys.executable,
                                         args=None, create_default_actions=True, color_scheme='monokai', reuse_backend=False)
        if parent.app:
            self.app = parent.app
            self.baseParent = parent
        # self.quickDoc = QuickDocPanel()
        # self.quickDoc.action_quick_doc.setShortcut('Ctrl+Q')
        # self.panels.append(self.quickDoc, QuickDocPanel.Position.BOTTOM)
        # self.quickDoc.setVisible(True)

        self.simbols = SymbolBrowserPanel()
        self.panels.append(self.simbols, SymbolBrowserPanel.Position.TOP)

    def clone(self):
        clone = self.__class__(parent=self.baseParent, server_script=self.backend.server_script,
                interpreter=self.backend.interpreter, args=self.backend.args,
                color_scheme=self.syntax_highlighter.color_scheme.name)
        return clone
