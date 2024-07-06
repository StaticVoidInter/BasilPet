import sys
import os
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *


class Basil(QWidget):

    # 初始化一只Basil
    def __init__(self, parent=None):
        super(Basil, self).__init__(parent)

        # 将窗口设置为透明、无边框、置于顶层
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        self.rightClickable = True

        # 将窗口移动到屏幕右下角
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() + 256, screen.height() - self.height() + 128)

        # 初始化图片
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Empty.png"))
        self.image = QLabel(self)
        self.image.setPixmap(QPixmap.fromImage(image))
        self.resize(352, 256)

        # 初始化计时器和播放器
        self.timer = QTimer(self)
        self.gifTimer = QTimer(self)
        self.soundPlayer = QSoundEffect(self)

        # 初始化情绪状态GIF窗口
        self.emoGif = QWidget(self)
        self.emoGif.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.emoGif.setAutoFillBackground(False)
        self.emoGif.setAttribute(Qt.WA_TranslucentBackground, True)
        self.emoGif.repaint()
        layout = QVBoxLayout(self.emoGif)
        self.emoGifLabel = QLabel(self.emoGif)
        layout.addWidget(self.emoGifLabel)
        self.emoGif.move(176, 64)
        self.emoGifMovie = QMovie(os.path.join(os.path.dirname(__file__), "Images", "Emotion", "Neutral.gif"))
        self.emoGifLabel.setMovie(self.emoGifMovie)
        self.emoGifMovie.start()
        self.emoGif.show()

        self.emoGif2 = QWidget(self)
        self.emoGif2.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.emoGif2.setAutoFillBackground(False)
        self.emoGif2.setAttribute(Qt.WA_TranslucentBackground, True)
        self.emoGif2.repaint()
        layout2 = QVBoxLayout(self.emoGif2)
        self.emoGifLabel2 = QLabel(self.emoGif2)
        layout2.addWidget(self.emoGifLabel2)
        self.emoGif2.move(176, 64)
        self.emoGifMovie2 = QMovie(os.path.join(os.path.dirname(__file__), "Images", "Emotion", "Neutral.gif"))
        self.emoGifLabel2.setMovie(self.emoGifMovie2)
        self.emoGifMovie2.start()
        self.emoGif2.show()

        self.runningGif = 1

        # 初始化动画列表
        self.autoAnimationList = [self.sleepAnimation, self.tumble, self.breaktime, self.swing, self.wander, self.book, self.camera, self.flower, self.princess, self.dontIgnoreMe]
        self.autoAnimationNameList = ["睡觉", "跌倒", "坐下休息", "荡秋千", "走来走去", "看书", "拍照", "浇花", "公主抱", "不要无视我"]

        self.realAnimationList = [self.lightbulb, self.realWander, self.hug, self.umbrella, self.realBook, self.realCamera, self.realFlower]
        self.realAnimationNameList = ["小夜灯", "走来走去", "贴贴", "撑伞", "看书", "拍照", "浇花"]

        # 初始化交互标记，每30秒未与Basil交互，则自动播放一个动画
        self.interactedTimer = QTimer(self)
        self.interactedTimer.timeout.connect(self.randomAction)
        self.interactedTimer.start(30000)

        # 初始化是否显示情绪
        self.emotionAction = QAction("显示情绪", self, checkable=True)
        self.emotionAction.toggled.connect(self.setEmotionVisible)
        self.emotionAction.setChecked(True)

        # 初始化是否播放声音
        self.soundAction = QAction("播放声音", self, checkable=True)
        self.soundAction.setChecked(True)
        self.soundAction.toggled.connect(self.setSound)

        # 初始化形态
        self.characterActionGroup = QActionGroup(self)
        self.characterActionGroup.setExclusive(True)
        self.dreamAction = QAction("梦境", self, checkable=True)
        self.realAction = QAction("现实", self, checkable=True)
        self.characterActionGroup.addAction(self.dreamAction)
        self.characterActionGroup.addAction(self.realAction)
        self.character = "Dream"
        self.dreamAction.triggered.connect(self.dreamActionTriggered)
        self.dreamAction.setChecked(True)
        self.realAction.triggered.connect(self.realActionTriggered)

        # 初始化生命状态
        self.alive = True
        self.somethingGrabbed = False

        # 开始动画
        self.show()
        self.startAnimation()

    # 随机播放动画
    def randomAction(self):
        if (not self.alive or self.somethingGrabbed): return
        self.soundPlayer.stop()
        if (self.dreamAction.isChecked()):
            random.choice(self.autoAnimationList)()
        else:
            random.choice(self.realAnimationList)()

    # 设置窗口左键可以拖动、右键呼出菜单
    def mousePressEvent(self, event):
        self.interactedTimer.start(30000)
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        elif (event.button() == Qt.RightButton and self.rightClickable):
            self.showContextMenu()

    def mouseMoveEvent(self, event):
        self.interactedTimer.start(30000)
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    # 设置是否显示情绪
    def setEmotionVisible(self):
        self.emoGif.setVisible(self.emotionAction.isChecked())
        self.emoGif2.setVisible(self.emotionAction.isChecked())

    # 设置切换梦境和现实形态
    def dreamActionTriggered(self):
        if (self.character == "Dream"):
            return
        self.alive = True
        self.character = "Dream"
        self.startAnimation()

    def realActionTriggered(self):
        if (self.character == "Real"):
            return
        self.alive = True
        self.character = "Real"
        self.realStart()

    # 设置情绪状态
    def setEmotion(self, emotion):
        self.emoGif.move(176, 64)
        self.emoGif2.move(176, 64)

        if (emotion == "Toast" or emotion == "RealDead"):
            self.dieSound()

        if (self.dreamAction.isChecked() and not emotion in ["LightbulbAfraid", "Faceless", "Something"]):
            filepath = os.path.join(os.path.dirname(__file__), "Images", "Emotion", f"{emotion}.gif")
        else:
            filepath = os.path.join(os.path.dirname(__file__), "Images", "Emotion", f"{emotion}.png")

        opacityUp = QGraphicsOpacityEffect()
        self.animationUp = QPropertyAnimation(opacityUp, b"opacity")
        self.animationUp.setDuration(400)
        self.animationUp.setStartValue(0)
        self.animationUp.setEndValue(1)

        opacityDown = QGraphicsOpacityEffect()
        self.animationDown = QPropertyAnimation(opacityDown, b"opacity")
        self.animationDown.setDuration(400)
        self.animationDown.setStartValue(1)
        self.animationDown.setEndValue(0)

        if (self.runningGif == 1):
            self.runningGif = 2
            self.emoGifMovie2 = QMovie(filepath)
            self.emoGifLabel2.setMovie(self.emoGifMovie2)
            self.emoGifLabel.setGraphicsEffect(opacityDown)
            self.emoGifLabel2.setGraphicsEffect(opacityUp)
            self.emoGifMovie2.start()
            self.animationDown.start()
            self.animationUp.start()
        else:
            self.runningGif = 1
            self.emoGifMovie = QMovie(filepath)
            self.emoGifLabel.setMovie(self.emoGifMovie)
            self.emoGifLabel2.setGraphicsEffect(opacityDown)
            self.emoGifLabel.setGraphicsEffect(opacityUp)
            self.emoGifMovie.start()
            self.animationDown.start()
            self.animationUp.start()

    # 设置声音是否播放
    def setSound(self):
        if (self.soundAction.isChecked()):
            self.soundPlayer.setVolume(100)
        else:
            self.soundPlayer.setVolume(0)

    # 播放死亡音效
    def dieSound(self):
        """这一段中最后一个是玩笑，在v1.0.2中禁用
        choice = random.randint(0, 2)
        if (choice == 0):
            self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "Something_Disappears.wav")))
        elif (choice == 1):
            self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "Creepy_Tune.wav")))
        else:
            self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "Oyasumi.wav")))
        """
        choice = random.randint(0, 1)
        if (choice == 0):
            self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "Something_Disappears.wav")))
        else:
            self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "Creepy_Tune.wav")))
        self.soundPlayer.setLoopCount(1)
        self.soundPlayer.play()

    # 右键菜单
    def showContextMenu(self):
        menu = QMenu(self)

        startAction = QAction("小可爱探头", self)
        startAction.triggered.connect(self.startAnimation)
        menu.addAction(startAction)
        if ((not self.alive) or (not self.dreamAction.isChecked()) or self.somethingGrabbed): startAction.setVisible(False)
        act1 = QAction("重置", self)
        act1.triggered.connect(self.resetImage)
        menu.addAction(act1)
        if ((not self.alive) or (not self.dreamAction.isChecked()) or self.somethingGrabbed): act1.setVisible(False)

        realStartAction = QAction("小可爱出现", self)
        realStartAction.triggered.connect(self.realStart)
        menu.addAction(realStartAction)
        if ((not self.alive) or self.dreamAction.isChecked() or self.somethingGrabbed): realStartAction.setVisible(False)
        actReal1 = QAction("重置", self)
        actReal1.triggered.connect(self.realImage)
        menu.addAction(actReal1)
        if ((not self.alive) or self.dreamAction.isChecked() or self.somethingGrabbed): actReal1.setVisible(False)

        menu.addSeparator()

        for i in range(0, len(self.autoAnimationList)):
            if (self.autoAnimationNameList[i] != "不要无视我"):
                act = QAction(self.autoAnimationNameList[i], self)
                act.triggered.connect(self.autoAnimationList[i])
                menu.addAction(act)
                if ((not self.alive) or (not self.dreamAction.isChecked()) or self.somethingGrabbed): act.setVisible(False)

        for i in range(0, len(self.realAnimationList)):
            act = QAction(self.realAnimationNameList[i], self)
            act.triggered.connect(self.realAnimationList[i])
            menu.addAction(act)
            if ((not self.alive) or self.dreamAction.isChecked() or self.somethingGrabbed): act.setVisible(False)

        if (self.dreamAction.isChecked() and self.alive and (not self.somethingGrabbed)):
            menu.addSeparator()
            actPicnic = QAction("投喂", self)
            actPicnic.triggered.connect(self.picnic)
            menu.addAction(actPicnic)
            actAnnoy = QAction("喇叭筒", self)
            actAnnoy.triggered.connect(self.annoy)
            menu.addAction(actAnnoy)
            actRain = QAction("雨云", self)
            actRain.triggered.connect(self.rain)
            menu.addAction(actRain)

        menu.addSeparator()

        actRedhand = QAction("红手", self)
        actRedhand.triggered.connect(self.redhand)
        menu.addAction(actRedhand)
        if ((not self.alive) or (not self.dreamAction.isChecked()) or self.somethingGrabbed): actRedhand.setVisible(False)

        actDrag = QAction("拖走", self)
        actDrag.triggered.connect(self.drag)
        menu.addAction(actDrag)
        if ((not self.alive) or (not self.dreamAction.isChecked()) or self.somethingGrabbed): actDrag.setVisible(False)

        actCut = QAction("切开", self)
        actCut.triggered.connect(self.cut)
        menu.addAction(actCut)
        if ((not self.alive) or (not self.dreamAction.isChecked()) or self.somethingGrabbed): actCut.setVisible(False)

        actWatermelon = QAction("西瓜", self)
        actWatermelon.triggered.connect(self.watermelon)
        menu.addAction(actWatermelon)
        if ((not self.alive) or (not self.dreamAction.isChecked()) or self.somethingGrabbed): actWatermelon.setVisible(False)

        actSomething = QAction("某个东西", self)
        actSomething.triggered.connect(self.something)
        menu.addAction(actSomething)
        if ((not self.alive) or (not self.dreamAction.isChecked()) or self.somethingGrabbed): actSomething.setVisible(False)

        actSomethingKill = QAction("吞没", self)
        actSomethingKill.triggered.connect(self.somethingKill)
        if (self.somethingGrabbed): menu.addAction(actSomethingKill)

        actSomethingLetgo = QAction("放开", self)
        actSomethingLetgo.triggered.connect(self.somethingLetgo)
        if (self.somethingGrabbed): menu.addAction(actSomethingLetgo)

        actElevator = QAction("电梯", self)
        actElevator.triggered.connect(self.elevator)
        menu.addAction(actElevator)
        if ((not self.alive) or (not self.dreamAction.isChecked()) or self.somethingGrabbed): actElevator.setVisible(False)

        actLifejam = QAction("生命果酱", self)
        actLifejam.triggered.connect(self.lifejam)
        menu.addAction(actLifejam)
        if (self.alive or (not self.dreamAction.isChecked())): actLifejam.setVisible(False)

        actDrown = QAction("推到水里", self)
        actDrown.triggered.connect(self.drown)
        menu.addAction(actDrown)
        if ((not self.alive) or self.dreamAction.isChecked()): actDrown.setVisible(False)

        actFakeLifejam = QAction("生命果酱", self)
        actFakeLifejam.triggered.connect(self.fakeLifejam)
        menu.addAction(actFakeLifejam)
        if (self.alive or self.dreamAction.isChecked()): actFakeLifejam.setVisible(False)

        menu.addSeparator()

        characterMenu = QMenu("切换形态", self)
        characterMenu.addAction(self.dreamAction)
        characterMenu.addAction(self.realAction)
        if (not self.somethingGrabbed): menu.addMenu(characterMenu)
        menu.addAction(self.emotionAction)
        menu.addAction(self.soundAction)
        exitAction = QAction("退出", self)
        exitAction.triggered.connect(lambda: sys.exit())
        menu.addAction(exitAction)

        menu.exec_(QCursor.pos())


    # 以下为各种动画
    # 所有动画统一使用self.timer，开头都需要self.timer.stop()以避免冲突，
    # 并self.setEmotion()重置情绪状态、self.interactedTimer.start()重置交互标记


    # 重置图片为站立Basil
    def resetImage(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.soundPlayer.stop()
        self.setEmotion("Neutral")
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Dream_Basil.png"))
        self.image.setPixmap(QPixmap.fromImage(image))

    # 开始动画
    def startAnimation(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("Neutral")
        self.timer = QTimer(self)
        self.startPic = 0
        self.startPic7 = False
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Start", "Start_0_0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer.timeout.connect(self.updateStart)
        self.timer.start(400)

    def updateStart(self):
        self.timer.stop()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateStart)
        self.startPic += 1
        filename = f"Start_{self.startPic//3}_{self.startPic%3}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Start", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        if (self.startPic == 1):
            self.timer.start(400)
        elif (self.startPic == 7):
            if (not self.startPic7):
                self.startPic7 = True
                self.startPic -= 2
                self.timer.start(750)
            else:
                self.timer.start(200)
        elif (self.startPic == 13):
            self.timer.stop()
            image = QImage()
            image.load(os.path.join(os.path.dirname(__file__), "Images", "Dream_Basil.png"))
            self.image.setPixmap(QPixmap.fromImage(image))
        else:
            self.timer.start(120)

    # 现实Basil开始动画
    def realStart(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("RealSmileOpen")
        self.timer = QTimer(self)
        self.realStartPic = 1
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Appear", "0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer.timeout.connect(self.updateRealStart)
        self.timer.start(800)

    def updateRealStart(self):
        filename = f"{self.realStartPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Appear", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.realStartPic += 1
        if (self.realStartPic == 5):
            self.timer.stop()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.realImage)
            self.timer.start(200)

    # 不要无视我
    def dontIgnoreMe(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("Injured")
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "DontIgnoreMe.png"))
        self.image.setPixmap(QPixmap.fromImage(image))

    # 上床睡觉
    def sleepAnimation(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("Neutral")
        self.sleepPic = 0
        self.timer = QTimer(self)
        self.timer.start(200)
        self.timer.timeout.connect(self.updateSleep)

    def updateSleep(self):
        if (self.sleepPic == 5):
            self.timer.stop()
            self.timer = QTimer(self)
            self.timer.start(1000)
            self.timer.timeout.connect(self.circulateSleep)
        else:
            filename = f"Sleep_{self.sleepPic}.png"
            image = QImage()
            image.load(os.path.join(os.path.dirname(__file__), "Images", "Sleep", filename))
            self.image.setPixmap(QPixmap.fromImage(image))
            self.sleepPic += 1

    def circulateSleep(self):
        filename = f"Sleep_{self.sleepPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Sleep", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.sleepPic = 9 - self.sleepPic

    # 跌倒
    def tumble(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("Injured")
        self.tumblePic = 0
        self.timer = QTimer(self)
        self.timer.start(200)
        self.timer.timeout.connect(self.updateTumble)

    def updateTumble(self):
        filename = f"Tumble_{self.tumblePic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Tumble", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.tumblePic += 1
        if (self.tumblePic == 11):
            self.timer.stop()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateTumble)
            self.timer.start(4000)
        elif (self.tumblePic == 12):
            self.resetImage()

    # 荡秋千
    def swing(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("Happy")
        self.swingPic = 1
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Swing", "Swing_1.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.updateSwing)
    
    def updateSwing(self):
        self.swingPic += 1
        filename = f"Swing_{self.swingPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Swing", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        if (self.swingPic == 15):
            self.swingPic = 0

    # 坐下来休息
    def breaktime(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("Happy")
        self.breaktimePic = 1
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Breaktime", "Breaktime_0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer = QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(self.updateBreaktime)
    
    def updateBreaktime(self):
        filename = f"Breaktime_{self.breaktimePic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Breaktime", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.breaktimePic = (self.breaktimePic + 1) % 4

    # 走来走去
    def wander(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.resetImage()
        self.wanderPic = 1
        self.timer = QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(self.updateWander)

    def updateWander(self):
        filename = f"{self.wanderPic%16+1}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Wander", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.wanderPic = self.wanderPic + 1
        if (self.wanderPic == 17): self.wanderPic = 1

    # 看书
    def book(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("Neutral")
        self.bookPic = 0
        self.resetImage()
        self.timer = QTimer(self)
        self.timer.start(400)
        self.timer.timeout.connect(self.updateBook)
    
    def updateBook(self):
        filename = f"{self.bookPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Book", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.bookPic += 1

        if (self.bookPic == 3):
            self.timer.start(900)
        elif (self.bookPic == 5 or self.bookPic == 7):
            self.timer.start(1600)
        elif (self.bookPic == 8):
            self.timer.stop()
        else:
            self.timer.start(400)

    # 拍照
    def camera(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("Neutral")
        self.cameraPic = 0
        self.resetImage()
        self.timer = QTimer(self)
        self.timer.start(400)
        self.timer.timeout.connect(self.updateCamera)

    def updateCamera(self):
        filename = f"{self.cameraPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Camera", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.cameraPic += 1

        if (self.cameraPic == 3):
            self.timer.start(900)
        elif (self.cameraPic == 5):
            self.timer.start(2000)
        elif (self.cameraPic == 6):
            self.timer.stop()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.resetImage)
            self.timer.start(6000)
        else:
            self.timer.start(400)

    # 浇花
    def flower(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("Happy")
        self.emoGif.move(224, 64)
        self.emoGif2.move(224, 64)
        self.flowerPic = 1
        choice = random.randint(0, 2)
        if (choice == 0):
            self.flowerChoice = "Tulip"
        elif (choice == 1):
            self.flowerChoice = "Sunflower"
        else:
            self.flowerChoice = "Lily"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", self.flowerChoice, "0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFlower)
        self.timer.start(2000)

    def updateFlower(self):
        filename = f"{self.flowerPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", self.flowerChoice, filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.flowerPic += 1
        if (self.flowerPic == 4):
            self.timer.stop()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.resetImage)
            self.timer.start(6000)

    # 公主抱
    def princess(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("Happy")
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Princess", "0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.princessEnd = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePrincess)
        self.timer.start(2000)

    def updatePrincess(self):
        if (not self.princessEnd):
            image = QImage()
            image.load(os.path.join(os.path.dirname(__file__), "Images", "Princess", "1.png"))
            self.image.setPixmap(QPixmap.fromImage(image))
            self.timer.start(6000)
            self.princessEnd = True
        else:
            self.timer.stop()
            self.resetImage()

    # 投喂
    def picnic(self):
        self.timer.stop()
        self.interactedTimer.start(30000)
        self.breaktime()
        self.soundPlayer.stop()
        self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "Picnic.wav")))
        self.soundPlayer.setLoopCount(1)
        self.soundPlayer.play()

    # 喇叭筒
    def annoy(self):
        self.timer.stop()
        self.interactedTimer.start(30000)
        self.setEmotion("Angry")
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Dream_Basil.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.soundPlayer.stop()
        self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "Airhorn.wav")))
        self.soundPlayer.setLoopCount(1)
        self.soundPlayer.play()

    # 雨云
    def rain(self):
        self.timer.stop()
        self.interactedTimer.start(30000)
        self.setEmotion("Sad")
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Dream_Basil.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.soundPlayer.stop()
        self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "RainCloud.wav")))
        self.soundPlayer.setLoopCount(1)
        self.soundPlayer.play()

    # 红手
    def redhand(self):
        self.interactedTimer.stop()
        self.timer.stop()
        self.setEmotion("Afraid")
        self.alive = False
        self.redhandPic = 1
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Redhand", "Redhand_0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer = QTimer(self)
        self.timer.start(400)
        self.timer.timeout.connect(self.updateRedhand)

    def updateRedhand(self):
        if (self.redhandPic == 4):
            self.setEmotion("Miserable")
        elif (self.redhandPic == 10):
            self.setEmotion("Toast")
        filename = f"Redhand_{self.redhandPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Redhand", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.redhandPic += 1
        if (self.redhandPic == 12):
            self.timer.stop()

    # 拖走
    def drag(self):
        self.interactedTimer.stop()
        self.timer.stop()
        self.setEmotion("Afraid")
        self.alive = False
        self.dragPic = 1
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Drag", "Drag_0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer = QTimer(self)
        self.timer.start(350)
        self.timer.timeout.connect(self.updateDrag)

    def updateDrag(self):
        if (self.dragPic == 4):
            self.setEmotion("Miserable")
        elif (self.dragPic == 9):
            self.setEmotion("Toast")
        filename = f"Drag_{self.dragPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Drag", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.dragPic += 1
        if (self.dragPic == 10):
            self.timer.stop()

    # 切开
    def cut(self):
        self.interactedTimer.stop()
        self.timer.stop()
        self.resetImage()

        self.soundPlayer.stop()
        self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "56122.wav")))
        self.soundPlayer.setLoopCount(QSoundEffect.Infinite)
        self.soundPlayer.play()

        step1 = QMessageBox(self)
        step1.setWindowTitle("贝瑟尔最近非常、非常不听话")
        step1.setText("贝瑟尔盯着你看。他不知道正在发生什么。\n你想切开贝瑟尔吗?")
        step1.setIcon(QMessageBox.Question)
        step1.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        step1.move(self.x() - 16, self.y() - 120)
        ret1 = step1.exec()
        if (ret1 == QMessageBox.No):
            self.interactedTimer.start(30000)
            self.soundPlayer.stop()
            self.resetImage()
            return
        else:
            step2 = QMessageBox(self)
            step2.setWindowTitle("贝瑟尔最近非常、非常不听话")
            step2.setText("贝瑟尔盯着你看。他好奇地歪着头。\n你想切开贝瑟尔吗?")
            step2.setIcon(QMessageBox.Question)
            step2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            step2.move(self.x() - 16, self.y() - 120)
            ret2 = step2.exec()
            if (ret2 == QMessageBox.No):
                self.interactedTimer.start(30000)
                self.soundPlayer.stop()
                self.resetImage()
                return
            else:
                self.setEmotion("Afraid")
                step3 = QMessageBox(self)
                step3.setWindowTitle("贝瑟尔最近非常、非常不听话")
                step3.setText("贝瑟尔盯着你看。他的双眼睁大了。他现在想离开这里。\n你想切开贝瑟尔吗?")
                step3.setIcon(QMessageBox.Question)
                step3.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                step3.move(self.x() - 64, self.y() - 120)
                ret3 = step3.exec()
                if (ret3 == QMessageBox.No):
                    self.interactedTimer.start(30000)
                    self.soundPlayer.stop()
                    self.resetImage()
                    return
                else:
                    step4 = QMessageBox(self)
                    step4.setWindowTitle("贝瑟尔最近非常、非常不听话")
                    step4.setText("贝瑟尔盯着你看。他挣扎着想挣脱。\n你想切开贝瑟尔吗?")
                    step4.setIcon(QMessageBox.Question)
                    step4.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    step4.move(self.x() - 16, self.y() - 120)
                    ret4 = step4.exec()
                    if (ret4 == QMessageBox.No):
                        self.interactedTimer.start(30000)
                        self.soundPlayer.stop()
                        self.resetImage()
                        return
                    else:
                        self.setEmotion("Miserable")
                        step5 = QMessageBox(self)
                        step5.setWindowTitle("贝瑟尔最近非常、非常不听话")
                        step5.setText("贝瑟尔盯着你看。他的双眼充满了绝望。\n你想切开贝瑟尔吗?")
                        step5.setIcon(QMessageBox.Question)
                        step5.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        step5.move(self.x() - 20, self.y() - 120)
                        ret5 = step5.exec()
                        if (ret5 == QMessageBox.No):
                            self.interactedTimer.start(30000)
                            self.soundPlayer.stop()
                            self.resetImage()
                            return
                        else:
                            step6 = QMessageBox(self)
                            step6.setWindowTitle("贝瑟尔最近非常、非常不听话")
                            step6.setText("贝瑟尔盯着你看。他试图喊叫，但是没有声音。\n你想切开贝瑟尔吗?")
                            step6.setIcon(QMessageBox.Question)
                            step6.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                            step6.move(self.x() - 20, self.y() - 120)
                            ret6 = step6.exec()
                            if (ret6 == QMessageBox.No):
                                self.interactedTimer.start(30000)
                                self.soundPlayer.stop()
                                self.resetImage()
                                return
                            else:
                                step7 = QMessageBox(self)
                                step7.setWindowTitle("贝瑟尔最近非常、非常不听话")
                                step7.setText("贝瑟尔盯着你看。他不知道正在发生什么。\n你想切开贝瑟尔吗?")
                                step7.setIcon(QMessageBox.Question)
                                step7.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                                step7.move(self.x() - 16, self.y() - 120)
                                ret7 = step7.exec()
                                if (ret7 == QMessageBox.No):
                                    self.interactedTimer.start(30000)
                                    self.soundPlayer.stop()
                                    self.resetImage()
                                    return
                                else:
                                    self.soundPlayer.stop()
                                    self.setEmotion("Toast")
                                    self.alive = False
                                    image = QImage()
                                    image.load(os.path.join(os.path.dirname(__file__), "Images", "Cut", "Cut_0.png"))
                                    self.image.setPixmap(QPixmap.fromImage(image))
                                    self.timer = QTimer(self)
                                    self.timer.timeout.connect(self.updateCut)
                                    self.timer.start(500)

    def updateCut(self):
        self.timer.stop()
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Cut", "Cut_1.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        finalStep = QMessageBox(self)
        finalStep.setWindowTitle("Waiting for something to happen?")
        finalStep.setText("你切开了贝瑟尔。\t\t\t")
        finalStep.setStandardButtons(QMessageBox.Ok)
        finalStep.setIcon(QMessageBox.Critical)
        finalStep.move(self.x() - 12, self.y() - 120)
        finalStep.exec()

    # 西瓜
    def watermelon(self):
        self.timer.stop()
        self.interactedTimer.stop()
        self.setEmotion("Toast")
        self.soundPlayer.stop()
        self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "Watermelon.wav")))
        self.soundPlayer.setLoopCount(2)
        self.soundPlayer.play()
        self.alive = False
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Watermelon", "Watermelon_0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.watermelonPic = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateWatermelon)
        self.timer.start(200)
    
    def updateWatermelon(self):
        if (self.watermelonPic == 3):
            self.timer.stop()
        else:
            filename = f"Watermelon_{self.watermelonPic}.png"
            image = QImage()
            image.load(os.path.join(os.path.dirname(__file__), "Images", "Watermelon", filename))
            self.image.setPixmap(QPixmap.fromImage(image))
            self.watermelonPic += 1

    # 某个东西
    def something(self):
        self.interactedTimer.stop()
        self.timer.stop()
        self.setEmotion("LightbulbAfraid")
        self.soundPlayer.stop()
        self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "56122.wav")))
        self.soundPlayer.setLoopCount(QSoundEffect.Infinite)
        self.soundPlayer.play()

        self.somethingPic = 1
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Something", "Grabbed_0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.somethingGrabbed = True
        self.timer = QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(self.updateSomething)
    
    def updateSomething(self):
        filename = f"Grabbed_{self.somethingPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Something", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        if (self.somethingPic < 8):
            self.somethingPic += 1
        else:
            self.somethingPic = 6

    # 吞没
    def somethingKill(self):
        self.timer.stop()
        self.somethingGrabbed = False
        self.soundPlayer.stop()
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Something", "Swallowed_1.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.setEmotion("Something")
        self.alive = False

        self.somethingPic = 2
        self.timer = QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(self.updateSomethingKill)

    def updateSomethingKill(self):
        if (self.somethingPic == 9):
            self.setEmotion("Toast")
            self.timer.stop()
            image = QImage()
            image.load(os.path.join(os.path.dirname(__file__), "Images", "Something", "Ate.png"))
            self.image.setPixmap(QPixmap.fromImage(image))
            return
        filename = f"Swallowed_{self.somethingPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Something", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.somethingPic += 1


    # Something放开
    def somethingLetgo(self):
        self.somethingGrabbed = False
        self.resetImage()

    # 电梯
    def elevator(self):
        self.timer.stop()
        self.interactedTimer.stop()
        self.alive = False
        self.setEmotion("Faceless")
        self.elevatorPic = 1
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Elevator", "0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateElevator)
        self.timer.start(500)

    def updateElevator(self):
        filename = f"{self.elevatorPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Elevator", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.elevatorPic += 1
        if (self.elevatorPic == 7):
            self.timer.stop()
            self.setEmotion("Toast")

    # 生命果酱
    def lifejam(self):
        self.timer.stop()
        self.interactedTimer.start(30000)
        self.soundPlayer.stop()
        self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "Life_Jam.wav")))
        self.soundPlayer.setLoopCount(1)
        self.soundPlayer.play()
        self.setEmotion("Lifejam")
        self.lifejamTimer = QTimer(self)
        self.lifejamTimer.timeout.connect(self.afterLifejam)
        self.lifejamTimer.start(600)
        self.alive = True
    
    def afterLifejam(self):
        self.lifejamTimer.stop()
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Dream_Basil.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        choice = random.randint(0, 2)
        if (choice == 0):
            self.setEmotion("Sad")
        elif (choice == 1):
            self.setEmotion("Angry")
        else:
            self.setEmotion("HengAAA")

        msg = QMessageBox(self)
        msg.setWindowTitle("你欺负了小贝")
        if (choice == 0):
            msg.setText("小贝感到伤心(；′⌒`)")
        elif (choice == 1):
            msg.setText("小贝生气了(｡•ˇ‸ˇ•｡)")
        else:
            """这一段是整活，在v1.0.2中禁用
            msg.setText("小贝发出了哼、哼、哼、啊啊啊啊啊啊啊的声音以示抗议！\nε=( o｀ω′)ノ")
            self.soundPlayer.stop()
            self.soundPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), "Audio", "HengAAA.wav")))
            self.soundPlayer.setLoopCount(1)
            self.soundPlayer.play()
            """
            msg.setText("小贝特别生气(ノ｀Д)ノ")
        msg.setIcon(QMessageBox.Information)
        yes = QPushButton("安慰小贝")
        yes.clicked.connect(self.resetImage)
        msg.addButton(yes, QMessageBox.YesRole)
        msg.move(self.x(), self.y() - 120)
        msg.exec()

    # 现实Basil站立
    def realImage(self):
        self.timer.stop()
        self.interactedTimer.start(30000)
        if (random.randint(0, 1) == 0):
            self.setEmotion("RealSmile")
        else:
            self.setEmotion("RealSmileClosed")
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Real_Basil.png"))
        self.image.setPixmap(QPixmap.fromImage(image))

    # 小夜灯
    def lightbulb(self):
        self.timer.stop()
        self.interactedTimer.start(30000)
        self.setEmotion("Lightbulb")
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Lightbulb.png"))
        self.image.setPixmap(QPixmap.fromImage(image))

    # 走来走去
    def realWander(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("RealSmile")
        self.realWanderPic = 1
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "RealWander", "0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer = QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(self.updateRealWander)

    def updateRealWander(self):
        filename = f"{self.realWanderPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "RealWander", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.realWanderPic = (self.realWanderPic + 1) % 16

    # 贴贴
    def hug(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("RealSmileClosed")
        self.hugPic = 1
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Hug", "Hug_0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer = QTimer(self)
        self.timer.start(500)
        self.timer.timeout.connect(self.updateHug)

    def updateHug(self):
        if (self.hugPic <= 7):
            filename = f"Hug_{self.hugPic}.png"
            image = QImage()
            image.load(os.path.join(os.path.dirname(__file__), "Images", "Hug", filename))
            self.image.setPixmap(QPixmap.fromImage(image))
            self.hugPic += 1
        elif (self.hugPic == 16):
            self.realImage()
        else:
            self.hugPic += 1

    # 撑伞
    def umbrella(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.soundPlayer.stop()
        self.setEmotion("RealSmile")
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Umbrella.png"))
        self.image.setPixmap(QPixmap.fromImage(image))

    # 看书
    def realBook(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("RealSmile")
        self.bookPic = 0
        self.realImage()
        self.timer = QTimer(self)
        self.timer.start(400)
        self.timer.timeout.connect(self.updateRealBook)
    
    def updateRealBook(self):
        filename = f"{self.bookPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "RealBook", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.bookPic += 1

        if (self.bookPic == 3):
            self.timer.start(900)
        elif (self.bookPic == 5 or self.bookPic == 7):
            self.timer.start(1600)
        elif (self.bookPic == 8):
            self.timer.stop()
        else:
            self.timer.start(400)

    # 拍照
    def realCamera(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.realImage()
        self.setEmotion("RealSmileOpen")
        self.cameraPic = 0
        self.timer = QTimer(self)
        self.timer.start(400)
        self.timer.timeout.connect(self.updateRealCamera)

    def updateRealCamera(self):
        filename = f"{self.cameraPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "RealCamera", filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.cameraPic += 1

        if (self.cameraPic == 3):
            self.timer.start(900)
        elif (self.cameraPic == 5):
            self.timer.start(2000)
        elif (self.cameraPic == 6):
            self.timer.stop()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.realImage)
            self.timer.start(6000)
        else:
            self.timer.start(400)

    # 浇花
    def realFlower(self):
        self.interactedTimer.start(30000)
        self.timer.stop()
        self.setEmotion("RealSmileOpen")
        self.emoGif.move(224, 64)
        self.emoGif2.move(224, 64)
        self.flowerPic = 1
        choice = random.randint(0, 2)
        if (choice == 0):
            self.flowerChoice = "RealTulip"
        elif (choice == 1):
            self.flowerChoice = "RealSunflower"
        else:
            self.flowerChoice = "RealLily"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", self.flowerChoice, "0.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRealFlower)
        self.timer.start(2000)

    def updateRealFlower(self):
        filename = f"{self.flowerPic}.png"
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", self.flowerChoice, filename))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.flowerPic += 1
        if (self.flowerPic == 4):
            self.timer.stop()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.realImage)
            self.timer.start(6000)

    # 溺水
    def drown(self):
        self.interactedTimer.stop()
        self.timer.stop()
        self.setEmotion("RealAfraid")
        self.realAction.setEnabled(False)
        self.alive = False
        self.drownPic = 0
        image = QImage()
        image.load(os.path.join(os.path.dirname(__file__), "Images", "Drown", "Water.png"))
        self.image.setPixmap(QPixmap.fromImage(image))
        self.timer = QTimer(self)
        self.drownFlag = False
        self.timer.start(350)
        self.timer.timeout.connect(self.updateDrown)

    def updateDrown(self):
        if (not self.drownFlag):
            image = QImage()
            image.load(os.path.join(os.path.dirname(__file__), "Images", "Drown", f"Drown_{self.drownPic}.png"))
            self.image.setPixmap(QPixmap.fromImage(image))
            self.drownPic += 1
            if (self.drownPic == 16):
                self.drownFlag = True
                self.drownPic = 1
                self.setEmotion("RealDead")
        else:
            image = QImage()
            image.load(os.path.join(os.path.dirname(__file__), "Images", "Drown", f"{self.drownPic}.png"))
            self.image.setPixmap(QPixmap.fromImage(image))
            self.drownPic = (self.drownPic + 1) % 3

    # 假的生命果酱
    def fakeLifejam(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("致命错误")
        msg.setText("你杀死了贝瑟尔。\t\t")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.move(self.x(), self.y() - 120)
        msg.exec()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    basil = Basil()
    sys.exit(app.exec_())
