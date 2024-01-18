import sys
import webbrowser
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,QMessageBox
from PyQt6.QtGui import QFont, QPixmap, QColor  # Import QColor here
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from multiprocessing import Process
import os

from visual import PokerVisualizationApp
from data import setup_ui
from calculator import EmissionCalculator
class CommonLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(900, 600) 
        # Set background image using QLabel
        self.background = QLabel(self)
        pixmap = QPixmap('cod1.png')  
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        self.background.resize(self.width(), self.height())  
        
        self.layout = QVBoxLayout(self.background)  # Set the layout on the background label
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)

        #  UI elements on top of the background
        self.setupUIElements()

        self.setWindowTitle("ECOVIS")
        self.show()

    def setupUIElements(self):
  
        heading = QLabel("ECOVIS", self)
        heading.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet("color: Green;")
        heading.resize(500, 70)  
        heading.move(190, 1)  

      
        pokerButton = self.createStyledButton("Visualize Poker Layout", self.launchPokerVisualizationApp, "#808080")
        pokerButton.resize(300, 60)
        pokerButton.move(100, 200)

        carbonButton = self.createStyledButton("Estimate Carbon Emission", self.launchTkinterApp, "#808080")  # Grey
        carbonButton.resize(300, 60)
        carbonButton.move(550, 200)

        
        emissionCalculatorButton = self.createStyledButton("Calculate CO2 Impact", self.launchEmissionCalculator, "#4CAF50")  # Green
        emissionCalculatorButton.resize(300, 60)
        emissionCalculatorButton.move(330, 350)

        knowMoreButton = self.createStyledButton("Know More", self.showAppInfo, "#FF0000")
        knowMoreButton.setFixedWidth(150)
        knowMoreButton.move(50, 550)


    def createStyledButton(self, text, callback, color):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 10px;
                padding: 10px 15px;
                font-size: 16px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.lightenColor(color)};
            }}
        """)
        return button
    
    @staticmethod
    def lightenColor(color, amount=0.2):
       
        import colorsys
        try:
            r, g, b, a = QColor(color).getRgbF()
            h, l, s = colorsys.rgb_to_hls(r, g, b)
            l = min(1, l + amount)
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return f'rgba({int(r * 255)}, {int(g * 255)}, {int(b * 255)}, {a})'
        except ValueError:
            return color

    def launchPokerVisualizationApp(self):
  
        self.pokerVisualizationApp = PokerVisualizationApp()
        self.pokerVisualizationApp.show()
    def launchTkinterApp(self):
     
        self.tkinterProcess = Process(target=setup_ui)
        self.tkinterProcess.start()

    def launchEmissionCalculator(self):
        # Instantiate and show the EmissionCalculator window
        self.emissionCalculatorApp = EmissionCalculator()
        self.emissionCalculatorApp.show()
        
    def showAppInfo(self):
        QMessageBox.information(self, "About ECOVIS", 
            "ECOVIS is an application designed to visualize the Poker Hands dataset using various layout algorithms. "
            "It allows users to analyze the impact of these algorithms on the dataset and assess the carbon emissions "
            "associated with computational tasks. Users can explore different algorithms, visualize data layouts, "
            "and calculate the environmental impact of data processing.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = CommonLauncher()
    sys.exit(app.exec())
