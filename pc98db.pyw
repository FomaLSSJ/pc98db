#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Thanks so much for the powerful support z3tzilla

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from lxml import etree
from lxml.html import HTMLParser
from tkinter import Tk
import urllib.request, lxml.html, webbrowser, string, sys, os

url = 'https://refuge.tokyo/pc9801/'

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		
		self.gameLink = None
		self.titleJap = None
		self.images = []
		self.cover = None
		
		self.setFixedSize(948, 600)
		self.setWindowTitle('PC98 Database Parser')
		self.statusBar().showMessage('Ready')
		
		self.cat = QComboBox(self)
		self.cat.setGeometry(QRect(5, 5, 256, 20))
		self.cat.currentIndexChanged.connect(self.SetCategories)
		
		self.sub_cat = QComboBox(self)
		self.sub_cat.setGeometry(QRect(5, 25, 256, 20))
		self.sub_cat.currentIndexChanged.connect(self.SetSubCategories)
		
		self.list = QTreeWidget(self)
		self.list.setHeaderHidden(True)
		self.list.clicked.connect(self.SetGame)
		self.list.setGeometry(QRect(5, 45, 256, 535))
		
		self.title = QLabel('<font size=5>???<br/>???</font>', self)
		self.title.setGeometry(QRect(280, 9, 741, 64))
		
		self.line = QFrame(self)
		self.line.setGeometry(QRect(280, 70, 648, 16))
		self.line.setFrameShape(QFrame.HLine)
		self.line.setFrameShadow(QFrame.Sunken)
		
		self.data = QLabel('Publisher:??? | Release:??? | Media:???', self)
		self.data.setGeometry(QRect(280, 87, 731, 16))
		
		self.cvr = QPushButton('Cover', self)
		self.cvr.clicked.connect(self.SetCover)
		self.cvr.setGeometry(QRect(280, 110, 60, 24))
		self.cvr.setEnabled(False)

		self.pic1 = QPushButton('Picture 1', self)
		self.pic1.clicked.connect(self.SetPic1)
		self.pic1.setGeometry(QRect(280, 140, 60, 24))
		self.pic1.setEnabled(False)
		
		self.pic2 = QPushButton('Picture 2', self)
		self.pic2.clicked.connect(self.SetPic2)
		self.pic2.setGeometry(QRect(350, 140, 60, 24))
		self.pic2.setEnabled(False)
		
		self.pic3 = QPushButton('Picture 3', self)
		self.pic3.clicked.connect(self.SetPic3)
		self.pic3.setGeometry(QRect(420, 140, 60, 24))
		self.pic3.setEnabled(False)
		
		self.scr1 = QPushButton('Screen 1', self)
		self.scr1.clicked.connect(self.SetScr1)
		self.scr1.setGeometry(QRect(520, 140, 60, 24))
		self.scr1.setEnabled(False)
		
		self.scr2 = QPushButton('Screen 2', self)
		self.scr2.clicked.connect(self.SetScr2)
		self.scr2.setGeometry(QRect(590, 140, 60, 24))
		self.scr2.setEnabled(False)
		
		self.scr3 = QPushButton('Screen 3', self)
		self.scr3.clicked.connect(self.SetScr3)
		self.scr3.setGeometry(QRect(660, 140, 60, 24))
		self.scr3.setEnabled(False)
		
		self.note = QPushButton('Note', self)
		self.note.clicked.connect(self.OpenNote)
		self.note.setGeometry(QRect(830, 110, 100, 24))
		self.note.setEnabled(False)
		
		self.browser = QPushButton('Open in Browser', self)
		self.browser.clicked.connect(self.GetUrl)
		self.browser.setGeometry(QRect(830, 140, 100, 24))
		
		self.copyjp = QPushButton('Copy Jap Title', self)
		self.copyjp.clicked.connect(self.CopyJpTitle)
		self.copyjp.setGeometry(QRect(830, 12, 100, 24))
		
		self.web = QWebEngineView(self)
		self.web.load(QUrl('http://fullmotionvideo.free.fr/screen/images/Noimage1.png'))
		self.web.setGeometry(QRect(280, 170, 650, 410))
		self.web.page().loadStarted.connect(self.WebStarted)
		self.web.page().loadFinished.connect(self.WebComplete)

		self.notewin = QWidget()
		self.webnote = QWebEngineView(self.notewin)
		self.webnote.setGeometry(QRect(5, 5, 1270, 790))
		
		self.about = QWidget()
		self.alabel = QLabel('<br/>Make script <b>FomaLSSJ</b><br/>Big thanks <b>z3tzilla</b><br/><br/><a href="https://github.com/FomaLSSJ/pc98db">Visit GitHub project page</a>', self.about)
		self.alabel.setOpenExternalLinks(True)
		self.alabel.setGeometry(QRect(5, 5, 310, 110))
		self.alabel.setAlignment(Qt.AlignCenter)
		
		self.GetRootElement()
		
	def SetCategories(self, index):
		self.statusBar().showMessage('Loading')
		self.GetCategories(self.cat.itemData(index))
		self.statusBar().showMessage('Complete')

	def SetSubCategories(self, index):
		self.statusBar().showMessage('Loading')
		self.GetSubCategories(self.sub_cat.itemData(index))
		self.statusBar().showMessage('Complete')

	def SetGame(self, index):
		if (not self.list.currentItem().text(1) or self.imgLoad):
			return
		
		try:
			self.gameLink = str(url + self.list.currentItem().text(1)[3:])
			self.page = urllib.request.urlopen(str(url + self.list.currentItem().text(1)[3:]))
			self.doc = lxml.html.document_fromstring(self.page.read(), parser=HTMLParser(encoding='utf-8'))
		except:
			self.statusBar().showMessage('Error, game not loaded')
			return
		
		self.statusBar().showMessage('Loading ...')
		
		self.images = []
		self.screens = []
		self.imgLoad = False

		coverVal = self.doc.cssselect('div#cover a')

		if (coverVal):
			self.cover = coverVal[0].get('href')
			self.cvr.setEnabled(True)
		else:
			self.cover = None
			self.cvr.setEnabled(False)
		
		self.titleEng = self.doc.cssselect('div#title_en')[0].text
		self.titleJap = self.doc.cssselect('div#title_jp')[0].text
		
		self.data.setText(self.doc.cssselect('div#publisher')[0].text)
		
		self.title.setText('<font size=5>%s<br/>%s</font>' % (self.titleEng, self.titleJap))
		
		noteVal = self.doc.cssselect('div.headline')
		
		if (noteVal):
			self.note.setEnabled(True)
		else:
			self.note.setEnabled(False)

		for A in self.doc.cssselect('div#screenshot a, div#screenshot_a a, div#screenshot_b a, div#screenshot_c a'):
			self.images.append(A.get('href'))
		
		if (self.images == []):
			for DIV in self.doc.cssselect('div.screenshot a'):
				self.images.append(DIV.get('href'))
			
			if (not self.images):
				self.web.setZoomFactor(1.68)
				for IMG in self.doc.cssselect('img.ss'):
					self.images.append(IMG.get('src'))
		
		for A in self.doc.cssselect('div#thumbnail a'):
			self.screens.append(A.get('href'))
			
		for A in self.doc.cssselect('div#thumbnail_re a'):
			self.screens.append(A.get('href'))
		
		if (not self.cover):
			self.cvr.setEnabled(False)
		else:
			self.cvr.setEnabled(True)

		self.pic1.setEnabled(True)
		self.pic2.setEnabled(True)
		self.pic3.setEnabled(True)

		if (not self.screens):
			self.scr1.setEnabled(False)
			self.scr2.setEnabled(False)
			self.scr3.setEnabled(False)
		else:
			self.scr1.setEnabled(True)
			self.scr2.setEnabled(False)
			self.scr3.setEnabled(False)
			if (len(self.screens) == 2):
				self.scr1.setEnabled(True)
				self.scr2.setEnabled(True)
				self.scr3.setEnabled(False)
			elif (len(self.screens) == 3):
				self.scr1.setEnabled(True)
				self.scr2.setEnabled(True)
				self.scr3.setEnabled(True)			
		
		self.web.load(QUrl(url + 'pc98/' + self.images[0]))
		self.web.setZoomFactor(1.0)
		self.SetButtonSelect(0)

	def GetRootElement(self):
		self.page = urllib.request.urlopen(url + "en/Adventure_ABCD.html")
		self.doc = lxml.html.document_fromstring(self.page.read())
		
		result = {}
		for A in self.doc.cssselect('div#genre-navi a'):
			result[A.cssselect('div')[0].text] = A.get('href')
		
		result.pop("Index", None)
		result.pop("Publisher", None)
		result.pop("PUBLISHER", None)
		result.pop("Exit", None)
		result.pop("EXIT", None)

		for key in sorted(result):
			self.cat.addItem(key, result[key])

	def GetCategories(self, url):
		self.page = urllib.request.urlopen('https://refuge.tokyo/pc9801/en/%s' % url)
		self.doc = lxml.html.document_fromstring(self.page.read())

		self.sub_cat.clear()
		
		result = {}
		for A in self.doc.cssselect('div#page_sel a, div#sub-genre a, div#sub-genre-fix a'):
			result[A.cssselect('div, span')[0].text] = A.get('href')
		
		for key in sorted(result):
			self.sub_cat.addItem(key, result[key])
		
		if (not result):
			self.GetSubCategories(url)

	def GetSubCategories(self, url):
		if (not url):
			return

		self.page = urllib.request.urlopen('https://refuge.tokyo/pc9801/en/%s' % url)
		self.doc = lxml.html.document_fromstring(self.page.read())
		
		self.list.clear()
		
		result = []
		
		for TD in self.doc.cssselect('div#gamelist table tr div.list_sub,div#gamelist2 table tr div.list_sub2'):
			result.append(TD.cssselect('div')[0].text)

		for r in result:
			self.rootTree = QTreeWidgetItem(self.list, [r])
			self.GetGameList(url, r)
			
		if (not result):
			self.rootTree = QTreeWidgetItem(self.list, ['List'])
			self.GetGameList(url, 'List')
		

	def GetGameList(self, url, subcat):
		result = {}
		getgame = False
		
		for TR in self.doc.cssselect('div#gamelist table tr, div#gamelist2 table tr'):
			for TD in TR.cssselect('td'):
				if ('class' in TD.attrib):
					if (TD.get('class') == 'list_sub'):
						if (TD.cssselect('div')[0].text == subcat):
							getgame = True
						else:
							getgame = False
				else:
					if (getgame):
						for A in TD.cssselect('a'):
							result[A.cssselect('div')[0].text] = A.get('href')
		
		if (subcat == 'List'):
			for A in self.doc.cssselect('div#gamelist table tr td a, div#gamelist2 table tr td a'):
				result[A.cssselect('div')[0].text] = A.get('href')
		
		for key in sorted(result):
			item = QTreeWidgetItem([key])
			item.setText(1, result[key])
			self.rootTree.addChild(item)
	
	def WebStarted(self):
		self.statusBar().showMessage('Loading Image ...')
		self.imgLoad = True
	
	def WebComplete(self):
		self.statusBar().showMessage('Image is Loaded')
		self.imgLoad = False
	
	def SetCover(self):
		if (not self.cover or self.cvr.isFlat() or self.imgLoad):
			pass
		else:
			print()
			self.web.load(QUrl(url + 'pc98/' + self.cover))
			self.web.setZoomFactor(1.0)
			self.SetButtonSelect(6)

	def SetPic1(self):
		if (not self.images or self.pic1.isFlat() or self.imgLoad):
			pass
		else:
			self.web.load(QUrl(url + 'pc98/' + self.images[0]))
			self.web.setZoomFactor(1.0)
			self.SetButtonSelect(0)
	
	def SetPic2(self):
		if (not self.images or self.pic2.isFlat() or self.imgLoad):
			pass
		else:
			self.web.load(QUrl(url + 'pc98/' + self.images[1]))
			self.web.setZoomFactor(1.0)
			self.SetButtonSelect(1)
	
	def SetPic3(self):
		if (not self.images or self.pic3.isFlat() or self.imgLoad):
			pass
		else:
			self.web.load(QUrl(url + 'pc98/' + self.images[2]))
			self.web.setZoomFactor(1.0)
			self.SetButtonSelect(2)
	
	def SetScr1(self):
		if (not self.screens or self.scr1.isFlat() or self.imgLoad):
			pass
		else:
			self.web.load(QUrl(url + 'pc98/' + self.screens[0]))
			self.web.setZoomFactor(1.0)
			self.SetButtonSelect(3)
	
	def SetScr2(self):
		if (not self.screens or self.scr2.isFlat() or self.imgLoad):
			pass
		else:
			self.web.load(QUrl(url + 'pc98/' + self.screens[1]))
			self.web.setZoomFactor(1.0)
			self.SetButtonSelect(4)
	
	def SetScr3(self):
		if (not self.screens or self.scr3.isFlat() or self.imgLoad):
			pass
		else:
			self.web.load(QUrl(url + 'pc98/' + self.screens[2]))
			self.web.setZoomFactor(1.0)
			self.SetButtonSelect(5)
	
	def SetButtonSelect(self, num):
		self.pic1.setFlat(False)
		self.pic2.setFlat(False)
		self.pic3.setFlat(False)
		self.scr1.setFlat(False)
		self.scr2.setFlat(False)
		self.scr3.setFlat(False)
		self.cvr.setFlat(False)

		if (num == 0):
			self.pic1.setFlat(True)
		elif (num == 1):
			self.pic2.setFlat(True)
		elif (num == 2):
			self.pic3.setFlat(True)
		elif (num == 3):
			self.scr1.setFlat(True)
		elif (num == 4):
			self.scr2.setFlat(True)
		elif (num == 5):
			self.scr3.setFlat(True)
		elif (num == 6):
			self.cvr.setFlat(True)
	
	def GetUrl(self):
		if (not self.gameLink):
			pass
		else:
			webbrowser.open(self.gameLink)

	def CopyJpTitle(self):
		if (not self.gameLink):
			pass
		else:
			copy = Tk()
			copy.withdraw()
			copy.clipboard_clear()
			copy.clipboard_append(self.titleJap)
			copy.destroy()
		
	def OpenNote(self):
		#note = self.doc.xpath('//*[@id="note"]')
		note = self.doc.cssselect('div#note, div#note_b')
		begin = '<html lang="ja"><head><title>PC98 Note</title><meta charset="utf-8"><link rel="stylesheet" href="https://refuge.tokyo/pc9801/pc9801.css"><link rel="stylesheet" href="https://refuge.tokyo/pc9801/pc98/css/note.css"><style>#note_b{margin:0!important}</style></head><body style="background-color:#000000;color:#f7f7f7; font-weight:bold; margin:0;">'
		end = '</body></html>'
		
		if (note):
			strnote = etree.tostring(note[0])
		strnoteUrl = str(strnote, 'utf-8').replace('src="','src="https://refuge.tokyo/pc9801/pc98/')
		file = open('note.html', 'w')
		file.write(begin)
		file.write(strnoteUrl)
		file.write(end)
		file.close
		
		filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), "note.html"))
		self.webnote.load(QUrl.fromLocalFile(filePath))
		self.notewin.setWindowTitle(self.titleEng + ' - Note')
		self.notewin.setGeometry(100, 50, 1280, 800)
		self.notewin.show()
			
	def keyPressEvent(self, event):
		if event.key() == Qt.Key_F1:
			self.about.setWindowTitle('About')
			self.about.setGeometry(QRect(600, 400, 320, 120))
			self.about.show()
			
	def closeEvent(self, event):
		if os.path.exists('note.html'):
			os.remove('note.html')
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	main = MainWindow()
	main.show()
	sys.exit(app.exec_())
