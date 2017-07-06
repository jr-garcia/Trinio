from .loader import MainWindow

from ._do_import import resolve_import

resolve_import()
from e3d import Engine
from e3d.backends import OGL3Backend
from e3d.gui import Panel

from PySide import QtGui
from PySide.QtCore import Qt

from cycgkit.cgtypes import vec3

from .view3D import View, ViewSides
from .codeEdit import CodeEditor, TabbedEditor, ConsolePanel


class MainUI(MainWindow):
    def __init__(self, file, app, parent):
        super(MainUI, self).__init__(file, parent)
        self.app = app
        self.engine = None
        self.backend = OGL3Backend
        self.scene_3d = None
        self.codeEdit = self.createEditor()
        self.console = ConsolePanel(self)
        self.views = []

        self.prepareEngine()
        self.replaceViews()
        self.replaceEditor()
        self.replaceConsole()
        self.timer = self.startTimer(1000 / 30)

    def createEditor(self):
        editor = TabbedEditor(self)

        editor.setMinimumSize(200, 200)
        editor.show()
        editor.create_new_document('untitled_', '.py')

        return editor

    def replaceEditor(self):
        self.textEdit.setParent(None)
        self.textEdit.deleteLater()
        self.splitter_editor.insertWidget(0, self.codeEdit)

    def replaceConsole(self):
        self.console_placeholder.setParent(None)
        self.console_placeholder.deleteLater()
        self.splitter_editor.insertWidget(1, self.console)

    def replaceViews(self):
        for i in range(1, 5):
            gv = self.findChild(QtGui.QGraphicsView, 'graphicsView_' + str(i))
            gv.setParent(None)
            gv.deleteLater()

        self.splitter_top.insertWidget(0, self.views[0])
        self.splitter_top.insertWidget(1, self.views[1])
        self.splitter_bottom.insertWidget(0, self.views[2])
        self.splitter_bottom.insertWidget(1, self.views[3])

        for v in self.views:
            v.show()

    def prepareEngine(self):
        self.engine = Engine(self.backend, None, useQT=True)
        engine = self.engine
        engine.initialize()

        try:
            self.views.append(View(engine, 'top', ViewSides.top))
            self.views.append(View(engine, 'left', ViewSides.left))
            self.views.append(View(engine, 'front', ViewSides.front))
            self.views.append(View(engine, 'perspective', ViewSides.perspective))
        except Exception as ex:
            print('error in main.prepareEngine: '.format(str(ex)))
            self.close()
            raise

        self.scene_3d = engine.scenes.addScene('scene_3d')
        self.scene_3d.ambientColor = vec3(.04, .06, .09)

        engine.scenes.setCurrentSceneID('scene_3d')
        engine.models.loadBox("boxmodel", [2], 2)
        self.box1 = self.scene_3d.addModel('boxmodel', 'box1', [0, 0, 0], [0, 0, 0], 1)

        self.addLights()

        engine.models.loadPlane("floorplane", 500, 500, 6)
        self.floor = self.scene_3d.addModel('floorplane', 'floor', [0, -10, 0], [0, 0, 0], 1)
        mt = self.floor._materials[0]
        mt.specularPower = 50
        mt.useDiffuseTexture = True
        mt.setDefaultNormalMap()
        mt.textureRepeat = 80

    def timerEvent(self, *args, **kwargs):
        if self.tab_scenes.isVisible():
            for v in self.views:
                v.update3d()
        # elif self.tab_code.isVisible():
        #     self.codeEdit.openConsole()

    def addLights(self):
        self.dlight = self.scene_3d.addLight(0, vec3(100000.0, 10000.0, 100000.0), vec3(45, 45, 0))
        self.dlight.color = vec3(.9, .9, 0.7)

    def closeEvent(self, *args, **kwargs):
        if self.timer:
            self.killTimer(self.timer)
        self.engine.terminate()
