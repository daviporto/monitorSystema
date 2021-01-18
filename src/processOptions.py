import psutil
from PyQt5 import QtWidgets


class ProcessOptions(QtWidgets.QWidget):
    def __init__(self, pid, position=None, parent=None):
        super(ProcessOptions, self).__init__(parent=parent)
        self.pid = pid
        if position:
            self.move(position)
        buttonKill = QtWidgets.QPushButton(self, text='Matar processo')
        buttonKillTree = QtWidgets.QPushButton(self, text='Matar arvore processo')
        buttonTerminar = QtWidgets.QPushButton(self, text='terminar processo')
        buttonSuspender = QtWidgets.QPushButton(self, text='suspender processo')
        buttonResumir = QtWidgets.QPushButton(self, text='resumir processo')

        buttonKill.clicked.connect(self.kill)
        buttonKillTree.clicked.connect(self.killTree)
        buttonTerminar.clicked.connect(self.terminar)
        buttonSuspender.clicked.connect(self.suspender)
        buttonResumir.clicked.connect(self.resumir)

        VboxLayout = QtWidgets.QVBoxLayout(self)
        VboxLayout.addWidget(buttonKill)
        VboxLayout.addWidget(buttonKillTree)
        VboxLayout.addWidget(buttonTerminar)
        VboxLayout.addWidget(buttonSuspender)
        VboxLayout.addWidget(buttonResumir)
        self.show()

    def kill(self):
        try:
            p = psutil.Process(self.pid)
            p.kill()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'erro', str(e))

    def killTree(self):
        parent = psutil.Process(self.pid)
        children = parent.children(recursive=True)
        for p in children:
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, title='erro', text=str(e))

        try:
            parent.kill()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'erro', str(e))

    def terminar(self):
        try:
            p = psutil.Process(self.pid)
            p.terminate
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'erro', str(e))

    def suspender(self):
        try:
            p = psutil.Process(self.pid)
            p.suspend()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'erro', str(e))

    def resumir(self):
        try:
            p = psutil.Process(self.pid)
            p.resume
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'erro', str(e))
