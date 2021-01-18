from collections import deque

from PyQt5 import QtChart
from PyQt5 import QtCore
from PyQt5 import QtGui

from src.charts.tamplete import TampleteView


class TampleteSingleProcess(TampleteView):

    def __init__(self, parent, seriesName, yRange=20, firstValue=0, num_data_points=500):
        super().__init__(parent=parent)
        if not parent:
            self.setWindowTitle(seriesName)

        self.seriesName = seriesName + ' '
        self.lastMousePosition = None
        self.num_data_points = num_data_points
        self.max = self.min = self.average = firstValue
        chart = QtChart.QChart()
        self.setChart(chart)
        self.series = QtChart.QSplineSeries(name=seriesName)
        chart.addSeries(self.series)

        self.data = deque(
            [0] * self.num_data_points, maxlen=self.num_data_points)
        self.series.append([
            QtCore.QPoint(x, y)
            for x, y in enumerate(self.data)
        ])

        x_axis = QtChart.QValueAxis()
        x_axis.setRange(0, self.num_data_points)
        x_axis.setLabelsVisible(False)
        y_axis = QtChart.QValueAxis()
        self.maxY = yRange
        y_axis.setRange(0, self.maxY)
        self.y_axis = y_axis
        chart.setAxisX(x_axis, self.series)
        chart.setAxisY(y_axis, self.series)
        chart.setTheme(QtChart.QChart.ChartThemeBlueCerulean)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.show()

    def refresh_stats(self, newValue):
        if newValue > self.maxY:
            self.maxY = newValue + 10
            self.y_axis.setRange(0, self.maxY)

        if newValue > self.max:
            self.max = newValue
        elif newValue < self.min:
            self.min = newValue
        self.average += newValue
        self.average /= 2

        self.data.append(newValue)
        new_data = [
            QtCore.QPoint(x, y)
            for x, y in enumerate(self.data)]
        self.series.replace(new_data)
        self.series.setName(self.seriesName + str(newValue))

        if self.dedicated:
            self.dedicated.refresh_stats(newValue)

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.parent() and a0.buttons() == QtCore.Qt.LeftButton:
            self.dedicated = TampleteSingleProcess(parent=None,
                                                   seriesName=self.seriesName)
