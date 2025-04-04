# from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
# from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
# from PyQt5.QtCore import Qt, QSize, QTimer
# from dotenv import dotenv_values
# import sys
# import os
# env_vars= dotenv_values(".env")
# Assistantname = env_vars.get("Assistantname")
# current_dir = os.getcwd()
# old_chat_message = ""
# TempDirPath = rf"{current_dir}\Frontend\Files"
# GraphicsDirPath = rf" {current_dir}\Frontend\Graphics"

# def AnswerModifier(Answer):
#     lines = Answer.split('\n')  # Split the text into lines
#     non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines
#     modified_answer = '\n'.join(non_empty_lines)  # Rejoin the lines
#     return modified_answer

# def QueryModifier(Query):
#     new_query = Query.lower().strip()  # Convert to lowercase and trim spaces
#     query_words = new_query.split()  # Split into words

#     question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", 
#                       "can you", "what's", "where's", "how's"]

#     # Check if query starts with a question word
#     if any(word + " " in new_query for word in question_words):
#         if query_words[-1][-1] in ['.', '?', '!']:
#             new_query = new_query[:-1] + "?"
#         else:
#             new_query += "?"  # Ensure it ends with a question mark
#     else:
#         if query_words[-1][-1] in ['.', '?', '!']:
#             new_query = new_query[:-1] + "."  # Replace last punctuation with '?'
#         else:
#             new_query += "."  # Append '?' if no punctuation is present

#     return new_query.capitalize()  # Capitalize the first letter

# def SetMicrophoneStatus(Command):
#     with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
#         file.write(Command)

# def GetMicrophoneStatus():
#     with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file:
#         Status = file.read()
#     return Status

# def SetAssistantStatus(Status):
#     with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
#         file.write(Status)

# def GetAssistantStatus():
#     with open(rf'{TempDirPath}\Status.data', "r", encoding='utf-8') as file:
#         Status = file.read()
#     return Status

# def MicButtonInitialed():
#     SetMicrophoneStatus("False")

# def MicButtonClosed():
#     SetMicrophoneStatus("True")

# def GraphicsDirectoryPath(Filename):
#     Path = rf'{GraphicsDirPath}\{Filename}'  
#     return Path

# def TempDirectoryPath(Filename):
#     Path = rf'{TempDirPath}\{Filename}'  
#     return Path

# def ShowTextToScreen(Text):
#     with open(rf'{TempDirPath}\Responses.data', "w", encoding='utf-8') as file:
#         file.write(Text)


# class ChatSection(QWidget):
#     def __init__(self):
#         super(ChatSection, self).__init__()

#         # Create layout
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(-10, 40, 40, 100)  # Adjusted negative margin values
#         layout.setSpacing(-100)  # Negative spacing is invalid, using a reasonable value

#         # Chat text edit
#         self.chat_text_edit = QTextEdit()
#         self.chat_text_edit.setReadOnly(True)
#         self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
#         self.chat_text_edit.setFrameStyle(QTextEdit.NoFrame)
#         layout.addWidget(self.chat_text_edit)
#         self.setStyleSheet("background-color: black;")
#         layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
#         layout.setStretch(1, 1)
#         self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
#         # Set text color
#         text_color = QColor(Qt.blue)
#         text_color_text = QTextCharFormat()
#         text_color_text.setForeground(text_color)
#         self.chat_text_edit.setCurrentCharFormat(text_color_text)

#         # GIF Label
#         self.gif_label = QLabel()
#         self.gif_label.setStyleSheet("border: none;")

#         movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
#         movie.setScaledSize(QSize(480, 270))

#         self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
#         self.gif_label.setMovie(movie)
#         movie.start()

#         layout.addWidget(self.gif_label)

#         # Status Label
#         self.label = QLabel("")
#         self.label.setStyleSheet("color: white; font-size:16px; margin-right: 195px; border: none; margin-top: -30px;")
#         self.label.setAlignment(Qt.AlignRight)
#         layout.addWidget(self.label)

#         # Adjust layout
#         layout.setSpacing(-10)
#         layout.addWidget(self.gif_label)

#         # Set font for chat text
#         font = QFont()
#         font.setPointSize(13)
#         self.chat_text_edit.setFont(font)

#         # Timer for periodic actions
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.loadMessages)
#         self.timer.timeout.connect(self.SpeechRecogText)
#         self.timer.start(5)

#         # Install event filter
#         self.chat_text_edit.viewport().installEventFilter(self)

#         # Set scrollbar styles
#         self.setStyleSheet("""
#             QScrollBar:vertical {
#                 border: none;
#                 background: black;
#                 width: 10px;
#                 margin: 0px 0px 0px 0px;
#             }
#             QScrollBar::handle:vertical { 
#                 background: white;
#                 min-height: 20px;
#             }
#             QScrollBar::add-line:vertical {
#                 background: black;
#                 subcontrol-position: bottom;
#                 subcontrol-origin: margin;
#                 height: 10px;
#             }
#             QScrollBar::sub-line:vertical { 
#                 background: black;
#                 subcontrol-position: top;
#                 subcontrol-origin: margin;
#                 height: 10px;
#             }
#             QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { 
#                 border: none;
#                 background: none;
#                 color: none;
#             }
#             QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { 
#                 background: none;
#             }
#         """)


#     def loadMessages(self):
#         """Loads messages from Responses.data and updates chat display"""
#         global old_chat_message
#         try:
#             with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
#                 messages = file.read().strip()

#             if not messages:
#                 pass
#             elif len(messages) <= 1:
#                 pass
#             elif str(old_chat_message) == str(messages):
#                 pass
#             else:
#                 self.addMessage(message=messages, color='White')
#                 old_chat_message = messages

#         except FileNotFoundError:
#             pass  # Handle missing file case

#     def SpeechRecogText(self):
#         """Reads status data and updates the label with recognized text."""
#         try:
#             with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
#                 messages = file.read().strip()
#             self.label.setText(messages)
#         except FileNotFoundError:
#             self.label.setText("Status Unavailable")

#     def load_icon(self, path, width=60, height=60):
#         """Loads and scales an icon from the given path."""
#         pixmap = QPixmap(path)
#         new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)
#         self.icon_label.setPixmap(new_pixmap)

#     def toggle_icon(self, event=None):
#         """Toggles between voice and mic icons when the button is clicked."""
#         if not hasattr(self, 'toggled'):  # Ensure 'toggled' exists
#             self.toggled = False  # Initialize if missing

#         if self.toggled:
#             self.load_icon(GraphicsDirectoryPath('mic.png'), 60, 60)
#             MicButtonClosed()
#         else:
#             self.load_icon(GraphicsDirectoryPath('voice.png'), 60, 60)
#             MicButtonInitialed()

#         self.toggled = not self.toggled  # Toggle state

#     def addMessage(self, message, color):
#         """Inserts a new message into the chat text edit with the given color."""
#         cursor = self.chat_text_edit.textCursor()

#         format = QTextCharFormat()
#         format.setForeground(QColor(color))

#         formatm = QTextBlockFormat()
#         formatm.setTopMargin(10)
#         formatm.setLeftMargin(10)

#         cursor.setCharFormat(format)
#         cursor.setBlockFormat(formatm)
#         cursor.insertText(message + "\n")

#         self.chat_text_edit.setTextCursor(cursor)

# class InitialScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
        
#         desktop = QApplication.primaryScreen()
#         screen_width = desktop.size().width()
#         screen_height = desktop.size().height()
        
#         content_layout = QVBoxLayout()
#         content_layout.setContentsMargins(0, 0, 0, 0)
        
#         # GIF Label
#         self.gif_label = QLabel()
#         movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
#         max_gif_size_H = int(screen_width / 1.69)
#         movie.setScaledSize(QSize(screen_width, max_gif_size_H))
#         self.gif_label.setAlignment(Qt.AlignCenter)
#         self.gif_label.setMovie(movie)
#         movie.start()
#         self.gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
#         # Icon Label
#         self.icon_label = QLabel()
#         self.load_icon(GraphicsDirectoryPath('Mic_on.png'))
#         self.icon_label.setFixedSize(150, 150)
#         self.icon_label.setAlignment(Qt.AlignCenter)
#         self.toggled = True
#         self.toggle_icon()
#         self.icon_label.mousePressEvent = self.toggle_icon
        
#         # Text Label
#         self.label = QLabel("")
#         self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")
        
#         content_layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)
#         content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
#         content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
#         content_layout.setContentsMargins(0, 0, 0, 150)
        
#         self.setLayout(content_layout)
#         self.setFixedHeight(screen_height)
#         self.setFixedWidth(screen_width)
#         self.setStyleSheet("background-color: black;")
        
#         # Timer
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.SpeechRecogText)
#         self.timer.start(5)
    
#     def SpeechRecogText(self):
#         try:
#             with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
#                 messages = file.read()
#             self.label.setText(messages)
#         except FileNotFoundError:
#             self.label.setText("Status Unavailable")
    
#     def load_icon(self, path, width=60, height=60):
#         pixmap = QPixmap(path)
#         new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)
#         self.icon_label.setPixmap(new_pixmap)
    
#     def toggle_icon(self, event=None):
#         if self.toggled:
#             self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
#             MicButtonClosed()
#         else:
#             self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
#             MicButtonInitialed()
#         self.toggled = not self.toggled


# class MessageScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
        
#         # Get screen dimensions
#         desktop = QApplication.primaryScreen()
#         screen_rect = desktop.geometry()
#         screen_width = screen_rect.width()
#         screen_height = screen_rect.height()

#         # Set up layout
#         layout = QVBoxLayout()
        
#         # Label
#         self.label = QLabel("")
#         self.label.setAlignment(Qt.AlignCenter)
#         layout.addWidget(self.label)
        
#         # Chat section
#         self.chat_section = ChatSection()
#         layout.addWidget(self.chat_section)

#         # Apply layout and styles
#         self.setLayout(layout)
#         self.setStyleSheet("background-color: black;")
#         self.setFixedHeight(screen_height)
#         self.setFixedWidth(screen_width)

# class CustomTopBar(QWidget):
#     def __init__(self, parent, stacked_widget):
#         super().__init__(parent)
#         self.stacked_widget = stacked_widget
#         self.current_screen = None
#         self.draggable = True
#         self.offset = None
#         self.initUI()

#     def initUI(self):
#         self.setFixedHeight(50)

#         # Layout
#         layout = QHBoxLayout(self)
#         layout.setAlignment(Qt.AlignRight)

#         # Home Button
#         home_button = QPushButton()
#         home_icon = QIcon(GraphicsDirectoryPath("Home.png"))
#         home_button.setIcon(home_icon)
#         home_button.setText(" Home")
#         home_button.setStyleSheet("height: 40px; line-height: 40px; background-color: white; color: black")

#         # Message Button
#         message_button = QPushButton()
#         message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
#         message_button.setIcon(message_icon)
#         message_button.setText(" Chat")
#         message_button.setStyleSheet("height: 40px; line-height: 40px; background-color: white; color: black")

#         # Minimize Button
#         minimize_button = QPushButton()
#         minimize_icon = QIcon(GraphicsDirectoryPath('Minimize2.png'))
#         minimize_button.setIcon(minimize_icon)
#         minimize_button.setStyleSheet("background-color: white")
#         minimize_button.clicked.connect(self.minimizeWindow)

#         # Maximize Button
#         self.maximize_button = QPushButton()
#         self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
#         self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
#         self.maximize_button.setIcon(self.maximize_icon)
#         self.maximize_button.setFlat(True)
#         self.maximize_button.setStyleSheet("background-color: white")
#         self.maximize_button.clicked.connect(self.maximizeWindow)

#         # Close Button
#         close_button = QPushButton()
#         close_icon = QIcon(GraphicsDirectoryPath('Close.png'))
#         close_button.setIcon(close_icon)
#         close_button.setStyleSheet("background-color: white")
#         close_button.clicked.connect(self.closeWindow)

#         # Line Separator
#         line_frame = QFrame()
#         line_frame.setFixedHeight(1)
#         line_frame.setFrameShape(QFrame.HLine)
#         line_frame.setFrameShadow(QFrame.Sunken)
#         line_frame.setStyleSheet("border-color: black;")

#         # Title Label
#         title_label = QLabel(f" {str(Assistantname).capitalize()} AI ")
#         title_label.setStyleSheet("color: black; font-size: 18px; background-color: white")

#         # Navigation Logic
#         home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
#         message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

#         # Adding widgets to layout
#         layout.addWidget(title_label)
#         layout.addStretch(1)
#         layout.addWidget(home_button)
#         layout.addWidget(message_button)
#         layout.addStretch(1)
#         layout.addWidget(minimize_button)
#         layout.addWidget(self.maximize_button)
#         layout.addWidget(close_button)

#         self.setLayout(layout)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.fillRect(self.rect(), Qt.white)
#         super().paintEvent(event)

#     def minimizeWindow(self):
#         self.parent().showMinimized()

#     def maximizeWindow(self):
#         if self.parent().isMaximized():
#             self.parent().showNormal()
#             self.maximize_button.setIcon(self.maximize_icon)
#         else:
#             self.parent().showMaximized()
#             self.maximize_button.setIcon(self.restore_icon)

#     def closeWindow(self):
#         self.parent().close()

#     def mousePressEvent(self, event):
#         if self.draggable:
#             self.offset = event.pos()

#     def mouseMoveEvent(self, event):
#         if self.draggable and self.offset:
#             new_pos = event.globalPos() - self.offset
#             self.parent().move(new_pos)

#     def showMessageScreen(self):
#         if self.current_screen is not None:
#             self.current_screen.hide()
#         message_screen = MessageScreen(self)
#         layout = self.parent().layout()
#         if layout is not None:
#             layout.addWidget(message_screen)
#         self.current_screen = message_screen

#     def showInitialScreen(self):
#         if self.current_screen is not None:
#             self.current_screen.hide()
#         initial_screen = InitialScreen(self)
#         layout = self.parent().layout()
#         if layout is not None:
#             layout.addWidget(initial_screen)
#         self.current_screen = initial_screen

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.initUI()

#     def initUI(self):
#         # Get screen dimensions
#         desktop = QApplication.desktop()
#         screen_width = desktop.screenGeometry().width()
#         screen_height = desktop.screenGeometry().height()

#         # Stack Widget for managing screens
#         stacked_widget = QStackedWidget(self)

#         # Adding screens
#         initial_screen = InitialScreen()
#         message_screen = MessageScreen()
#         stacked_widget.addWidget(initial_screen)
#         stacked_widget.addWidget(message_screen)

#         # Set window properties
#         self.setGeometry(0, 0, screen_width, screen_height)
#         self.setStyleSheet("background-color: black;")

#         # Custom top bar
#         top_bar = CustomTopBar(self, stacked_widget)
#         self.setMenuWidget(top_bar)
#         self.setCentralWidget(stacked_widget)

# def GraphicalUserInterface():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     GraphicalUserInterface()
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

# Environment setup
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname", "Assistant")  # Default if not found
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics")
def AnswerModifier(Answer):
    lines = Answer.split('\n')  # Split the text into lines
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines
    modified_answer = '\n'.join(non_empty_lines)  # Rejoin the lines
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()  # Convert to lowercase and trim spaces
    query_words = new_query.split()  # Split into words

    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", 
                      "can you", "what's", "where's", "how's"]

    # Check if query starts with a question word
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"  # Ensure it ends with a question mark
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."  # Replace last punctuation with '?'
        else:
            new_query += "."  # Append '?' if no punctuation is present

    return new_query.capitalize()  # Capitalize the first letter
def safe_load_icon(path, default_size=(60, 60)):
    """Safely loads an icon from path with error handling"""
    if not os.path.exists(path):
        print(f"Warning: Icon file not found: {path}")
        # Create a colored placeholder pixmap if file is missing
        pixmap = QPixmap(default_size[0], default_size[1])
        pixmap.fill(Qt.gray)
        return pixmap
    return QPixmap(path)

def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Responses.data', "w", encoding='utf-8') as file:
        file.write(Text)

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data', "r", encoding='utf-8') as file:
        Status = file.read()
    return Status
def GraphicsDirectoryPath(filename):
    """Get the full path for a graphics file"""
    return os.path.join(GraphicsDirPath, filename)

def TempDirectoryPath(filename):
    """Get the full path for a temp file"""
    return os.path.join(TempDirPath, filename)

def SetMicrophoneStatus(command):
    """Write microphone status to file"""
    with open(TempDirectoryPath('Mic.data'), "w", encoding='utf-8') as file:
        file.write(command)

def GetMicrophoneStatus():
    """Read microphone status from file"""
    try:
        with open(TempDirectoryPath('Mic.data'), "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "False"

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        desktop = QApplication.primaryScreen()
        screen_width = desktop.size().width()
        screen_height = desktop.size().height()
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # GIF Label with error handling
        self.gif_label = QLabel()
        gif_path = GraphicsDirectoryPath('Jarvis.gif')
        if os.path.exists(gif_path):
            movie = QMovie(gif_path)
            max_gif_size_H = int(screen_width / 1.69)
            movie.setScaledSize(QSize(screen_width, max_gif_size_H))
            self.gif_label.setMovie(movie)
            movie.start()
        else:
            print(f"Warning: GIF file not found: {gif_path}")
            self.gif_label.setText("GIF Animation Placeholder")
            self.gif_label.setStyleSheet("color: white; background-color: gray;")
        
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Icon Label
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        initial_icon = safe_load_icon(GraphicsDirectoryPath('Mic_on.png'))
        self.icon_label.setPixmap(initial_icon.scaled(150, 150, Qt.KeepAspectRatio))
        
        self.toggled = True
        self.icon_label.mousePressEvent = self.toggle_icon
        
        # Text Label
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")
        
        content_layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)
        
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")
        
        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(5)

    def load_icon(self, path, width=60, height=60):
        pixmap = safe_load_icon(path, (width, height))
        new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio)
        self.icon_label.setPixmap(new_pixmap)
    
    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
            MicButtonClosed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
            MicButtonInitialed()
        self.toggled = not self.toggled

    def update_status(self):
        """Update status text from file"""
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read().strip()
            self.label.setText(messages)
        except FileNotFoundError:
            self.label.setText("Status Unavailable")

class ChatSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(10)  # Changed from invalid -100
        
        # Chat text edit
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QTextEdit.NoFrame)
        layout.addWidget(self.chat_text_edit)
        
        # Set up chat display properties
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        
        # Timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_messages)
        self.timer.start(5)

    def load_messages(self):
        """Load and display messages from file"""
        global old_chat_message
        try:
            with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
                messages = file.read().strip()
                
            if messages and messages != old_chat_message:
                self.add_message(messages, 'White')
                old_chat_message = messages
                
        except FileNotFoundError:
            pass

    def add_message(self, message, color):
        """Add a new message to the chat display"""
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("")
        self.chat_section = ChatSection()
        layout.addWidget(self.label)
        layout.addWidget(self.chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setup_ui()

    def setup_ui(self):
        # Create and set up stacked widget
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(InitialScreen())
        self.stacked_widget.addWidget(MessageScreen())
        
        # Set up window properties
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setStyleSheet("background-color: black;")
        
        # Create and set up custom title bar
        self.title_bar = CustomTopBar(self, self.stacked_widget)
        self.setMenuWidget(self.title_bar)
        self.setCentralWidget(self.stacked_widget)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        
        # Title
        title = QLabel(f" {Assistantname.capitalize()} AI ")
        title.setStyleSheet("color: black; font-size: 18px; background-color: white")
        
        # Navigation buttons
        home_btn = self.create_button("Home.png", "Home", lambda: self.stacked_widget.setCurrentIndex(0))
        chat_btn = self.create_button("Chats.png", "Chat", lambda: self.stacked_widget.setCurrentIndex(1))
        
        # Window control buttons
        min_btn = self.create_button("Minimize2.png", "", self.parent().showMinimized)
        max_btn = self.create_button("Maximize.png", "", self.toggle_maximize)
        close_btn = self.create_button("Close.png", "", self.parent().close)
        
        # Add widgets to layout
        layout.addWidget(title)
        layout.addStretch(1)
        layout.addWidget(home_btn)
        layout.addWidget(chat_btn)
        layout.addStretch(1)
        layout.addWidget(min_btn)
        layout.addWidget(max_btn)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        self.setFixedHeight(50)
        self.setStyleSheet("background-color: white")

    def create_button(self, icon_name, text, callback):
        btn = QPushButton()
        icon = QIcon(safe_load_icon(GraphicsDirectoryPath(icon_name)))
        btn.setIcon(icon)
        if text:
            btn.setText(f" {text}")
        btn.setStyleSheet("height: 40px; line-height: 40px; background-color: white; color: black")
        btn.clicked.connect(callback)
        return btn

    def toggle_maximize(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
        else:
            self.parent().showMaximized()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()