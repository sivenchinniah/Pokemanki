from aqt.qt import *
from aqt import mw

from .utils import *


class Tags:
    def __init__(self):
        self.parentwindow = QDialog()
        self.alltags = []

    def tagMenu(self):
        self.savedtags = get_json("_tags.json", [])
        rawtags = mw.col.tags.all()
        alltags = self.alltags
        for item in rawtags:
            taglist = item.split("::")
            alltags.append(taglist)
        tagdict = {}
        for item in alltags:
            if len(item) == 1:
                if item[0] in tagdict:
                    continue
                else:
                    tagdict[item[0]] = {}
            elif len(item) == 2:
                if item[0] in tagdict:
                    if item[1] in tagdict[item[0]]:
                        continue
                    else:
                        tagdict[item[0]][item[1]] = {}
                else:
                    tagdict[item[0]] = {}
                    tagdict[item[0]][item[1]] = {}
            elif len(item) == 3:
                if item[0] in tagdict:
                    if item[1] in tagdict[item[0]]:
                        if item[2] in tagdict[item[0]][item[1]]:
                            continue
                        else:
                            tagdict[item[0]][item[1]][item[2]] = {}
                    else:
                        tagdict[item[0]][item[1]] = {}
                        tagdict[item[0]][item[1]][item[2]] = {}
                else:
                    tagdict[item[0]] = {}
                    tagdict[item[0]][item[1]] = {}
                    tagdict[item[0]][item[1]][item[2]] = {}
            elif len(item) == 4:
                if item[0] in tagdict:
                    if item[1] in tagdict[item[0]]:
                        if item[2] in tagdict[item[0]][item[1]]:
                            if item[3] in tagdict[item[0]][item[1]][item[2]]:
                                continue
                            else:
                                tagdict[item[0]][item[1]
                                                 ][item[2]][item[3]] = {}
                        else:
                            tagdict[item[0]][item[1]][item[2]] = {}
                            tagdict[item[0]][item[1]][item[2]][item[3]] = {}
                    else:
                        tagdict[item[0]][item[1]] = {}
                        tagdict[item[0]][item[1]][item[2]] = {}
                        tagdict[item[0]][item[1]][item[2]][item[3]] = {}
                else:
                    tagdict[item[0]] = {}
                    tagdict[item[0]][item[1]] = {}
                    tagdict[item[0]][item[1]][item[2]] = {}
                    tagdict[item[0]][item[1]][item[2]][item[3]] = {}
        taglist = []
        for i in tagdict:
            if not tagdict[i]:
                taglist.append([i, []])
            else:
                childlist = []
                for j in tagdict[i]:
                    if not tagdict[i][j]:
                        childlist.append([j, []])
                    else:
                        grandchildlist = []
                        for k in tagdict[i][j]:
                            if not tagdict[i][j][k]:
                                grandchildlist.append([k, []])
                            else:
                                greatgrandchildlist = []
                                for l in tagdict[i][j][k]:
                                    greatgrandchildlist.append([l, []])
                                greatgrandchildlist = sorted(
                                    greatgrandchildlist, key=lambda x: x[0].lower())
                                grandchildlist.append([k, greatgrandchildlist])
                        grandchildlist = sorted(
                            grandchildlist, key=lambda x: x[0].lower())
                        childlist.append([j, grandchildlist])
                childlist = sorted(childlist, key=lambda x: x[0].lower())
                taglist.append([i, childlist])
        taglist = sorted(taglist, key=lambda x: x[0].lower())
        parentwindow = self.parentwindow
        parentwindow.setMinimumWidth(255)
        parentwindow.setMinimumHeight(192)
        lbl = QLabel(
            "Please select the tags for which you would like Pokemon assigned.", parentwindow)
        lbl.move(5, 5)
        widget = QWidget(parentwindow)
        widget.resize(255, 192)
        widget.move(0, 20)
        tree = QTreeWidget(widget)
        tree.setColumnCount(1)
        tree.setHeaderLabels(["Tags"])
        headerItem = QTreeWidgetItem()
        item = QTreeWidgetItem()
        parentlist = self.parentlist = []
        for i in taglist:
            if not i[1]:
                parent = QTreeWidgetItem(tree)
                parent.setText(0, i[0])
                parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
                if i[0] in self.savedtags:
                    parent.setCheckState(0, Qt.Checked)
                else:
                    parent.setCheckState(0, Qt.Unchecked)
                parentlist.append([parent, []])
            else:
                parent = QTreeWidgetItem(tree)
                parent.setText(0, i[0])
                parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
                if i[0] in self.savedtags:
                    parent.setCheckState(0, Qt.Checked)
                else:
                    parent.setCheckState(0, Qt.Unchecked)
                childlist = []
                for j in i[1]:
                    if not j[1]:
                        child = QTreeWidgetItem(parent)
                        child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                        child.setText(0, j[0])
                        if i[0] + "::" + j[0] in self.savedtags:
                            child.setCheckState(0, Qt.Checked)
                        else:
                            child.setCheckState(0, Qt.Unchecked)
                        childlist.append([child, []])
                    else:
                        child = QTreeWidgetItem(parent)
                        child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                        child.setText(0, j[0])
                        if i[0] + "::" + j[0] in self.savedtags:
                            child.setCheckState(0, Qt.Checked)
                        else:
                            child.setCheckState(0, Qt.Unchecked)
                        grandchildlist = []
                        for k in j[1]:
                            if not k[1]:
                                grandchild = QTreeWidgetItem(child)
                                grandchild.setFlags(
                                    grandchild.flags() | Qt.ItemIsUserCheckable)
                                grandchild.setText(0, k[0])
                                if i[0] + "::" + j[0] + "::" + k[0] in self.savedtags:
                                    grandchild.setCheckState(0, Qt.Checked)
                                else:
                                    grandchild.setCheckState(0, Qt.Unchecked)
                                grandchildlist.append([grandchild, []])
                            else:
                                grandchild = QTreeWidgetItem(child)
                                grandchild.setFlags(
                                    grandchild.flags() | Qt.ItemIsUserCheckable)
                                grandchild.setText(0, k[0])
                                if i[0] + "::" + j[0] + "::" + k[0] in self.savedtags:
                                    grandchild.setCheckState(0, Qt.Checked)
                                else:
                                    grandchild.setCheckState(0, Qt.Unchecked)
                                greatgrandchildlist = []
                                for l in k[1]:
                                    greatgrandchild = QTreeWidgetItem(
                                        grandchild)
                                    greatgrandchild.setFlags(
                                        greatgrandchild.flags() | Qt.ItemIsUserCheckable)
                                    greatgrandchild.setText(0, l[0])
                                    if i[0] + "::" + j[0] + "::" + k[0] + "::" + l[0] in self.savedtags:
                                        greatgrandchild.setCheckState(
                                            0, Qt.Checked)
                                    else:
                                        greatgrandchild.setCheckState(
                                            0, Qt.Unchecked)
                                    greatgrandchildlist.append(
                                        [greatgrandchild, []])
                                grandchildlist.append(
                                    [grandchild, greatgrandchildlist])
                        childlist.append([child, grandchildlist])
                parentlist.append([parent, childlist])
        btn = QPushButton("OK", parentwindow)
        btn.move(100, 220)
        btn.clicked.connect(self.tagAssign)
        parentwindow.exec_()

    def tagAssign(self):
        checked = self.checked = []
        for item in self.parentlist:
            if item[0].checkState(0) == Qt.Checked:
                checked.append(item[0].text(0))
            if item[1]:
                for jtem in item[1]:
                    if jtem[0].checkState(0) == Qt.Checked:
                        checked.append(item[0].text(
                            0) + "::" + jtem[0].text(0))
                    if jtem[1]:
                        for ktem in jtem[1]:
                            if ktem[0].checkState(0) == Qt.Checked:
                                checked.append(item[0].text(
                                    0) + "::" + jtem[0].text(0) + "::" + ktem[0].text(0))
                            if ktem[1]:
                                for ltem in ktem[1]:
                                    if ltem[0].checkState(0) == Qt.Checked:
                                        checked.append(item[0].text(
                                            0) + "::" + jtem[0].text(0) + "::" + ktem[0].text(0) + "::" + ltem[0].text(0))

        write_json("_tags.json", checked)
        self.parentwindow.done(QDialog.Accepted)
