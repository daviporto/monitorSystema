from collections import deque

import psutil
from PyQt5 import QtChart
from PyQt5 import QtCore
from PyQt5 import QtGui

from src.charts.tamplete import TampleteView


class CPUUsageView(TampleteView):
    num_data_points = 500
    chart_title = "ultilização do cpu "

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.max = self.min = 0
        if not parent:
            self.setWindowTitle(self.title)

        chart = QtChart.QChart(title=self.chart_title)
        self.setChart(chart)
        self.chart().setTitle(self.chart_title + f"min-> {self.min}, max-> {self.max}")
        self.seriesName = "ultilização  "
        self.series = QtChart.QSplineSeries(name=self.seriesName)
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
        y_axis.setRange(0, 100)
        chart.setAxisX(x_axis, self.series)
        chart.setAxisY(y_axis, self.series)
        chart.setTheme(QtChart.QChart.ChartThemeBlueCerulean)

        self.timer = QtCore.QTimer(
            interval=200, timeout=self.refresh_stats)
        self.timer.start()
        self.show()

    def refresh_stats(self):
        usage = psutil.cpu_percent()
        self.data.append(usage)
        new_data = [
            QtCore.QPoint(x, y)
            for x, y in enumerate(self.data)]
        self.series.replace(new_data)

        self.series.setName(self.seriesName + int(usage).__str__() + "%")
        if usage < self.min:
            self.min = usage
            self.chart().setTitle(self.chart_title + f"min-> {self.min}, max-> {self.max}")
        elif usage > self.max:
            self.max = usage
            self.chart().setTitle(self.chart_title + f"min-> {self.min}, max-> {self.max}")

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.parent() and a0.buttons() == QtCore.Qt.LeftButton:
            self.dedicated = CPUUsageView()
