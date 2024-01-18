import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup, QHBoxLayout, QGroupBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

class EmissionCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font: 12pt "Arial";
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                border: 1px solid #bfbfbf;
                border-radius: 5px;
                padding: 5px;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px;
                font: bold 12pt "Arial";
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QRadioButton {
                font: 10pt "Arial";
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        layout.addWidget(QLabel("Enter Carbon Intensity in (kg):"))
        self.carbonIntensityInput = QLineEdit(self)
        layout.addWidget(self.carbonIntensityInput)

       
        self.applianceGroup = QGroupBox("Select a co2 equivalency:")
        mainApplianceLayout = QHBoxLayout()  # Main horizontal layout

        # Tech appliances layout
        techApplianceLayout = QVBoxLayout()
        # Nature-related metrics layout
        natureApplianceLayout = QVBoxLayout()

        self.applianceButtons = QButtonGroup(self)

        # Tech appliances
        techAppliances = [
            ("Smartphone Charger", "smartphone_charger_image.jpg"),
            ("LED Light Bulb", "bulb_image.jpg"),
            ("Television", "television_image.JFIF"),
        ]

        for i, (name, imagePath) in enumerate(techAppliances):
            button = QRadioButton(name)
            pixmap = QPixmap(imagePath)
            scaled_pixmap = pixmap.scaled(QSize(256, 256), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            button.setIcon(QIcon(scaled_pixmap))
            button.setIconSize(QSize(256, 256))
            self.applianceButtons.addButton(button, i)
            techApplianceLayout.addWidget(button)

        # Nature-related metrics
        natureAppliances = [
            ("Human Breathing", "human_breathing_image.png"),
            ("Ice Cap Melting", "melting_image.JFIF"),
            ("Deforestation", "deforestation_image.jpg"),
        ]

        for i, (name, imagePath) in enumerate(natureAppliances, start=len(techAppliances)):
            button = QRadioButton(name)
            pixmap = QPixmap(imagePath)
            scaled_pixmap = pixmap.scaled(QSize(256, 256), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            button.setIcon(QIcon(scaled_pixmap))
            button.setIconSize(QSize(256, 256))
            self.applianceButtons.addButton(button, i)
            natureApplianceLayout.addWidget(button)

        mainApplianceLayout.addLayout(techApplianceLayout)
        mainApplianceLayout.addLayout(natureApplianceLayout)
        self.applianceGroup.setLayout(mainApplianceLayout)
        layout.addWidget(self.applianceGroup)

        self.calcButton = QPushButton("Calculate", self)
        self.calcButton.clicked.connect(self.performCalculation)
        layout.addWidget(self.calcButton)

        self.resultLabel = QLabel("")
        layout.addWidget(self.resultLabel)

        self.setLayout(layout)
        self.setWindowTitle('Emission Impact Calculator')
        self.setFixedSize(1000, 800)

    def showEvent(self, event):
        # Centering the window on the screen when the window is shown
        rect = self.frameGeometry()
        centerPoint = QApplication.screens()[0].availableGeometry().center()
        rect.moveCenter(centerPoint)
        self.move(rect.topLeft())
        super().showEvent(event)    

    def performCalculation(self):
        selected_button = self.applianceButtons.checkedButton()
        appliance = selected_button.text() if selected_button else None
        emission = float(self.carbonIntensityInput.text())
        
        # Average power consumption in watts and additional metrics
        avg_power = {
            "Smartphone Charger": 5, 
            "LED Light Bulb": 10, 
            "Television": 100, 
            "Human Breathing": None, 
            "Ice Cap Melting": None,
            "Deforestation": None  
        }

        deforestation_co2_absorption = 2.4  # metric tons of CO2 per hectare per year

        # Calculate the time based on the emission and average power
        if appliance in avg_power and avg_power[appliance] is not None:
            power = avg_power[appliance]
            time_hours = emission / (power / 1000)
            result = f"The amount of CO2 generated is equivalent to running {appliance} for {time_hours:.2f} hours."
        elif appliance == "Human Breathing":
            co2_per_day = 1  # kg per day
            time_days = emission / co2_per_day
            result = f"The amount of CO2 generated is equivalent to human breathing for {time_days:.2f} days."
        elif appliance == "Ice Cap Melting":
            co2_per_ton_for_melting = 1000  # kg per metric ton
            area_melted_per_ton = 3 * 1000000  # square millimeters
            area_melted = (emission / co2_per_ton_for_melting) * area_melted_per_ton
            result = f"The amount of CO2 generated is equivalent to ice caps melting about {area_melted:.2f} square millimeters."
        elif appliance == "Deforestation":
            area_saved_per_ton = (emission / deforestation_co2_absorption) * 10000  # square meters (converted from hectares)
            result = f"The amount of CO2 generated is equivalent to the absorption of a {area_saved_per_ton:.2f} square meter forest area for one year."
        else:
            result = "Invalid appliance selected."

        self.resultLabel.setStyleSheet("color: red;")
        self.resultLabel.setText(result)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmissionCalculator()
    ex.show()
    sys.exit(app.exec())
