import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QScrollArea, QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
from chatbot_logic import ChatbotLogic

class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Onboarding Chatbot")
        self.setGeometry(100, 100, 800, 831)

        # Aktif olan butonları takip etmek için liste
        self.active_option_widgets = []

        # Ana widget
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Chat alanı
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_layout.setSpacing(10)
        self.scroll_area_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_area_widget.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.main_layout.addWidget(self.scroll_area)

        # Input alanı
        self.input_widget = QWidget()
        self.input_layout = QHBoxLayout()
        self.input_widget.setLayout(self.input_layout)
        self.main_layout.addWidget(self.input_widget)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Bir mesaj yazın...")
        self.message_input.setFont(QFont("Arial", 12))
        self.message_input.setStyleSheet("""
            QLineEdit {
                border-radius: 15px;
                padding: 10px;
                border: 1px solid #0078d7;
                background: #f9f9f9;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        self.input_layout.addWidget(self.message_input)

        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon("send_icon.png"))
        self.send_button.setStyleSheet("""
            QPushButton {
                background: #0078d7;
                border-radius: 15px;
                padding: 10px;
                color: white;
            }
            QPushButton:hover {
                background: #005bb5;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)

        # Seçenek butonları için aktif stil
        self.option_button_style_active = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #0078d7;
                border-radius: 15px;
                padding: 8px 15px;
                margin: 5px;
                color: #333;
                font-size: 12px;
                text-align: left;
                min-width: 200px;
                white-space: normal;
                max-width: 400px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """

        # Seçenek butonları için devre dışı stil
        self.option_button_style_disabled = """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 15px;
                padding: 8px 15px;
                margin: 5px;
                color: #999999;
                font-size: 12px;
                text-align: left;
                min-width: 200px;
                white-space: normal;
                max-width: 400px;
            }
        """

        # Kategori ve soru seçeneklerini tutacak değişkenler
        self.current_category = None
        self.current_question = None

        # ChatbotLogic'i başlat
        self.chatbot = ChatbotLogic(self)

        # Timer
        self.scroll_timer = QTimer()
        self.scroll_timer.setSingleShot(True)
        self.scroll_timer.timeout.connect(self.delayed_scroll)

        # Hoşgeldin mesajı
        self.welcome_message = (
            "Merhaba, Kütüphane Dökümantasyon Daire Başkanlığına hoşgeldiniz. "
            "Hangi konuda size yardımcı olabilirim?"
        )

        # Başlangıç mesajını göster
        self.show_welcome()

    def disable_previous_options(self):
        """Önceki tüm seçenekleri devre dışı bırak"""
        for widget in self.active_option_widgets:
            for child in widget.findChildren(QPushButton):
                child.setEnabled(False)
                child.setStyleSheet(self.option_button_style_disabled)
                try:
                    child.clicked.disconnect()
                except TypeError:
                    pass  # Eğer zaten disconnect edilmişse hata vermesini engelle

    def show_welcome(self):
        """Hoşgeldin mesajını ve kategori seçeneklerini göster"""
        self.add_message(self.welcome_message, user=False)
        self.show_category_options()

    def show_category_options(self):
        """Kategori seçeneklerini buton olarak göster"""
        # Önceki seçenekleri devre dışı bırak
        self.disable_previous_options()

        options_widget = QWidget()
        options_layout = QVBoxLayout()
        options_layout.setSpacing(5)
        options_layout.setContentsMargins(0, 5, 0, 5)
        options_widget.setLayout(options_layout)

        for category in self.chatbot.get_categories():
            btn = QPushButton(category["title"])
            btn.setStyleSheet(self.option_button_style_active)
            btn.clicked.connect(lambda checked, cat_id=category["id"]:
                              self.category_selected(cat_id))
            options_layout.addWidget(btn)

        self.scroll_area_layout.addWidget(options_widget)
        self.active_option_widgets.append(options_widget)
        self.delayed_scroll()

    def show_question_options(self, category_id):
        """Seçilen kategorideki soruları buton olarak göster"""
        # Önceki seçenekleri devre dışı bırak
        self.disable_previous_options()

        questions = self.chatbot.get_questions_by_category(category_id)
        options_widget = QWidget()
        options_layout = QVBoxLayout()
        options_layout.setSpacing(5)
        options_layout.setContentsMargins(0, 5, 0, 5)
        options_widget.setLayout(options_layout)

        for question in questions.keys():
            btn = QPushButton(question)
            btn.setStyleSheet(self.option_button_style_active)
            btn.clicked.connect(lambda checked, q=question: self.question_selected(q))
            options_layout.addWidget(btn)

        self.scroll_area_layout.addWidget(options_widget)
        self.active_option_widgets.append(options_widget)
        self.delayed_scroll()

    def category_selected(self, category_id):
        """Kategori seçildiğinde çağrılır"""
        self.current_category = category_id
        category_title = next(cat["title"] for cat in self.chatbot.get_categories()
                            if cat["id"] == category_id)

        self.add_message(f"{category_title} konusunda hangi sorunuz var?", user=False)
        self.show_question_options(category_id)

    def question_selected(self, question):
        """Soru seçildiğinde çağrılır"""
        self.current_question = question
        self.add_message(question, user=True)
        response = self.chatbot.process_message(question)
        self.add_message(response, user=False)
        self.show_continuation_options()

    def show_continuation_options(self):
        """Devam seçeneklerini göster"""
        # Önceki seçenekleri devre dışı bırak
        self.disable_previous_options()

        options_widget = QWidget()
        options_layout = QVBoxLayout()
        options_layout.setSpacing(5)
        options_layout.setContentsMargins(0, 5, 0, 5)
        options_widget.setLayout(options_layout)

        same_category_btn = QPushButton("Aynı konuda başka bir sorum var")
        same_category_btn.setStyleSheet(self.option_button_style_active)
        same_category_btn.clicked.connect(lambda: self.category_selected(self.current_category))

        different_category_btn = QPushButton("Başka bir konuda sorum var")
        different_category_btn.setStyleSheet(self.option_button_style_active)
        different_category_btn.clicked.connect(self.show_different_category_prompt)

        options_layout.addWidget(same_category_btn)
        options_layout.addWidget(different_category_btn)

        self.scroll_area_layout.addWidget(options_widget)
        self.active_option_widgets.append(options_widget)
        self.delayed_scroll()

    def show_different_category_prompt(self):
        """Farklı kategori seçimi için prompt göster"""
        self.add_message("Hangi türden bir soru sormak istersiniz?", user=False)
        self.show_category_options()

    def send_message(self):
        """Kullanıcı mesajını gönderir"""
        user_message = self.message_input.text().strip()
        if user_message:
            self.add_message(user_message, user=True)
            self.message_input.clear()
            chatbot_response = self.chatbot.process_message(user_message)
            self.add_message(chatbot_response, user=False)
            self.show_continuation_options()

    def add_message(self, text, user=True):
        """Sohbet alanına mesaj ekler"""
        message_container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        message_container.setLayout(container_layout)

        message_frame = QFrame()
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(12, 8, 12, 8)
        message_frame.setLayout(frame_layout)

        message_label = QLabel(text)
        message_label.setWordWrap(True)
        message_label.setFont(QFont("Arial", 12))

        text_width = message_label.fontMetrics().boundingRect(text).width()
        max_width = min(text_width + 50, 400)
        min_width = 50
        message_label.setMinimumWidth(min(max_width, min_width))
        message_label.setMaximumWidth(max_width)

        if user:
            message_frame.setStyleSheet("""
                QFrame {
                    background-color: #0078d7;
                    border-radius: 15px;
                }
                QLabel {
                    color: white;
                }
            """)
            container_layout.addStretch()
            container_layout.addWidget(message_frame)
        else:
            message_frame.setStyleSheet("""
                QFrame {
                    background-color: #e0e0e0;
                    border-radius: 15px;
                }
                QLabel {
                    color: black;
                }
            """)
            container_layout.addWidget(message_frame)
            container_layout.addStretch()

        frame_layout.addWidget(message_label)
        self.scroll_area_layout.addWidget(message_container)
        self.scroll_timer.start(100)

    def delayed_scroll(self):
        """Scroll alanını en alta kaydırır"""
        scroll_bar = self.scroll_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotWindow()
    window.show()
    sys.exit(app.exec_())