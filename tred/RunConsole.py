import os
import sys
from pyqode.core.api import TextHelper
from pyqode.qt import QtWidgets
from pyqode.core.widgets import output_window, OutputWindow
from pyqode.core.widgets.output_window import OutputFormatter
from pyqode.python.widgets import PyConsole
from pyqode.python.backend import server
from pyqode.qt import QtCore, QtWidgets
from pyqode.core.api import Panel
from pyqode.core import icons


editor_windows = []


class Console(PyConsole):
    def __init__(self, parent):
        self.parent = parent
        # original __init__
        interpreter = sys.executable
        backend = server.__file__
        color_scheme = 'vim'
        self._pygment_color_scheme = color_scheme
        super(PyConsole, self).__init__(parent=parent, input_handler=output_window.BufferedInputHandler(),
                                        backend=backend, color_scheme=self.SolarizedColorScheme)
        self.start_process(interpreter.replace('pythonw', 'python'), arguments=['-i'], print_command=False,
                           use_pseudo_terminal=True)


class ConsolePanel(Panel):
    def __init__(self, parent):
        if parent.app:
            QtWidgets.qApp = parent.app
            output_window.qApp = parent.app

        super(ConsolePanel, self).__init__(dynamic=True)
        # layouts
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        child_layout = QtWidgets.QVBoxLayout()

        # A QTextEdit to show the doc
        self.text_edit = Console(self)
        # self.text_edit.setReadOnly(True)
        # self.text_edit.setAcceptRichText(True)
        layout.addWidget(self.text_edit)

        # A QPushButton (inside a child layout for a better alignment)
        # to close the panel
        self.bt_close = QtWidgets.QPushButton()
        self.bt_close.setIcon(icons.icon('window-close', ':/pyqode-icons/rc/close.png', 'fa.close'))
        self.bt_close.setIconSize(QtCore.QSize(16, 16))
        self.bt_close.clicked.connect(self.hide)
        child_layout.addWidget(self.bt_close)
        child_layout.addStretch()
        layout.addLayout(child_layout)

        # Action
        self.action_quick_doc = QtWidgets.QAction(_('Show documentation'), self)
        self.action_quick_doc.setShortcut('Alt+Q')
        icon = icons.icon(qta_name='fa.book')
        if icon:
            self.action_quick_doc.setIcon(icon)

        self.action_quick_doc.triggered.connect(self._on_action_quick_doc_triggered)

    def _on_action_quick_doc_triggered(self):
        tc = TextHelper(self.editor).word_under_cursor(select_whole_word=True)
        request_data = {'code': self.editor.toPlainText(), 'line': tc.blockNumber(), 'column': tc.columnNumber(),
            'path'            : self.editor.file.path, 'encoding': self.editor.file.encoding}
        self.editor.backend.send_request(quick_doc, request_data, on_receive=self._on_results_available)
