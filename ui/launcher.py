import sys
import os
import time
import subprocess
from Qt import QtCore, QtGui, QtWidgets
from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *

import shotgun_api3

import xLauncher_UI
sg = shotgun_api3.Shotgun('https://x.shotgunstudio.com',
                          script_name='shotgunUtils',
                          api_key='<key>')

oldPaths = []

xmlPath = None


class xLauncherWindow(QMainWindow):
    def __init__(self, parent=QtWidgets.QApplication.activeWindow()):
        """
        Initializes UI
        """
        super(xLauncherWindow, self).__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # dev or published piperoot
        self.env = sys.argv[-1]

        self.application = sys.argv[-1].lower()
        self.loadModules(modules=['envTools', 'xmlTools'])
        self.setXMLpath()
        self.setShow()

        # The PIPEROOT is always Q:/PUBLISHED unless you're in dev mode (In case it needs to change, enable this)
        # self.setShowPiperoot()
        self.loadModules()

        # Populate the show combo menu
        active_shows = sg.find('Project', [['sg_status', 'is', 'active']], ['code'])
        shows = sorted([i['code'] for i in active_shows])

        # Dicts for the icon, logo label, and window name
        iconDict = {
            'nuke': '%s/apps/windows/icons/xNuke.png' % os.environ['PIPEROOT'],
            'nukex': '%s/apps/windows/icons/xNukeX.png' % os.environ['PIPEROOT'],
            'nukeassist': '%s/apps/windows/icons/xNukeAssist2.png' % os.environ['PIPEROOT'],
            'maya': '%s/apps/windows/icons/xMaya.png' % os.environ['PIPEROOT'],
            'rv': '%s/apps/windows/icons/xRV.png' % os.environ['PIPEROOT']
        }
        nameDict = {
            'nuke': 'X Nuke',
            'nukex': 'X NukeX',
            'nukeassist': 'X Nuke Assist',
            'maya': 'X Maya',
            'rv': 'X RV'
        }

        # Import the compiled ui
        self.ui = xLauncher_UI.Ui_applicationLauncherMainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(standardStyleSheet.get())

        # Set icons and window names
        self.icon = QIcon()
        self.icon.addPixmap(iconDict[self.application])
        self.setWindowIcon(self.icon)
        self.ui.iconLabel.setPixmap(iconDict[self.application])
        self.setWindowTitle(nameDict[self.application])

        # Populate show combo box and set the current show value
        self.ui.showComboBox.addItems(shows)
        showIdx = self.ui.showComboBox.findText(os.environ['SHOW'], QtCore.Qt.MatchFixedString)
        self.ui.showComboBox.setCurrentIndex(showIdx)

        # Set env for currently selected show
        self.setForShow()
        self.ui.showComboBox.currentIndexChanged.connect(self.setForShow)

        # Get application versions
        # self.getVersions()

        # Hook up buttons
        self.ui.openPushButton.clicked.connect(self.launchApp)
        self.ui.helpPushButton.clicked.connect(self.helpPopup)

        # Pressing return launches app
        self.openApp = QtWidgets.QAction(self)  # create action
        self.openApp.setShortcut(QKeySequence(Qt.Key_Return))  # set shortcut key for that action
        self.ui.applicationLauncherCentralwidget.addAction(self.openApp)  # assign action to central widget
        self.openApp.triggered.connect(self.launchApp)

    def setShow(self):
        envDict = self.getEnvXML()
        if envDict:
            os.environ['SHOW'] = envDict['SHOW']
        else:
            os.environ['SHOW'] = 'common'

        print "SHOW IS: ", os.environ['SHOW']

    def setXMLpath(self):
        # Get launcher env xml path and create if missing
        self.user = envTools.getUser()
        self.xmlPath = ('C:/Users/' + self.user + "/AppData/Roaming/X/launcherEnv.config")
        if not os.path.isfile(self.xmlPath):
            self.createEnvXML()

    # def setShowPiperoot(self):
    #     """
    #     Sets PIPEROOT env based on argument received on launch
    #     """
    #     showConfigPiperoot = 'Q:/PUBLISHED/'
    #     configPiperoot = envTools.getShowConfigAttr(show=os.environ['SHOW'],
    #                                                 element='mounts',
    #                                                 attr='PIPEROOT')
    #     if os.path.exists(configPiperoot):
    #         showConfigPiperoot = configPiperoot
    #
    #     if ((self.env == 'dev') and not (showConfigPiperoot == "Q:/PUBLISHED/")) or self.env == 'live':
    #         os.environ['PIPEROOT'] = showConfigPiperoot
    #
    #     print "SHOW PIPEROOT IS: ", os.environ['PIPEROOT']

    def createEnvXML(self):
        """
        Creates user XML file to save last opened show env for each application
        """
        try:
            nuke = {"SHOW": "common", "SEQ": "", "SHOT": ""}
            nukex = {"SHOW": "common", "SEQ": "", "SHOT": ""}
            nukeassist = {"SHOW": "common", "SEQ": "", "SHOT": ""}
            maya = {"SHOW": "common", "SEQ": "", "SHOT": ""}
            rv = {"SHOW": "common", "SEQ": "", "SHOT": ""}

            elements = {}
            elements['0'] = 'maya'
            elements['1'] = 'nuke'
            elements['2'] = 'nukex'
            elements['3'] = 'nukeassist'
            elements['4'] = 'rv'

            data = [elements, maya, nuke, nukex, nukeassist, rv]

            xmlDir = self.xmlPath.replace("launcherEnv.config", "")

            if not os.path.exists(xmlDir):
                os.mkdir(xmlDir)

            xmlTools.writeDataXml(data, self.xmlPath, rootElement="enviromnentDefault")
        except Exception, e:
            print "Warning: could not create env XML at %s" % xmlPath
            print(repr(e))

    def getEnvXML(self):
        """
        Gets the env from XML file when launcher is opened
        """
        try:
            return xmlTools.getXmlElementDict(self.xmlPath, self.application)
        except Exception, e:
            print "Warning: could not find env XML at %s" % self.xmlPath
            print(repr(e))

    def updateEnvXML(self, app, show, seq, shot):
        """
        Updates the XML file every time an application is launched
        :param app: application
        :param show: show env var, can be "" if no value needed
        :param seq: sequence env var, can be "" if no value needed
        :param shot: shot env var, can be "" if no value needed
        """
        try:
            nuke = xmlTools.getXmlElementDict(self.xmlPath, 'nuke')
            nukex = xmlTools.getXmlElementDict(self.xmlPath, 'nukex')
            nukeassist = xmlTools.getXmlElementDict(self.xmlPath, 'nukeassist')
            maya = xmlTools.getXmlElementDict(self.xmlPath, 'maya')
            rv = xmlTools.getXmlElementDict(self.xmlPath, 'rv')

            if app == 'maya':
                maya = {"SHOW": show, "SEQ": seq, "SHOT": shot}
            if app == 'nuke':
                nuke = {"SHOW": show, "SEQ": seq, "SHOT": shot}
            if app == 'nukex':
                nukex = {"SHOW": show, "SEQ": seq, "SHOT": shot}
            if app == 'nukeassist':
                nukeassist = {"SHOW": show, "SEQ": seq, "SHOT": shot}
            if app == 'rv':
                rv = {"SHOW": show, "SEQ": seq, "SHOT": shot}

            elements = {}
            elements['0'] = 'maya'
            elements['1'] = 'nuke'
            elements['2'] = 'nukex'
            elements['3'] = 'nukeassist'
            elements['4'] = 'rv'

            data = [elements, maya, nuke, nukex, nukeassist, rv]

            xmlTools.writeDataXml(data, self.xmlPath, rootElement="enviromnentDefault")
        except Exception, e:
            print "Warning: could not update env XML at %s" % xmlPath
            print(repr(e))

    def loadModules(self, modules=[
        'xLauncher_UI','standardStyleSheet','envTools','appsVersions','xEnvironment', 'xmlTools']):
        """
        Reloads modules based on current environment
        """
        global oldPaths

        # piperoot was prob changed
        # first remove old paths
        for p in oldPaths:
            idx = sys.path.index(p)
            if idx:
                del sys.path[idx]

        newPaths = [os.path.join(os.environ['PIPEROOT'], 'apps', 'python', '2.7', 'pipeline'),
                    os.path.join(os.environ['PIPEROOT'], 'apps', 'python', '2.7', 'pipeline', 'info'),
                    os.path.join(os.environ['PIPEROOT'], 'apps', 'python', '2.7', 'xLauncher'),
                    os.path.join(os.environ['PIPEROOT'], 'apps', 'python', '2.7', 'common')]

        for p in newPaths:
            sys.path.insert(1, p)
        oldPaths = sys.path

        for m in modules:
            if m in sys.modules:
                del sys.modules[m]
            globals()[m] = __import__(m)
            exec 'print %s.__file__' %m

        print envTools.__file__
        print ("+" * 100)

    def setForShow(self):
        """
        Sets environment based on current show
        """
        print "DEFAULT SHOW: ", os.environ['SHOW']

        os.environ['SHOW'] = self.ui.showComboBox.currentText()
        print "+++++++++++++++++++++++++++++++++++++++++++++++++"
        print "SELECTED SHOW: ", os.environ['SHOW']
        print "+++++++++++++++++++++++++++++++++++++++++++++++++"

        # reset shows piperoot
        xEnvironment.setEnvVars(['scv'])

        # get piperoot for show from showconfig
        # self.setShowPiperoot()

        # self.loadModules()
        self.getVersions()

    def getVersions(self):
        """
        Gets all versions found in xEnvironment that are on the machine. Populates the version combo box
        and sets the index to the show version specified in the showConfig.
        """
        self.allVersions = appsVersions.getAppPaths(self.application, getShowVers=False)
        self.showVersion = appsVersions.getAppPaths(self.application, getShowVers=True)

        try:
            self.showVersion = self.showVersion[self.showVersion.keys()[0]].keys()[0]
        except:
            self.showVersion = ""
            print "Show version not on machine"

        keys = self.allVersions.keys()
        versions = []

        for key in keys:
            version = self.allVersions[key].keys()[0]
            if version == self.showVersion:
                version = version + "- show version"
            versions.append(version)

        if (self.showVersion + "- show version") not in versions:
            print "WARNING: Show version not found on machine, setting version to highest existing version"
            QtWidgets.QMessageBox.warning(self, "Warning", "Software version for show was not found on this machine,"
                                                           " please select an available version.")
            versions.insert(0, "Select Version")
            self.showVersion = "Select Version"

        self.ui.versionComboBox.clear()
        self.ui.versionComboBox.addItems(versions)

        if self.showVersion == "Select Version":
            versionIdx = self.ui.versionComboBox.findText(self.showVersion, QtCore.Qt.MatchFixedString)
        else:
            versionIdx = self.ui.versionComboBox.findText(
                self.showVersion + "- show version", QtCore.Qt.MatchFixedString)

        self.ui.versionComboBox.setCurrentIndex(versionIdx)

    def launchApp(self):
        """
        Sets the env vars and launches the application
        """

        envTools.updateEnvXML(self.xmlPath, self.application, os.environ['SHOW'], "", "")
        keys = self.allVersions.keys()
        path = ""

        for key in keys:
            version = self.allVersions[key].keys()[0]
            if version == self.ui.versionComboBox.currentText().replace("- show version", ""):
                appVersion = version
                path = self.allVersions[key][version]


        if 'maya' in self.application:
            os.environ["MAYA_VERSION"] = appVersion
        if 'nuke' in self.application:
            os.environ["NUKE_VERSION"] = appVersion
        if 'rv' in self.application:
            os.environ["RV_VERSION"] = appVersion

        print os.environ["SHOW"]
        print "SETTING software environment variables"
        xEnvironment.setEnvVars(['smv', 'sav'])
        print os.environ["SHOW"]

        app_exe=[path]
        if self.application in ["nukex", "nukeassist", "studio"]:
            app_exe.append('-%s' %self.application)

        if path == "":
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a software version.")
            return
        time.sleep(1)

        print '+' * 50
        for i in sys.path:
            print i
        print '+' * 50
        print os.environ['DEADLINE_PATH']
        print os.environ['DEADLINE_REPOSITORY_PATH']
        print os.environ['DEADLINE_VERSION']

        subprocess.Popen(app_exe)
        QApplication.quit()

    def helpPopup(self):
        """
        Displays popup information box with instructions on using the launcher
        """
        helpMessage = "Welcome to the X Application Launcher!\n\nSelect your show from the combo box or just start " \
                      "typing the show code to automatically  set the show.\n\nPress the 'Launch' button or hit " \
                      "Enter to launch your application.\n\nBy default, the application version will be set to the " \
                      "show version. If you need to use another version you may selected from the version menu."
        QtWidgets.QMessageBox.information(self, "Help", helpMessage)


def main(args):

    app = QtWidgets.QApplication(args)
    elmWin = xLauncherWindow()
    elmWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)