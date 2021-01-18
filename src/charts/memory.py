from collections import deque

import psutil
from PyQt5 import QtChart
from PyQt5 import QtCore
from PyQt5 import QtGui

from src.charts.tamplete import TampleteView

GB = 1024 * 1024 * 1024


class MemoryUsageView(TampleteView):
    numDataPonints = 500
    title = "uso de memória(%)"
    min = max = average = 0
    swap = {
        'min': 0,
        'max': 0,
        'average': 0
    }
    memory = {
        'min': 0,
        'max': 0,
        'average': 0
    }

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        if not parent:
            self.setWindowTitle(self.title)

        chart = QtChart.QChart(title=self.title)
        self.setChart(chart)
        self.memoryName = "memória "
        self.freeMemoryName = "memoria livre "
        self.swapAreaName = 'area de swap '

        xAxis = QtChart.QValueAxis()
        xAxis.setRange(0, self.numDataPonints)
        xAxis.setLabelsVisible(False)
        chart.setAxisX(xAxis)

        yAxis = QtChart.QValueAxis()
        memory = psutil.virtual_memory()
        self.memory['average'] = memory.total - memory.available
        yAxis.setRange(0, 100)
        chart.setAxisY(yAxis)

        fisicalMemorySpline = QtChart.QSplineSeries()
        fisicalMemorySpline.setName(self.memoryName)
        chart.addSeries(fisicalMemorySpline)
        fisicalMemorySpline.attachAxis(xAxis)
        fisicalMemorySpline.attachAxis(yAxis)
        self.fisicalMemorySpline = fisicalMemorySpline

        freeMemorySpline = QtChart.QSplineSeries()
        freeMemorySpline.setName(self.freeMemoryName)
        chart.addSeries(freeMemorySpline)
        freeMemorySpline.attachAxis(xAxis)
        freeMemorySpline.attachAxis(yAxis)
        self.freeMemorySpline = freeMemorySpline

        swapMemorySpline = QtChart.QSplineSeries()
        swapMemorySpline.setName(self.swapAreaName)
        chart.addSeries(swapMemorySpline)
        swapMemorySpline.attachAxis(xAxis)
        swapMemorySpline.attachAxis(yAxis)
        self.swapMemorySpline = swapMemorySpline

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        chart.setTheme(QtChart.QChart.ChartThemeBlueCerulean)

        self.memoryData = deque([int(psutil.virtual_memory().percent)] * self.numDataPonints,
                                maxlen=self.numDataPonints)
        self.swapData = deque([int(psutil.swap_memory().percent)] * self.numDataPonints, maxlen=self.numDataPonints)
        self.freeMemoryData = deque([100 - int(psutil.virtual_memory().percent)] * self.numDataPonints,
                                    maxlen=self.numDataPonints)

        self.fisicalMemorySpline.append([QtCore.QPoint(x, y) for x, y, in enumerate(self.memoryData)])
        self.swapMemorySpline.append([QtCore.QPoint(x, y) for x, y, in enumerate(self.swapData)])
        self.freeMemorySpline.append([QtCore.QPoint(x, y) for x, y, in enumerate(self.freeMemoryData)])

        self.timer = QtCore.QTimer(interval=200, timeout=self.upadeData)
        self.timer.start()
        self.show()

    def upadeData(self):
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        self.memoryData.append(int(memory.percent))
        self.fisicalMemorySpline.replace([QtCore.QPoint(x, y) for x, y in enumerate(self.memoryData)])
        self.fisicalMemorySpline.setName(self.memoryName + '{:.2f}MB'.format(memory.used / (1024 * 1024)))

        self.swapData.append(int(swap.percent))
        self.swapMemorySpline.replace([QtCore.QPoint(x, y) for x, y in enumerate(self.swapData)])
        self.swapMemorySpline.setName(self.swapAreaName + '{:.2f}MB'.format(swap.used / (1024 * 1024)))

        self.freeMemoryData.append(int(100 - memory.percent))
        self.freeMemorySpline.replace([QtCore.QPoint(x, y) for x, y in enumerate(self.freeMemoryData)])
        self.freeMemorySpline.setName(self.freeMemoryName + '{:.2f}MB'.format((memory.free / (1024 * 1024))))

        # used = memory.total - memory.available
        # if used < self.memory['min']:
        #     self.min = min
        # elif used > self.memory['max']:
        #     self.max = max
        # self.memory['average'] += used
        # self.memory['average'] /= 2
        #
        # used = swap.total - swap.free
        # if used < self.swap['min']:
        #     self.min = min
        # elif used > self.swap['max']:
        #     self.max = max
        # self.swap['average'] += used
        # self.swap['average'] /= 2

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.parent() and a0.buttons() == QtCore.Qt.LeftButton:
            self.dedicated = MemoryUsageView()
