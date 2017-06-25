from PySide.QtGui import *
from PySide.QtCore import QObject, QEvent
from PySide.QtOpenGL import QGLWidget

from e3d.cameras import SimpleCamera
from e3d.window.qt_window import e3DGLWidget
from e3d.gui import Layer, Label

from ._defaultValues import *


class ViewSides:
    top = 'top'
    left = 'left'
    front = 'front'
    perspective = 'perspective'


class View(QFrame):
    def __init__(self, engine, name, side=ViewSides.perspective):
        super(View, self).__init__()
        self.name = name
        try:
            self.e3dWindow = engine.createQTWidget(name + ' 3D view', 'Trinio Editor')
        except Exception as ex:
            raise
        assert isinstance(self.e3dWindow, e3DGLWidget)
        mainLayout = QHBoxLayout()
        self.engine = engine
        self.setLayout(mainLayout)
        self.layout().addWidget(self.e3dWindow)
        self.camera = SimpleCamera(rotation=cameraRot, ID=name)
        if side == ViewSides.top:
            self.camera.moveUp(initialViewDist)
            self.camera.rotateX(90)
        elif side == ViewSides.front:
            self.camera.moveBackward(initialViewDist)
        elif side == ViewSides.left:
            self.camera.moveLeft(initialViewDist)
            self.camera.rotateY(-90)
        else:
            self.camera.rotateY(45)
            self.camera.rotateX(20)
            self.camera.position = cameraPos

        self.eFilter = e3dEventFilter(self.resizeEvent)
        self.e3dWindow.installEventFilter(self.eFilter)
        self.e3dWindow.show()

        self.nameLayer = self.e3dWindow.gui.addLayer(name + '_view')
        size = [.5, .07]
        position = [0, 1 - size[1]]
        self.nameLabel = Label(position, size, name, parent=self.nameLayer, fontColor=[1,1,0,1], borderSize=0)

    def __repr__(self):
        return self.name

    def update3d(self):
        self._setCamera()
        self.e3dWindow.update()

    def _setCamera(self):
        self.engine.scenes.currentScene.currentCamera = self.camera

    def resizeEvent(self, *args, **kwargs):
        self._setCamera()
        super(View, self).resizeEvent(*args, ** kwargs)

    def repaint(self, *args, **kwargs):
        self.update3d()
        super(View, self).repaint(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.update3d()
        super(View, self).update(*args, **kwargs)


class e3dEventFilter(QObject):
    def __init__(self, resizeFunc):
        super(e3dEventFilter, self).__init__()
        self.resizeFunc = resizeFunc

    def eventFilter(self, *args, **kwargs):
        if args[1].type() == QEvent.Resize:
            self.resizeFunc(None)
        if args[1].type() == QEvent.Paint:
            self.resizeFunc(None)

        return QObject.eventFilter(self, args[0], args[1])




