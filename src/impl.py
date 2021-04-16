"""
This module contains a series of classes with undefined methods to later be implemented in the subclasses.
"""


class Requester:
    """Any class that requires content from the clipboard or test source must implement this class"""

    def __init__(self):
        """Constructor that starts the object"""
        super(Requester, self).__init__()

    def set_content(self, target: str, content):
        """This method receives a series of key-value pairs"""
        pass


class AbstractMonitor:
    """Provides an abstract monitor model that can be used to monitor anything"""

    def __init__(self):
        """Initiates monitor status to stopped"""
        super(AbstractMonitor, self).__init__()
        self.__monitoring: bool = False

    def start_monitoring(self) -> None:
        """Change the monitor status to 'running'"""
        self.__monitoring = True

    def stop_monitoring(self) -> None:
        """Change the monitor status to 'stopped'"""
        self.__monitoring = False

    def is_running(self) -> bool:
        """Returns the status of the monitor"""
        return self.__monitoring


class AbstractLoader:
    """Provides the abstract schema for a resource loader"""

    def __init__(self):
        """Empty constructor"""
        super(AbstractLoader, self).__init__()

    def get(self, key) -> object:
        """Returns a resource or value obtained by the loading process"""
        pass

    def get_path(self) -> str:
        """Returns the path of the resource"""
        pass


class AbstractFormatter:
    """Provides a simple outline for implementing a formatter"""

    def __init__(self):
        """Default constructor"""
        super(AbstractFormatter, self).__init__()

    def format(self, content) -> object:
        """Used to format objects"""
        pass
