import sys
import asyncio
import aiohttp
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

class ResizableIconButton(QPushButton):
    def __init__(self, text='', *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.icon_path = None
        self.current_icon = None
        self.setMinimumSize(360, 202)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        button_size = self.size()
        # button_size = button_size.boundedTo(QSize(640, 360))
        # self.updateIconSize(button_size)

    def updateIconSize(self, size):
        if self.current_icon:
            pixmap = self.current_icon.pixmap(size)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                super().setIcon(QIcon(scaled_pixmap))
                self.setIconSize(size)

    def setIcon(self, icon):
        if isinstance(icon, str):
            self.icon_path = icon
            pixmap = QPixmap(self.icon_path)
            self.current_icon = QIcon(pixmap)
        elif isinstance(icon, QIcon):
            self.current_icon = icon
        else:
            raise ValueError("Icon must be a file path or a QIcon instance.")
        
        button_size = self.size()
        self.updateIconSize(button_size)

    def setIconFromData(self, data):
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        icon = QIcon(pixmap)
        self.setIcon(icon)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resizable Icon Button Example")

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create a resizable icon button
        self.icon_button = ResizableIconButton()
        layout.addWidget(self.icon_button)

        self.setGeometry(100, 100, 300, 200)

        # Load video thumbnail asynchronously
        asyncio.run(self.loadThumbnail('https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg'))

    async def loadThumbnail(self, url):
        await asyncio.gather(
            self.loadVideoThumbnail(url)
        )

    async def loadVideoThumbnail(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    pixmap = QPixmap()
                    pixmap.loadFromData(data)
                    icon = QIcon(pixmap)
                    self.icon_button.setIcon(icon)


if __name__ == "__main__":
    import sys
    import traceback
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    try:
        asyncio.run(window.loadThumbnail('https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg'))
    except Exception as e:
        traceback.print_exc()  # Print the exception traceback
        sys.exit(1)

    sys.exit(app.exec_())
