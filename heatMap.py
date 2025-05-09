from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QTextEdit, QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

class HeatmapApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heatmap Generator")
        self.setGeometry(200, 150, 900, 650)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Button layout
        button_layout = QHBoxLayout()

        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }

            QTextEdit {
                border-radius: 8px;
                padding: 10px;
            }

            QLabel {
                padding: 6px;
            }

            QPushButton {
                background-color: #203F9A;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-weight: 500;
            }

            QPushButton:hover {
                background-color: #4173B0;
            }

            QPushButton:pressed {
                background-color: #1c3788;
            }

            QPushButton:disabled {
                background-color: #c4c4c4;
                color: #eeeeee;
            }
        """)


        # Upload button
        self.upload_btn = QPushButton(" Load CSV File")
        self.upload_btn.clicked.connect(self.load_file)
        button_layout.addWidget(self.upload_btn)

        # Generate button
        self.generate_btn = QPushButton(" Generate Heatmap")
        self.generate_btn.clicked.connect(self.generate_from_text)
        button_layout.addWidget(self.generate_btn)

        # Save button
        self.save_btn = QPushButton(" Save Heatmap")
        self.save_btn.clicked.connect(self.save_heatmap)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)

        # Clear button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_btn)

        self.layout.addLayout(button_layout)
        

        # Text input
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter values separated by commas (e.g.:\n1.1,2.2,3.3\n4.4,5.5,6.6)")
        self.layout.addWidget(self.text_edit)

        # Status label
        self.info_label = QLabel("Waiting for input...")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.heatmap_file = "heatmap_temp.png"

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                data = pd.read_csv(file_path, header=None)
                self.info_label.setText("CSV file loaded. Generating heatmap...")
                self.show_heatmap(data)
            except Exception as e:
                self.info_label.setText(f"Error: {str(e)}")

    def generate_from_text(self):
        try:
            text = self.text_edit.toPlainText()
            lines = text.strip().split("\n")
            data = []
            for i, line in enumerate(lines, start=1):
                row = []
                for j, val in enumerate(line.strip().split(","), start=1):
                    try:
                        row.append(float(val.strip()))
                    except ValueError:
                        raise ValueError(f"Invalid number at row {i}, column {j}: '{val}'")
                data.append(row)
            df = pd.DataFrame(data)
            self.info_label.setText("Generating heatmap from text...")
            self.show_heatmap(df)
        except Exception as e:
            self.info_label.setText(f"Input error: {str(e)}")

    def show_heatmap(self, data):
        plt.figure(figsize=(8, 8))  # Kare oranlı ve daha geniş alan
        ax = sns.heatmap(data, cmap="YlOrRd", cbar=True, square=True, linewidths=0.5, linecolor='black')
        ax.set_title("Heatmap with color bar")
        plt.xticks(rotation=0)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(self.heatmap_file)
        plt.close()

        pixmap = QPixmap(self.heatmap_file)
        self.image_label.setPixmap(pixmap)
        self.save_btn.setEnabled(True)
        self.info_label.setText("✅ Heatmap generated successfully.")


    def save_heatmap(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Heatmap As", "heatmap.png", "PNG Files (*.png)")
        if file_path:
            try:
                os.replace(self.heatmap_file, file_path)
                self.info_label.setText(f"✅ Heatmap saved: {file_path}")
                self.save_btn.setEnabled(False)
            except Exception as e:
                self.info_label.setText(f"Save error: {str(e)}")

    def clear_all(self):
        self.text_edit.clear()
        self.image_label.clear()
        self.info_label.setText("Cleared.")
        self.save_btn.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeatmapApp()
    window.show()
    sys.exit(app.exec())
