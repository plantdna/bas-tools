from PyQt5.QtWidgets import QAction, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import os

icon_file_path = os.path.join(os.getcwd(), "public/icons/icons8-file-64.png")
    
def openFileDialog(lineEdit, filter_txt=None):
    if filter_txt:
        (fp, ft) = QFileDialog.getOpenFileName(filter=filter_txt)
    else:
        (fp, ft) = QFileDialog.getOpenFileName()

    lineEdit.setText(fp)


def lineFileDialogEdit(lineEdit, filter_txt):
    selectApply = QAction(lineEdit)
    selectApply.setIcon(QIcon(icon_file_path))
    selectApply.triggered.connect(lambda: openFileDialog(lineEdit, filter_txt))
    lineEdit.addAction(selectApply, QLineEdit.TrailingPosition)
    return lineEdit