from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from src.plugin_system import PluginInterface


class ExamplePlugin(PluginInterface):
    """Example plugin that demonstrates a custom button widget"""

    @classmethod
    def get_button_widget(cls, parent=None) -> QWidget:
        """Create and return the plugin button widget"""
        container = QWidget(parent)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Custom button with icon
        btn = QPushButton("Click Me 2!")
        btn.setIcon(QIcon.fromTheme("dialog-information"))
        btn.setFixedHeight(45)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Example functionality
        btn.clicked.connect(lambda: print("Plugin button clicked!"))

        # Add description
        description = QLabel("This is an example plugin button 2!")
        description.setAlignment(Qt.AlignCenter)

        layout.addWidget(btn)
        layout.addWidget(description)

        return container
