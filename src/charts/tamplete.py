from PyQt5 import QtChart
from PyQt5 import QtCore
from PyQt5 import QtGui


class TampleteView(QtChart.QChartView):

    def __init__(self, parent):
        """MainWindow constructor"""
        super().__init__(parent=parent)
        self.lastMousePosition = None
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.dedicated = None

    def keyPressEvent(self, event):
        keymap = {
            QtCore.Qt.Key_Up: lambda: self.chart().scroll(0, -10),
            QtCore.Qt.Key_Down: lambda: self.chart().scroll(0, 10),
            QtCore.Qt.Key_Right: lambda: self.chart().scroll(-10, 0),
            QtCore.Qt.Key_Left: lambda: self.chart().scroll(10, 0),
            QtCore.Qt.Key_Shift: self.chart().zoomIn,
            QtCore.Qt.Key_Control: self.chart().zoomOut,
        }
        callback = keymap.get(event.key())
        if callback:
            callback()

    def wheelEvent(self, QWheelEvent):
        if QWheelEvent.angleDelta().y() > 0:
            self.chart().zoomIn()
        else:
            self.chart().zoomOut()

    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == QtCore.Qt.LeftButton:
            if self.lastMousePosition:
                delta = QMouseEvent.globalPos() - self.lastMousePosition
                self.chart().scroll(-delta.x(), delta.y())
                self.lastMousePosition = QMouseEvent.globalPos()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == QtCore.Qt.LeftButton:
            self.lastMousePosition = QMouseEvent.globalPos()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == QtCore.Qt.LeftButton:
            self.lastMousePosition = None

