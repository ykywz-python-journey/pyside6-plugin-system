import importlib
import inspect
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QScrollArea, QFrame, QLabel
)
from PySide6.QtCore import Qt

import os

from src.plugin_system import PluginInterface


class PluginLoader:
    """Handles loading of plugin modules"""

    def __init__(self, plugin_dir="./plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins = []

    def load_plugins(self):
        """Load all valid plugins from the plugin directory"""
        self.plugins.clear()

        if not self.plugin_dir.exists():
            print(f"Plugin directory {self.plugin_dir} not found")
            return []

        for item in self.plugin_dir.iterdir():
            if item.is_file() and item.suffix == ".py" and item.stem != "__init__":
                try:
                    module = self._import_module(item)
                    plugin = self._get_plugin_from_module(module)
                    if plugin:
                        self.plugins.append(plugin)
                except Exception as e:
                    print(f"Failed to load {item}: {str(e)}")

        return self.plugins

    def _import_module(self, file_path):
        """Dynamically import a module from file path"""
        # Create an absolute module path
        module_path = f"plugins.{file_path.stem}"

        # Use importlib to load the module
        spec = importlib.util.spec_from_file_location(module_path, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

    def _get_plugin_from_module(self, module):
        """Extract plugin class from module"""
        for name, obj in inspect.getmembers(module):
            if (
                    inspect.isclass(obj)
                    and obj is not PluginInterface
                    and issubclass(obj, PluginInterface)
            ):
                return obj()
        return None


class MainWindow(QMainWindow):
    """Main application window that hosts the plugin buttons"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Plugin System")
        self.setMinimumSize(400, 300)

        # Set up main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Title label
        title_label = QLabel("Plugin Buttons")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.main_layout.addWidget(title_label)

        # Scroll area for buttons
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Container for buttons
        self.button_container = QWidget()
        self.button_layout = QVBoxLayout(self.button_container)
        self.button_layout.setAlignment(Qt.AlignTop)
        self.button_layout.setSpacing(5)
        self.scroll_area.setWidget(self.button_container)

        # Load plugins button
        self.load_button = QPushButton("Refresh Plugins")
        self.load_button.clicked.connect(self.load_plugins)
        self.load_button.setFixedHeight(40)
        self.main_layout.addWidget(self.load_button)

        # Initial plugin load
        self.load_plugins()

    def load_plugins(self):
        """Load plugins and display their buttons"""
        # Clear existing buttons
        while self.button_layout.count():
            child = self.button_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Load and create button widgets from plugins
        loader = PluginLoader()
        plugins = loader.load_plugins()

        if not plugins:
            no_plugins_label = QLabel("No plugins found in plugins/ directory")
            no_plugins_label.setAlignment(Qt.AlignCenter)
            self.button_layout.addWidget(no_plugins_label)
            return

        for plugin in plugins:
            try:
                button_widget = plugin.get_button_widget(self.button_container)
                if isinstance(button_widget, QWidget):
                    self.button_layout.addWidget(button_widget)

                    # Add separator between buttons
                    separator = QFrame()
                    separator.setFrameShape(QFrame.HLine)
                    separator.setFrameShadow(QFrame.Sunken)
                    self.button_layout.addWidget(separator)
            except Exception as e:
                print(f"Failed to create widget for plugin: {str(e)}")


if __name__ == "__main__":
    # Ensure plugins directory exists
    if not Path("./plugins").exists():
        Path("./plugins").mkdir()
        print("Created 'plugins' directory - add your plugin files here")

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
