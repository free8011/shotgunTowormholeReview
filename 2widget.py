# -*- coding: utf-8 -*-
import csv
import json
import os
import sys

import requests
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication, QMainWindow, QPushButton, QWidget

userpath = os.path.join(os.path.expanduser("~"), 'wormhole')
setupfile = "setting.env"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class UIToolTab(QWidget):
    def __init__(self, parent=None):
        super(UIToolTab, self).__init__(parent)
        # self.CPSBTN = QPushButton("text2", self)
        # self.CPSBTN.move(100, 350)

        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1160, 313)

        self.horizontalLayoutWidget = QtGui.QWidget(Form)

        self.label = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label.setText('http://')
        self.lineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 110, 1141, 80))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(991, 223, 161, 61))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.save)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("setting your wormhole url", "setting wormhole url", None))

        # self.pushButton.setText(_translate("Form", "Up Load", None))
        self.pushButton.setText(_translate("Form", "Next", None))

    def save(self):
        url = self.lineEdit.text()
        if not url == '':
            if not os.path.exists(userpath):
                os.makedirs(userpath)
            with open(os.path.join(userpath, setupfile), 'wt') as f:
                f.write("url : %s" % url)
                # print "url:%s"% url
        else:
            pass
            # print os.path.join(userpath,setupfile)


class UIWindow(QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))

        # self.ToolsBTN.move(50, 350)
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1160, 313)
        self.company = 'min'
        self.filename = ''
        self.reviewlist = []
        self.projectlist = []
        self.getshotlist = []
        self.userlist = []
        self.whTaskTypeList = []
        self.AuthorId = ""
        self.AReviewer = ""
        self.url = "http://min.wormholepipeline.com/interface"
        self.resultReview = []

        self.ToolsBTN = QPushButton('setting wormhole URL', self)
        self.ToolsBTN.setGeometry(10, 223, 200, 61)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(991, 223, 161, 61))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.requester = QtGui.QLabel(Form)
        self.requester.setGeometry(QtCore.QRect(855, 20, 190, 41))

        self.comboBox = QtGui.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(960, 20, 191, 41))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))

        self.Reviewer = QtGui.QLabel(Form)
        self.Reviewer.setGeometry(QtCore.QRect(755, 65, 190, 41))

        self.comboBox2 = QtGui.QComboBox(Form)
        self.comboBox2.setGeometry(QtCore.QRect(960, 65, 191, 41))
        self.comboBox2.setObjectName(_fromUtf8("comboBox2"))

        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 110, 1141, 80))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_2 = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # event control
        self.pushButton_2.clicked.connect(self.selfile)
        self.comboBox.currentIndexChanged.connect(self.selAuthor)
        self.comboBox2.currentIndexChanged.connect(self.selReviewer)
        self.pushButton.clicked.connect(self.send)

        # self.done_btn = QtGui.QPushButton()
        # self.done_btn.setText(_translate("Form", "finished", None))

        self.getTaskTypeList()

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "Up Load", None))
        self.pushButton_2.setText(_translate("Form", "...", None))
        self.requester.setText(_translate("Form", "Requester : ", None))
        self.Reviewer.setText(_translate("Form", "Reviewer (Approver) : ", None))

    def selAuthor(self, index):
        # print unicode(self.comboBox.currentText())
        requester = self.comboBox.itemData(index, QtCore.Qt.UserRole).toString()
        self.AuthorId = unicode(requester)

    def selReviewer(self, index):
        # print unicode(self.comboBox.currentText())
        requester = self.comboBox2.itemData(index, QtCore.Qt.UserRole).toString()
        self.AReviewer = unicode(requester)

    def selfile(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Select File', '.')
        self.lineEdit.setText(self.filename)

        with open(self.filename) as f:
            reader = csv.reader(f)
            next(reader)
            self.reviewlist = []
            # projectlist = []
            for id, Subject, Links, Thumbnail, Body, Status, Author, To, Type, Date_Created, Date_Updated, Updated_by, Attachment, Deadline, Priority, Tags, Project in reader:
                dic = {}
                dic['shotgunid'] = id
                dic["projectId"] = str(Project)
                dic["reviewComment"] = str(Body)
                dic["author"] = str(Author)
                dic["cdate"] = str(Date_Created)
                dic["edate"] = str(Date_Updated)
                dic["updateby"] = str(Updated_by)
                id = Links.split('_')
                dic["tasktypeNm"] = id[-2]
                dic["version"] = id[-1]
                del id[-2:]
                dic["shotid"] = '_'.join(id)
                if not self.projectlist.count(Project) >= 1:
                    self.projectlist.append(Project)

                dic["reviewerCC"] = self.getContactList(Project, dic["shotid"])

                dic["taskTypeCd"] = self.getTaskTypeName(dic["tasktypeNm"])
                self.reviewlist.append(dic)

        self.getuserlist()

        return

    def getdata(self, apiname, paras):
        apiUrl = self.url + apiname
        api = requests.post(apiUrl, data=paras)
        return json.loads(api.text)

    def getuserlist(self):
        shotlist_api = "/getProjectUser.php?"
        for proj in self.projectlist:
            paras = {"corpPrefix": self.company, "projectId": proj, "format": "json"}
            data = self.getdata(shotlist_api, paras)
            users = data['UserList']
            for userid in users:
                if not self.userlist.count(userid['userId']) >= 1:
                    udic = {}
                    udic['id'] = userid['userId']
                    udic['name'] = userid['userName']

                    self.userlist.append(udic)
                    self.comboBox.addItem(userid['userName'], userid['userId'])
                    self.comboBox2.addItem(userid['userName'], userid['userId'])
        return

    def getContactList(self, proj, id):
        contactList_api = "/getContactList.php?"
        paras = {"corpPrefix": self.company, "projectId": proj, "shotId": id, "format": "json"}
        data = self.getdata(contactList_api, paras)
        # pprint(data)
        reviewerCC = []
        if data['isSuccess'] == '1':
            for userList in data['userList']:
                if userList['taskTypeCode'] != '':
                    reviewerCC.append(userList['userId'])
        return ','.join(reviewerCC)

    def getTaskTypeList(self):
        taskType = "/getTaskTypeList.php?"
        paras = {"corpPrefix": self.company, "format": "json"}
        data = self.getdata(taskType, paras)
        if data['isSuccess'] == '1':
            self.whTaskTypeList = data['taskTypeList']

    def getTaskTypeName(self, name):
        gettasktype = []
        for tasktype in self.whTaskTypeList:
            if tasktype['name'] == name:
                gettasktype.append(tasktype['code'])

        if len(gettasktype) == 1:
            return gettasktype[0]

        elif len(gettasktype) > 1:
            print 'error : The taskname is not only "%s"' % name
        elif len(gettasktype) == 0:
            print 'error : not exits taskname "%s"' % name

    def send(self):
        rowcount = len(self.reviewlist)
        resultAPI = {}
        for reqList in self.reviewlist:
            reqReview_api = "/reqReview.php?"
            paras = {"corpPrefix": self.company, "projectId": reqList['projectId'], "nodeType": "S",
                     "nodeId": reqList['shotid'], "taskTypeCd": reqList['taskTypeCd'],
                     "reviewComment": reqList['reviewComment'], "userId": self.AuthorId,
                     "reviewerCC": reqList['reviewerCC'], "reviewerApr": self.AReviewer, "format": "json"}
            data = self.getdata(reqReview_api, paras)
            if data['isSuccess'] == '0':
                reqList['result'] = "False"
            else:
                reqList['result'] = "True"
            self.resultReview.append(reqList)


            # print self.resultReview
            # self.done_btn.show()


# reqReview.php?
# corpPrefix=std&projectId=BGJ&nodeType=S&nodeId=MK2_20_0020&taskTypeCd=13&movie=p:/std/BGJ/MK2_20/MK2_20_0020/PMH/abc.mov&reviewComment=reviewcomments here..&userId=test01&reviewerApr=ApprUserId&reviewerCC=CCuserId1,CCuserId2,CCuserId3


class ResultView(QWidget):
    def __init__(self, parent=None, reviewlist=[]):
        super(ResultView, self).__init__(parent)
        self.reviewlist = reviewlist
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1160, 313)

        self.tableview = QtGui.QTableWidget(Form)
        self.tableview.setObjectName(_fromUtf8("tableview"))
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.h_layout = QtGui.QVBoxLayout()
        self.h_layout.addWidget(self.tableview)
        self.setLayout(self.h_layout)

        self.run()

    def run(self):
        columns = self.reviewlist[0].keys()
        self.tableview.setColumnCount(len(columns))
        self.tableview.setRowCount(len(self.reviewlist))
        for i in range(len(columns)):
            key = columns[i]
            self.tableview.setHorizontalHeaderItem(i, QtGui.QTableWidgetItem(key))

        for row in range(len(self.reviewlist)):
            datavalues = self.reviewlist[row].values()

            for i in range(len(datavalues)):
                item = QtGui.QTableWidgetItem(datavalues[i])
                self.tableview.setItem(row, i, item)
                if self.reviewlist[row]['result'] == 'False':
                    self.tableview.item(row, i).setBackground(QtGui.QColor(255, 0, 0))
                else:
                    self.tableview.item(row, i).setBackground(QtGui.QColor(255, 255, 255))
        for i in range(len(columns)):
            self.tableview.resizeColumnToContents(i)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        settingfilepath = os.path.join(userpath, setupfile)
        app_icon = QtGui.QIcon('WH_Icon16.png')
        self.setWindowIcon(app_icon)
        if not os.path.exists(settingfilepath):
            self.startUIToolTab()
        else:
            self.startUIWindow()

    def startUIToolTab(self):
        self.resize(1160, 313)
        self.ToolTab = UIToolTab(self)
        self.setWindowTitle("setting wormhole URL")
        self.setCentralWidget(self.ToolTab)
        self.ToolTab.pushButton.clicked.connect(self.startUIWindow)
        self.show()

    def startUIWindow(self):
        self.resize(1160, 313)
        self.Window = UIWindow(self)
        self.setWindowTitle("review to wormhole from shotgun")
        self.setCentralWidget(self.Window)
        self.Window.ToolsBTN.clicked.connect(self.startUIToolTab)
        self.Window.pushButton.clicked.connect(self.startResultView)
        self.show()

    def startResultView(self):
        resultreviewlist = self.Window.resultReview
        # self.Window.done_btn.close()
        self.resize(1160, 313)
        self.ui3 = ResultView(self, resultreviewlist)

        self.setWindowTitle("result view")
        self.setCentralWidget(self.ui3)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
