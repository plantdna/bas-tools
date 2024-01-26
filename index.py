import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from components.LineFileDialogEdit import lineFileDialogEdit
from services.smd import simplified_marker_design
from services.ba import background_assessment

class ImageWindow(QDialog):
    def __init__(self, image_path, id):
        super().__init__()
        self.image_path = image_path
        self.id = id
        self.initUI()
 
    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle(self.id)
        self.resize(500, 500)
        self.setFixedSize(self.width(), self.height())

        self.image_label = QLabel()
        pix = QPixmap(self.image_path)
        self.image_label.setPixmap(pix)
        self.image_label.setScaledContents(True)

        vbox=QVBoxLayout()
        vbox.addWidget(self.image_label)
        self.setLayout(vbox)


class BASWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BASTools V1.0")
        # initial window size
        self.resize(640, 680)
        # disabled adjust window size
        self.setFixedSize(self.width(), self.height())

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "Simplified Marker Design")
        self.addTab(self.tab2, "Background Assessment")

        # default tab index
        self.setCurrentIndex(0)

        # initial Tab UI
        self.step1UI(self.tab1)
        self.step2UI(self.tab2)

    def message_box(self, info):
        msg = QMessageBox() 
        msg.setIcon(QMessageBox.Information) 

        # setting message for Message Box 
        msg.setText(info) 
        
        # setting Message box window title 
        msg.setWindowTitle("Information MessageBox") 
    
        # declaring buttons on Message Box 
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()


    def step1UI(self, tab):
        self.tab1_layout = QFormLayout()
        self.tab1_layout.setVerticalSpacing(20)

        ped_line = lineFileDialogEdit(QLineEdit(), "(*.ped)")
        ped_line.setFixedWidth(500)
        ped_line.setFixedHeight(32)

        map_line = lineFileDialogEdit(QLineEdit(), "(*.map)")
        map_line.setFixedWidth(500)
        map_line.setFixedHeight(32)

        num_line = QSpinBox()
        num_line.setFixedWidth(500)
        num_line.setFixedHeight(32)

        # submit button
        self.button = QPushButton("Start the analysis", self)
        self.button.setStyleSheet(
            """
            QPushButton{background:#096dd9;border-radius:5px;}
            """
        )
        self.button.setFixedHeight(32)
        self.button.clicked.connect(
            lambda: self.step1Submit(
                ped_line.text(),
                map_line.text(),
                num_line.text(),
            )
        )

        # image
        self.image_label = QLabel()
        pix = QPixmap(os.path.join(os.getcwd(), "output/selected_markers.png"))
        self.image_label.setPixmap(pix)
        self.image_label.setScaledContents(True)

        self.tab1_layout.addRow("FilePath(.ped):", ped_line)
        self.tab1_layout.addRow("FilePath(.map):", map_line)
        self.tab1_layout.addRow("Number:", num_line)
        self.tab1_layout.addRow(self.button)
        self.tab1_layout.addRow(self.image_label)

        tab.setLayout(self.tab1_layout)

    def step1Submit(self, ped, map, markers):
        try:
            self.button.setEnabled(False)
            self.button.setText("Loading...")
            simplified_marker_design(ped, map, int(markers))
            self.button.setEnabled(True)
            self.button.setText("Start the analysis")

            # update image
            pix = QPixmap(os.path.join(os.getcwd(), "output/selected_markers.png"))
            self.image_label.setPixmap(pix)
            self.image_label.setScaledContents(True)
        except Exception as e:
            self.message_box(str(e))

    def row_selection(self, row):
        try:
            image_path = os.path.join(os.getcwd(), f"output/sample_image/{row[0].text()}.png")
            if not os.path.exists(image_path):
                self.message_box("Please check that the picture was generated!")
            else:
                self.chile_Win = ImageWindow(image_path, row[0].text())
                self.chile_Win.show()
                self.chile_Win.exec_()
        except Exception as e:
            self.message_box(str(e))

    def step2Submit(self, ped_fp, map_fp):
        try:
            df = background_assessment(ped_fp, map_fp)
            (rc, cc) = df.shape
            columns = df.columns.tolist()
            self.tableWidget.setColumnCount(cc)
            self.tableWidget.setRowCount(rc)
            # 插入数据
            for i, row in df.iterrows():
                for j, c_name in enumerate(columns):
                    item = QTableWidgetItem(str(row[c_name]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(i, j, item)
        except Exception as e:
            self.message_box(str(e))


    def step2UI(self, tab):
        tab2_layout = QFormLayout()

        ped_line = lineFileDialogEdit(QLineEdit(), "(*.ped)")
        ped_line.setFixedWidth(500)
        ped_line.setFixedHeight(32)

        map_line = lineFileDialogEdit(QLineEdit(), "(*.map)")
        map_line.setFixedWidth(500)
        map_line.setFixedHeight(32)

        # submit button
        self.tab2_button = QPushButton("Start the analysis", self)
        self.tab2_button.setStyleSheet(
            """
            QPushButton{background:#096dd9;border-radius:5px;}
            """
        )
        self.tab2_button.setFixedHeight(32)
        self.tab2_button.clicked.connect(
            lambda: self.step2Submit(
                ped_line.text(),
                map_line.text(),
            )
        )

        # table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setHorizontalHeaderLabels(["ID"] + [f"Chr{i}" for i in range(1, 11)])
        # 绑定事件
        self.tableWidget.itemSelectionChanged.connect(
            lambda : self.row_selection(self.tableWidget.selectedItems())
        )

        tab2_layout.addRow("FilePath(.ped):", ped_line)
        tab2_layout.addRow("FilePath(.map):", map_line)
        tab2_layout.addRow(self.tab2_button)
        tab2_layout.addRow(self.tableWidget)

        tab.setLayout(tab2_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.getcwd(), "public/icons/icons8-dna-96.png")))
    basWidget = BASWidget()
    basWidget.show()
    sys.exit(app.exec())
