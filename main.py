import sys
from PyQt5 import QtWidgets

from SimulationDiffusion import SimulationDiffusion

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SimulationDiffusion()
    app.exec_()
