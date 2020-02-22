# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
 
class Item(object):
    def __init__(self, _parent=None):
        self._dict = {}
        self.parent_item = _parent
        self.children = []
    
    def appendChild(self, item):
        self.children.append(item)

    def data(self, column):
        if column in self._dict.keys():
            return self._dict[column]
        return ''
 
    def setData(self, column, data):
        self._dict[column] = data
    
    def child(self, row):
        return self.children[row]

    def childrenCount(self):
        return len(self.children)

    def parent(self):
        return self.parent_item

    def removeChild(self, row):
        del self.children[row]

    def row(self):
        if self.parent_item:
            return self.parent_item.children.index(self)
        return 0

class Model(QtCore.QAbstractItemModel):
    def __init__(self, parent_=None):
        super(Model, self).__init__(parent_)
        self.items = []
        self.column = 0

    def addItem(self, row, item, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self.items.insert(row, item)
        self.endInsertRows()

    def columnCount(self, parent=QtCore.QModelIndex()):
        if len(self.items) == 0:
            return self.column
        return len(self.items[0])
 
    def data(self, index, role):
        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            return self.items[index.row()][index.column()]
        return QtCore.QVariant()
        
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, i, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return i
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return i

    def index(self, row, column, parent=QtCore.QModelIndex()):
        return self.createIndex(row, column, parent)

    def parent(self, index):
        return QtCore.QModelIndex()
        
    def removeItem(self, row, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        del self.items[row]
        self.endRemoveRows()
 
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.items)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self.items[index.row()][index.column()] = value
            #index.internalPointer() = value
            return True
        return False

class Delegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None, setModelDataEvent=None):
        super(Delegate, self).__init__(parent)
        self.setModelDataEvent = setModelDataEvent
 
    def createEditor(self, parent, option, index):
        return QtWidgets.QLineEdit(parent)
 
    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setText(str(value))
 
    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())
        if not self.setModelDataEvent is None:
            self.setModelDataEvent()