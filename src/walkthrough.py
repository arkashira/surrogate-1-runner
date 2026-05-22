import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox

class WalkthroughWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Initial Setup Walkthrough")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Welcome to the initial setup walkthrough!")
        self.layout.addWidget(self.label)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_step)
        self.layout.addWidget(self.next_button)

        self.skip_button = QPushButton("Skip")
        self.skip_button.clicked.connect(self.skip_walkthrough)
        self.layout.addWidget(self.skip_button)

        self.current_step = 0
        self.steps = [
            "Step 1: Configure your environment variables.",
            "Step 2: Install the required dependencies.",
            "Step 3: Set up the initial dataset configuration.",
            "Step 4: Verify the setup and start the service."
        ]

        self.update_step()

    def update_step(self):
        if self.current_step < len(self.steps):
            self.label.setText(self.steps[self.current_step])
        else:
            self.label.setText("Walkthrough completed!")
            self.next_button.setText("Finish")
            self.next_button.clicked.connect(self.close)

    def next_step(self):
        self.current_step += 1
        self.update_step()

    def skip_walkthrough(self):
        reply = QMessageBox.question(self, 'Skip Walkthrough', 'Are you sure you want to skip the walkthrough?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

def check_first_launch():
    first_launch_file = "/opt/axentx/surrogate-1/.first_launch"
    if not os.path.exists(first_launch_file):
        with open(first_launch_file, 'w') as f:
            f.write("Walkthrough completed")
        return True
    return False

def main():
    app = QApplication([])
    if check_first_launch():
        window = WalkthroughWindow()
        window.show()
        app.exec_()

if __name__ == "__main__":
    main()