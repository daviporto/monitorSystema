from collections import deque

import psutil
from PyQt5 import QtChart
from PyQt5 import QtCore
from PyQt5 import QtGui

from src.charts.tamplete import TampleteView

MB = 1024 * 1024


class DiskUsageView(TampleteView):
    numDataPonints = 20
    title = 'uso de disco '

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        chart = QtChart.QChart(title=self.title)
        if not parent:
            self.setWindowTitle(self.title)

        self.setChart(chart)
        self.yRange = 20
        diskInfo = psutil.disk_io_counters()
        self.lastRead = diskInfo.read_bytes
        self.lastWrite = diskInfo.write_bytes

        xAxis = QtChart.QValueAxis()
        xAxis.setRange(0, self.numDataPonints)
        xAxis.setLabelsVisible(False)
        chart.setAxisX(xAxis)

        yAxis = QtChart.QValueAxis()
        yAxis.setRange(0, self.yRange)
        chart.setAxisY(yAxis)
        self.yAxis = yAxis

        writeSpline = QtChart.QSplineSeries()
        self.WriteSplineName = "write(MB) "
        writeSpline.setName(self.WriteSplineName)
        chart.addSeries(writeSpline)
        writeSpline.attachAxis(xAxis)
        writeSpline.attachAxis(yAxis)
        self.writeSpline = writeSpline

        readSpline = QtChart.QSplineSeries()
        self.readSplineName = "read(MB) "
        readSpline.setName(self.readSplineName)
        chart.addSeries(readSpline)
        readSpline.attachAxis(xAxis)
        readSpline.attachAxis(yAxis)
        self.readSpline = readSpline

        chart.setTheme(QtChart.QChart.ChartThemeBlueCerulean)

        self.writeData = deque([0] * self.numDataPonints, maxlen=self.numDataPonints)
        self.readData = deque([0] * self.numDataPonints, maxlen=self.numDataPonints)

        self.writeSpline.append([QtCore.QPoint(x, y) for x, y, in enumerate(self.writeData)])
        self.readSpline.append([QtCore.QPoint(x, y) for x, y, in enumerate(self.readData)])

        self.timer = QtCore.QTimer(interval=1000, timeout=self.upadeData)
        self.timer.start()
        self.show()

    def upadeData(self):
        diskInfo = psutil.disk_io_counters()
        delta = (diskInfo.write_bytes - self.lastWrite) // MB

        self.writeData.append(delta)
        self.writeSpline.replace([QtCore.QPoint(x, y) for x, y in enumerate(self.writeData)])
        if delta > self.yRange:
            self.yRange *= 1.5
            self.yAxis.setRange(0, self.yRange)
        self.writeSpline.setName(self.WriteSplineName + '{:.2f}MB/S'.format(delta))

        delta = (diskInfo.read_bytes - self.lastRead) // MB
        self.readData.append(delta)
        self.readSpline.replace([QtCore.QPoint(x, y) for x, y in enumerate(self.readData)])
        if delta > self.yRange:
            self.yRange *= 1.5
            self.yAxis.setRange(0, self.yRange)
        self.readSpline.setName(self.readSplineName + '{:.2f}MB/S'.format(delta))

        self.lastRead = diskInfo.read_bytes
        self.lastWrite = diskInfo.write_bytes
        self.chart().setTitle(self.title + f'total lido->{int(self.lastRead / MB)}MB,'
                                           f' total escrito->{int(self.lastRead / MB)}MB')

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.parent() and a0.buttons() == QtCore.Qt.LeftButton:
            self.dedicated = DiskUsageView()
