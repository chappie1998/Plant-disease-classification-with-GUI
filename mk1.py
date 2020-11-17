from PyQt5 import QtCore, QtGui, QtWidgets
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import os

new_model = tf.keras.models.load_model('saved_model')

classes_name = ['Apple Scab Leaf', 'Apple leaf', 'Apple rust leaf', 'Bell_pepper leaf', 'Bell_pepper leaf spot', 'Blueberry leaf', 'Cherry leaf', 'Corn Gray leaf spot', 'Corn leaf blight', 'Corn rust leaf', 'Peach leaf', 'Potato leaf early blight', 'Potato leaf late blight', 'Raspberry leaf', 'Soyabean leaf', 'Squash Powdery mildew leaf', 'Strawberry leaf', 'Tomato Early blight leaf', 'Tomato Septoria leaf spot', 'Tomato leaf', 'Tomato leaf bacterial spot', 'Tomato leaf late blight', 'Tomato leaf mosaic virus', 'Tomato leaf yellow virus', 'Tomato mold leaf', 'Tomato two spotted spider mites leaf', 'grape leaf', 'grape leaf black rot']

# Check its architecture
# new_model.summary()
global idx
global images_list

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(833, 754)

        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.acc_result = QtWidgets.QLineEdit(Dialog)
        # self.acc_result.setText("98%")
        self.acc_result.setObjectName("acc_result")
        self.gridLayout.addWidget(self.acc_result, 0, 4, 1, 1)

        self.exit = QtWidgets.QPushButton(Dialog)
        self.exit.clicked.connect(self.closeEvent)
        self.exit.setObjectName("exit")
        self.gridLayout.addWidget(self.exit, 0, 8, 1, 1)

        self.acc = QtWidgets.QLabel(Dialog)
        self.acc.setObjectName("acc")
        self.gridLayout.addWidget(self.acc, 0, 3, 1, 1)

        self.folder = QtWidgets.QPushButton(Dialog)
        self.folder.clicked.connect(self.getfolder)
        self.folder.setObjectName("folder")
        self.gridLayout.addWidget(self.folder, 0, 5, 1, 1)

        self.disease = QtWidgets.QLabel(Dialog)
        self.disease.setObjectName("disease")
        self.gridLayout.addWidget(self.disease, 0, 1, 1, 1)

        self.image = QtWidgets.QPushButton(Dialog)
        self.image.clicked.connect(self.getimage)
        self.image.setObjectName("image")
        self.gridLayout.addWidget(self.image, 0, 0, 1, 1)

        self.next = QtWidgets.QPushButton(Dialog)
        self.next.clicked.connect(self.nextimage)
        self.next.setObjectName("next")
        self.gridLayout.addWidget(self.next, 0, 6, 1, 1)

        self.result = QtWidgets.QLineEdit(Dialog)
        # self.result.setText("Apple rust leaf")
        self.result.setObjectName("result")
        self.gridLayout.addWidget(self.result, 0, 2, 1, 1)

        self.previous = QtWidgets.QPushButton(Dialog)
        self.previous.clicked.connect(self.previousimage)
        self.previous.setObjectName("previous")
        self.gridLayout.addWidget(self.previous, 0, 7, 1, 1)

        self.showimage = QtWidgets.QLabel(Dialog)
        self.showimage.setText("")
        self.showimage.setScaledContents(True)
        self.showimage.setObjectName("showimage")
        self.gridLayout.addWidget(self.showimage, 1, 0, 1, 9)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.exit.setText(_translate("Dialog", "Exit"))
        self.acc.setText(_translate("Dialog", "Accuracry"))
        self.folder.setText(_translate("Dialog", "Open Folder"))
        self.disease.setText(_translate("Dialog", "Disease"))
        self.image.setText(_translate("Dialog", "Image"))
        self.next.setText(_translate("Dialog", "Next"))
        self.previous.setText(_translate("Dialog", "Previous"))

    def getimage(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file', '.', "Image files (*.jpg *.png)")
        image_path = fname[0]
        img = Image.open(image_path)
        img = img.resize((256,256), Image.ANTIALIAS)
        img  = image.img_to_array(img)
        img  = img.reshape((1,) + img.shape)
        predictions = new_model.predict(img)
        self.acc_result.setText((str(round(np.amax(predictions[0])*100, 2))+"%"))
        print(np.amax(predictions[0]))
        predictions = classes_name[np.argmax(predictions[0])]
        print(predictions)
        self.result.setText(predictions)
        pixmap = QtGui.QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(500,500)
        self.showimage.setPixmap(scaled_pixmap)

    def getfolder(self):
        global images_list
        global idx
        images_list = []
        idx = 0
        dir = str(QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory"))
        for p in os.listdir(dir):
            images_list.append(dir+"/"+p)

        image_path = images_list[idx]
        img = Image.open(image_path)
        img = img.resize((256,256), Image.ANTIALIAS)
        img  = image.img_to_array(img)
        img  = img.reshape((1,) + img.shape)
        predictions = new_model.predict(img)
        self.acc_result.setText((str(round(np.amax(predictions[0])*100, 2))+"%"))
        print(np.amax(predictions[0]))
        predictions = classes_name[np.argmax(predictions[0])]
        print(predictions)
        self.result.setText(predictions)
        pixmap = QtGui.QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(500,500, QtCore.Qt.KeepAspectRatio)
        self.showimage.setPixmap(scaled_pixmap)

    def nextimage(self):
        global idx
        global images_list
        idx = idx + 1
        if idx >= len(images_list):
            idx = len(images_list)-1

        image_path = images_list[idx]
        img = Image.open(image_path)
        img = img.resize((256,256), Image.ANTIALIAS)
        img  = image.img_to_array(img)
        img  = img.reshape((1,) + img.shape)
        predictions = new_model.predict(img)
        self.acc_result.setText((str(round(np.amax(predictions[0])*100, 2))+"%"))
        print(np.amax(predictions[0]))
        predictions = classes_name[np.argmax(predictions[0])]
        print(predictions)
        self.result.setText(predictions)
        pixmap = QtGui.QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(500,500, QtCore.Qt.KeepAspectRatio)
        self.showimage.setPixmap(scaled_pixmap)

    def previousimage(self):
        global idx
        global images_list
        idx = idx - 1
        if idx <= 0:
            idx = 0
        image_path = images_list[idx]
        img = Image.open(image_path)
        img = img.resize((256,256), Image.ANTIALIAS)
        img  = image.img_to_array(img)
        img  = img.reshape((1,) + img.shape)
        predictions = new_model.predict(img)
        self.acc_result.setText((str(round(np.amax(predictions[0])*100, 2))+"%"))
        print(np.amax(predictions[0]))
        predictions = classes_name[np.argmax(predictions[0])]
        print(predictions)
        self.result.setText(predictions)
        pixmap = QtGui.QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(500,500, QtCore.Qt.KeepAspectRatio)
        self.showimage.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox()
        close.setText("You sure?")
        close.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        close = close.exec()
        if close == QtWidgets.QMessageBox.Yes:
            QtWidgets.qApp.quit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
