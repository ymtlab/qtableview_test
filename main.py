import sys
from mainwindow import Ui_MainWindow
from tableview import Model, Delegate, Item
from PyQt5 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = Model(self)
        self.model.column = 100

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setItemDelegate(Delegate())
        self.ui.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tableView.customContextMenuRequested.connect(self.contextMenu)
        self.ui.pushButton.clicked.connect(self.insertRow)
        self.ui.pushButton_2.clicked.connect(self.delItem)

    def contextMenu(self, point):
        self.menu = QtWidgets.QMenu(self)
        self.menu.addAction('Insert', self.insertRow)
        self.menu.addAction('Delete', self.delItem)
        self.menu.exec_( self.focusWidget().mapToGlobal(point) )
 
    def insertRow(self):
        indexes = self.ui.tableView.selectedIndexes()
        
        if len(indexes) == 0:
            item = [ str(self.model.rowCount()) + str(i) for i in range(self.model.column) ]
            self.model.addItem( self.model.rowCount(), item )
            return
        
        indexes2 = []
        for index in indexes[::-1]:
            if not index.row() in [ index2.row() for index2 in indexes2 ]:
                indexes2.append(index)

        for index in indexes2:
            item = [ str(self.model.rowCount()) + str(i) for i in range(self.model.column) ]
            self.model.addItem( index.row() + 1, item )

    def delItem(self):
        indexes = self.ui.tableView.selectedIndexes()
        
        if self.model.rowCount() == 0:
            return

        if len(indexes) == 0:
            self.model.removeItem( self.model.rowCount()-1 )
            return
        
        rows = set( [ index.row() for index in indexes ] )
        for row in list(rows)[::-1]:
            self.model.removeItem( row )
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
 
if __name__ == '__main__':
    main()