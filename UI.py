# AltServer-Linux GUI wrote in PyQT5
# This is the UI part
# Author of the GUI : powen

# import
from Main import *

HOME = os.path.expanduser("~")
AUTOSTART_PATH = os.path.join(HOME, ".config/autostart/AltServer.desktop")
IS_AUTOSTART = os.path.exists(AUTOSTART_PATH)

# check permission
if using_resource_altserver:
    if not os.access(AltServer, os.X_OK):
        subprocess.run(f"chmod +x {AltServer}", shell=True)
    if not os.access(AutoStart, os.X_OK):
        subprocess.run(f"chmod +x {AutoStart}", shell=True)

# UI part
app = QApplication(sys.argv)
app.setApplicationName("AltServer")
app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon(resource_path("MenuBar.png"))
app.setWindowIcon(QIcon(resource_path("AppIcon.png")))

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Create the menu
menu = QMenu()
About = QAction("About AltServer")
About.triggered.connect(about_message)
menu.addAction(About)
menu.addSeparator()

# Add Inatall AltStore option to the menu.
AltInstall = QAction("Install AltStore")
AltInstall.triggered.connect(Installation)
menu.addAction(AltInstall)
menu.addSeparator()

# Add Launch At Login in  option to the menu.
LaunchAtLogin = QAction("Launch at Login", checkable=True)
launch_enable = False
CheckTime = 0
if IS_AUTOSTART and CheckTime == 0:
    LaunchAtLogin.setChecked(True)
    launch_enable = True
    CheckTime = 1
if not IS_AUTOSTART and CheckTime == 0:
    LaunchAtLogin.setChecked(False)
    launch_enable = False
    CheckTime = 1


def launch_config():
    if LaunchAtLogin.isChecked():
        launch_enable = True
    if not LaunchAtLogin.isChecked():
        launch_enable = False
    if launch_enable:
        LaunchAtLogin.setChecked(True)
        subprocess.run(resource_path("AutoStart.sh"), shell=True)
    if not launch_enable:
        LaunchAtLogin.setChecked(False)
        os.remove(AUTOSTART_PATH)


LaunchAtLogin.toggled.connect(launch_config)
menu.addAction(LaunchAtLogin)

# Add Pair in  option to the menu.
Pair = QAction("Pair")
menu.addAction(Pair)
Pair.triggered.connect(pair)

# Add Restart Daemon in  option to the menu.
RestartDaemon = QAction("Restart AltDaemon")
menu.addAction(RestartDaemon)
RestartDaemon.triggered.connect(restart_daemon)
menu.addSeparator()

# Add Check Update option to the menu.
CheckUpdate = QAction("Check for Update")
CheckUpdate.triggered.connect(check_update)
menu.addAction(CheckUpdate)
menu.addSeparator()

# Add a Quit option to the menu.
def app_quit():
    subprocess.run(f"killall {AltServer}", shell=True)
    app.quit()


quit = QAction("Quit AltServer")
quit.triggered.connect(app_quit)
quit.setCheckable(False)
quit.setShortcut("Ctrl+Q")
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)
subprocess.run(f"{AltServer} &> /dev/null &", shell=True)
UpdateNotification()
app.exec_()
