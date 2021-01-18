from collections import deque

import psutil
from PyQt5 import QtChart
from PyQt5 import QtCore
from PyQt5 import QtGui

from src.charts.tamplete import TampleteView

KB = 1024


class NetUsageView(TampleteView):
    numDataPonints = 20
    title = 'sockets '

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        if not parent:
            self.setWindowTitle(self.title)

        chart = QtChart.QChart(title=self.title)
        self.setChart(chart)
        self.yRange = 10
        netInfo = psutil.net_io_counters()
        self.lastSent = netInfo.bytes_sent
        self.lastReceived = netInfo.bytes_recv

        xAxis = QtChart.QValueAxis()
        xAxis.setRange(0, self.numDataPonints)
        xAxis.setLabelsVisible(False)
        chart.setAxisX(xAxis)

        yAxis = QtChart.QValueAxis()
        yAxis.setRange(0, self.yRange)
        chart.setAxisY(yAxis)
        self.yAxis = yAxis

        self.sendSplineName = "eviados "
        sentSpline = QtChart.QSplineSeries()
        sentSpline.setName(self.sendSplineName)
        chart.addSeries(sentSpline)
        sentSpline.attachAxis(xAxis)
        sentSpline.attachAxis(yAxis)
        self.sendSpline = sentSpline

        self.reciveSplineName = "recebidos "
        receivedSpline = QtChart.QSplineSeries()
        receivedSpline.setName(self.reciveSplineName)
        chart.addSeries(receivedSpline)
        receivedSpline.attachAxis(xAxis)
        receivedSpline.attachAxis(yAxis)
        self.reciveSpline = receivedSpline

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        chart.setTheme(QtChart.QChart.ChartThemeBlueCerulean)

        self.sentData = deque([0] * self.numDataPonints, maxlen=self.numDataPonints)
        self.receivedData = deque([0] * self.numDataPonints, maxlen=self.numDataPonints)

        self.sendSpline.append([QtCore.QPointF(x, y) for x, y, in enumerate(self.sentData)])
        self.reciveSpline.append([QtCore.QPointF(x, y) for x, y, in enumerate(self.receivedData)])

        self.timer = QtCore.QTimer(interval=1000, timeout=self.upadeData)
        self.timer.start()
        self.show()

    def upadeData(self):
        netInfo = psutil.net_io_counters()
        delta = (netInfo.bytes_sent - self.lastSent) / KB

        self.sentData.append(delta)
        self.sendSpline.replace([QtCore.QPointF(x, y) for x, y in enumerate(self.sentData)])
        if delta > self.yRange:
            self.yRange *= 1.5
            self.yAxis.setRange(0, self.yRange)
        self.sendSpline.setName(self.sendSplineName + '{:.2f}KB/s'.format(delta))

        delta = (netInfo.bytes_recv - self.lastReceived) / KB
        self.receivedData.append(delta)
        self.reciveSpline.replace([QtCore.QPointF(x, y) for x, y in enumerate(self.receivedData)])
        if delta > self.yRange:
            self.yRange *= 1.5
            self.yAxis.setRange(0, self.yRange)
        self.reciveSpline.setName(self.reciveSplineName + '{:.2f}KB/s'.format(delta))

        self.lastSent = netInfo.bytes_sent
        self.lastReceived = netInfo.bytes_recv
        self.chart().setTitle(self.title + f'total recebido->{int(self.lastReceived / (1024 * 1024))}MB,'
                                           f' total enviado->{int(self.lastSent / (1024 * 1024))}MB')

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.parent() and a0.buttons() == QtCore.Qt.LeftButton:
            self.dedicated = NetUsageView()
