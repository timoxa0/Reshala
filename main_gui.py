from PyQt6 import QtWidgets, QtCore, QtGui
from colorama import Fore, init
from ui import Ui_mainWindow
import qdarktheme
import darkdetect
import threading
import configctl
import langctl
import helper
import icon
import sys

init(autoreset=True)

def set_theme(theme: str):
    app.setStyleSheet(qdarktheme.load_stylesheet(theme.lower()))

lang_file = langctl.Lang('lang.json')
config_file = configctl.Config('config.json')
config = config_file.load()

t = threading.Thread(target=darkdetect.listener, args=(set_theme,))
t.daemon = True
t.start()

class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.settingsTabs.setCurrentIndex(0)
        self.iconfile = icon.iconFromBase64()
        self.setWindowIcon(self.iconfile)
        # Filling basic paramiters
        self.wgLoginEdit.setText(config['basic']['login'])
        self.wgPasswordEdit.setText(config['basic']['password'])
        self.delayTopSpinbox.setValue(config['basic']['toplimit'])
        self.delayDownSpinbox.setValue(config['basic']['downlimit'])
        # Filling ditionary paramiters
        self.dServerEdit.setText(config['dictionary']['server'])
        self.dCredsLoginEdit.setText(config['dictionary']['userID'])
        self.dCredsPasswordEdit.setText(config['dictionary']['userKey'])
        self.useDictComboBox.setCurrentIndex(config['dictionary']['use'])
        # Filling advanced paramiters
        self.logLevelComboBox.setCurrentIndex(self.logLevelComboBox.findText(config['advanced']['logLevel'], QtCore.Qt.MatchFlag.MatchFixedString))
        self.acComboBox.setCurrentIndex(config['advanced']['Always Continue'])
        self.chromeProcessEdit.setText(config['advanced']['chrome_process'])
        self.chromedriverProcessEdit.setText(config['advanced']['driver_process'])
        # Connecting buttons
        self.saveBtn.clicked.connect(self.exit_btn)
        self.startBtn.clicked.connect(self.start_btn)

        # Translate
        lang = lang_file.load()
        # Title
        self.setWindowTitle(lang['gui']['title'])
        # Buttons
        self.saveBtn.setText(lang['gui']['saveExitBtn'])
        self.startBtn.setText(lang['gui']['saveRunBtn'])
        # Basic Settings
        self.settingsTabs.setTabText(0, lang['gui']['basicSettings']['tabName'])
        self.wgLoginLabel.setText(lang['gui']['basicSettings']['loginLabel'])
        self.wgPasswordLabel.setText(lang['gui']['basicSettings']['passwordLabel'])
        self.delayLabel.setText(lang['gui']['basicSettings']['delayLabel'])
        self.delayDownLabel.setText(lang['gui']['basicSettings']['downDelayLimitLabel'])
        self.delayTopLabel.setText(lang['gui']['basicSettings']['topDelayLimitLabel'])
        # Dictionary Settings
        self.settingsTabs.setTabText(1, lang['gui']['dictionarySettings']['tabName'])
        self.dServerLabel.setText(lang['gui']['dictionarySettings']['serverIPLabel'])
        self.dCredsLoginLabel.setText(lang['gui']['dictionarySettings']['loginLabel'])
        self.dCredsPasswordLabel.setText(lang['gui']['dictionarySettings']['passwordLabel'])
        self.useDictLabel.setText(lang['gui']['dictionarySettings']['useDictionaryLabel'])
        self.useDictComboBox.setItemText(0, lang['gui']['other']['no'])
        self.useDictComboBox.setItemText(1, lang['gui']['other']['yes'])
        # Advanced Settings
        self.settingsTabs.setTabText(2, lang['gui']['advancedSettings']['tabName'])
        self.logLevelLabel.setText(lang['gui']['advancedSettings']['logLevelLabel'])
        self.acLabel.setText(lang['gui']['advancedSettings']['acLabel'])
        self.chromeProcessLabel.setText(lang['gui']['advancedSettings']['chromeProcessLabel'])
        self.chromedriverProcessLabel.setText(lang['gui']['advancedSettings']['driverProcessLabel'])
        self.acComboBox.setItemText(0, lang['gui']['other']['no'])
        self.acComboBox.setItemText(1, lang['gui']['other']['yes'])


    def save_cfg(self):
        config['basic']['login'] = self.wgLoginEdit.text()
        config['basic']['password'] = self.wgPasswordEdit.text()
        config['basic']['toplimit'] = self.delayTopSpinbox.value()
        config['basic']['downlimit'] = self.delayDownSpinbox.value()

        config['dictionary']['server'] = self.dServerEdit.text()
        config['dictionary']['userID'] = self.dCredsLoginEdit.text()
        config['dictionary']['userKey'] = self.dCredsPasswordEdit.text()
        config['dictionary']['use'] = self.useDictComboBox.currentIndex()

        config['advanced']['logLevel'] = self.logLevelComboBox.currentText()
        config['advanced']['Always Continue'] = self.acComboBox.currentIndex()
        config['advanced']['chrome_process'] = self.chromeProcessEdit.text()
        config['advanced']['driver_process'] = self.chromedriverProcessEdit.text()

        config_file.dump(config)


    def exit_btn(self):
        self.save_cfg()
        sys.exit(0)

 
    def start_btn(self):
        self.save_cfg()
        self.hide()
        try:
            helper.main(config)
        except Exception as ex:
            print(ex)
            sys.exit(-1)

app = QtWidgets.QApplication(sys.argv)
if darkdetect.isDark():
    app.setStyleSheet(qdarktheme.load_stylesheet())
else:
    app.setStyleSheet(qdarktheme.load_stylesheet('light'))

window = MainWindow()
window.show()
app.setWindowIcon(window.iconfile)
gui_started_msg = 'GUI started!'
print(Fore.RESET + '{GUI} INFO: ' + gui_started_msg)
app.exec()
