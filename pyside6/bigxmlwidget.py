from enum import Enum
from PySide6.QtCore import QXmlStreamReader, QFile, QIODevice, Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QTreeWidget, QWidget, QMessageBox, QTreeWidgetItem, QApplication


class XmlItemType(Enum):
    Empty = 0
    Node = 1
    Attribute = 2
    Comment = 3

class BigXmlItem(QTreeWidgetItem):
     def __init__(self, parent, type):
        super( BigXmlItem, self ).__init__( parent)
        self.__type = type

     @property
     def type(self):
        return self.__type   


class BigXmlWidget(QTreeWidget, QWidget):

    def __init__(self, parent):
        super( BigXmlWidget, self ).__init__( parent )

        self.currentFile = QFile()
        self.readLevel = -1
        self.fOpenNew = True
        #folderIcon = QIcon()
        #folderIcon.addPixmap( QIcon(':/images/open.png'), QIcon.Normal, QIcon.On)
        #folderIcon.addPixmap( QIcon(':/images/close.png'), QIcon.Normal, QIcon.Off)

        HEADERS = (self.tr("Node/Attribute"), self.tr("Value"))
        self.setColumnCount(len(HEADERS))
        self.setHeaderLabels(HEADERS)
        self.setAlternatingRowColors(True)

    def openFile(self, fileName: str, fOpenNew: bool):
        if self.fOpenNew:
            self.currentFile.close()
            self.currentFile.setFileName(fileName)
            if self.currentFile.open(QIODevice.ReadOnly | QIODevice.Text):
                self.currentFile.seek(0)
                self.readBigXMLtoLevel(2)
                return True
            else:
                QMessageBox.warning(self, self.tr("BigXmlReader"),
                                  self.tr("Cannot read file "+fileName+" - "+self.currentFile.errorString()))
                return False
        return True

    def readBigXMLtoLevel(self,levelDown: int):
        xml = QXmlStreamReader(self.currentFile)
        item = BigXmlItem(self)
        level = 0;

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.clear()
        while not xml.atEnd():
            tokentype = xml.readNext() 

            match tokentype:
                case QXmlStreamReader.StartElement:
                    level = level+1
                    if level <= levelDown:
                        item = self.createChildItem(item, XmlItemType.Node)
                        item.setText(0, xml.name().toString());
                        #item.setIcon(0, folderIcon);
                        if level == levelDown:
                            newItem = BigXmlItem(item, XmlItemType.Empty)
                        else:
                            for attr in xml.attributes():
                                childItem = BigXmlItem(item, XmlItemType.Attribute)
                                childItem.setText(0, attr.name().toString())
                                childItem.setText(1, attr.value().toString())
            
                    break
                case QXmlStreamReader.EndElement:
                    if level <= levelDown:
                        if (item): item = item.parent()
                        level = level - 1
                    break
                case QXmlStreamReader.Characters, QXmlStreamReader.DTD, QXmlStreamReader.Comment:
                    if (level <= levelDown):
                        if (item):
                            name = xml.text().toString().simplified()
                            if ( name.size() > 0):
                                item.setText(1, name)
                                item.setIcon(0, bookmarkIcon)
                                item.setXmlType(BigXmlItem.Comment)
                                item.takeChildren().clear()
                            
                    break

        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        QApplication.restoreOverrideCursor()
        return not xml.error()