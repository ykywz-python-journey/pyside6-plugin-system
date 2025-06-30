from PySide6.QtWidgets import QWidget


class PluginInterface:
    """Base class that all plugins must implement"""

    @classmethod
    def get_button_widget(cls, parent=None) -> QWidget:
        """
        Returns a button widget that will be added to the main UI
        This must be implemented by plugin classes
        """
        raise NotImplementedError
