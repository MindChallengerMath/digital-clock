import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import Qt, QRectF, QTimer
from PySide6.QtGui import QBrush, QColor


# ---------------- PLAYER ----------------
class Player:
    def __init__(self, scene):
        self.rect = scene.addRect(50, 500, 40, 40, brush=QBrush(QColor("blue")))
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.jump_force = -15
        self.on_ground = False

    def x(self):
        return self.rect.rect().x()

    def y(self):
        return self.rect.rect().y()

    def move(self, dx, dy):
        r = self.rect.rect()
        self.rect.setRect(r.x() + dx, r.y() + dy, 40, 40)

    def set_pos(self, x, y):
        self.rect.setRect(x, y, 40, 40)


# ---------------- GAME WINDOW ----------------
class Game(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Platformer Game")
        self.setFixedSize(1000, 650)

        self.view = QGraphicsView(self)
        self.view.setGeometry(0, 0, 1000, 650)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1000, 650)
        self.view.setScene(self.scene)

        self.keys = set()
        self.state = "menu"

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)

        self.show_menu()

    # ---------------- MENU ----------------
    def show_menu(self):
        self.scene.clear()
        self.state = "menu"

        self.title = QLabel("PLATFORMER GAME", self)
        self.title.setGeometry(350, 150, 400, 50)
        self.title.setStyleSheet("font-size: 30px;")

        self.start_button = QPushButton("Start Game", self)
        self.start_button.setGeometry(430, 300, 150, 50)
        self.start_button.clicked.connect(self.start_game)

        self.title.show()
        self.start_button.show()

    # ---------------- START GAME ----------------
    def start_game(self):
        self.title.hide()
        self.start_button.hide()

        self.scene.clear()
        self.state = "playing"

        # Platforms
        self.platforms = [
            self.scene.addRect(0, 600, 1000, 50, brush=QBrush(QColor("green"))),
            self.scene.addRect(200, 500, 150, 20, brush=QBrush(QColor("green"))),
            self.scene.addRect(450, 400, 150, 20, brush=QBrush(QColor("green"))),
            self.scene.addRect(700, 300, 150, 20, brush=QBrush(QColor("green")))
        ]

        # Goal
        self.goal = self.scene.addRect(900, 230, 40, 70, brush=QBrush(QColor("red")))

        self.player = Player(self.scene)

    # ---------------- WIN SCREEN ----------------
    def show_win(self):
        self.scene.clear()
        self.state = "win"

        self.win_label = QLabel("YOU WIN! Press R", self)
        self.win_label.setGeometry(380, 250, 300, 50)
        self.win_label.setStyleSheet("font-size: 28px;")
        self.win_label.show()

    # ---------------- GAME LOOP ----------------
    def update_game(self):
        if self.state != "playing":
            return

        # Movement
        self.player.vx = 0

        if Qt.Key_A in self.keys:
            self.player.vx = -self.player.speed

        if Qt.Key_D in self.keys:
            self.player.vx = self.player.speed

        self.player.vy += 0.7
        if self.player.vy > 12:
            self.player.vy = 12

        # Horizontal movement
        self.player.move(self.player.vx, 0)

        # Vertical movement
        self.player.move(0, self.player.vy)

        self.player.on_ground = False

        # Collision
        player_rect = self.player.rect.rect()

        for p in self.platforms:
            plat = p.rect()

            if player_rect.intersects(plat):
                if self.player.vy > 0:
                    self.player.set_pos(player_rect.x(), plat.y() - 40)
                    self.player.vy = 0
                    self.player.on_ground = True

        # Goal collision
        if player_rect.intersects(self.goal.rect()):
            self.show_win()

    # ---------------- INPUT ----------------
    def keyPressEvent(self, event):
        self.keys.add(event.key())

        if self.state == "playing":
            if event.key() == Qt.Key_Space:
                if self.player.on_ground:
                    self.player.vy = self.player.jump_force

        if self.state == "win":
            if event.key() == Qt.Key_R:
                self.win_label.hide()
                self.show_menu()

    def keyReleaseEvent(self, event):
        if event.key() in self.keys:
            self.keys.remove(event.key())


# ---------------- RUN ----------------
app = QApplication(sys.argv)
window = Game()
window.show()
sys.exit(app.exec())