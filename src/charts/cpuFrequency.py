from collections import deque

import psutil
from PyQt5 import QtChart
from PyQt5 import QtCore
from PyQt5 import QtGui

from src.charts.tamplete import TampleteView


class CPUFrequencyView(TampleteView):
    numDataPonints = 500
    title = "frequência"
    min = max = average = 0

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.lastMousePosition = None

        if not parent:
            self.setWindowTitle(self.title)
        chart = QtChart.QChart(title=self.title)
        self.setChart(chart)
        self.seriesName = 'Frequency'
        self.series = QtChart.QSplineSeries(name=self.seriesName)
        chart.addSeries(self.series)

        self.data = deque([0] * self.numDataPonints, maxlen=self.numDataPonints)
        self.series.append([QtCore.QPoint(x, y) for x, y, in enumerate(self.data)])

        xAxis = QtChart.QValueAxis()
        xAxis.setRange(0, self.numDataPonints)
        xAxis.setLabelsVisible(False)
        chart.setAxisX(xAxis, self.series)
        yAxis = QtChart.QValueAxis()
        current, min, max = psutil.cpu_freq()
        self.chart().setTitle(self.title + f" min->{min}, max->{max}")
        self.average = current
        yAxis.setRange(0, max)
        chart.setAxisY(yAxis, self.series)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        chart.setTheme(QtChart.QChart.ChartThemeBlueCerulean)

        self.timer = QtCore.QTimer(interval=200, timeout=self.updateFrequency)
        self.timer.start()
        self.show()

    def updateFrequency(self):
        current, min, max = psutil.cpu_freq()

        self.data.append(int(current))
        newStuff = [QtCore.QPoint(x, y) for x, y, in enumerate(self.data)]
        self.series.replace(newStuff)
        self.series.setName(self.seriesName + " " + int(current).__str__() + "Mhz")
        if min < self.min:
            self.min = min
            self.chart().setTitle(self.title + f" min->{min}, max->{max}")
        if max > self.max:
            self.max = max
            self.chart().setTitle(self.title + f" min->{min}, max->{max}")

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.parent() and a0.buttons() == QtCore.Qt.LeftButton:
            self.dedicated = CPUFrequencyView()
