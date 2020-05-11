__copyright__ = "2020, Emile Fugulin <code@efugulin.com>"
__license__ = "GPL v3"

from calibre.customize import InterfaceActionBase


class GoogleBooksSync(InterfaceActionBase):
    name = "Google Books Sync"
    description = "Provides synchronization of your eBooks and metadata from Calibre to Google Books"
    supported_platforms = ["windows", "osx", "linux"]
    author = "Emile Fugulin"
    version = (0, 1, 0)
    minimum_calibre_version = (3, 16, 0)

    actual_plugin = "calibre_plugins.google_books_sync.ui:GoogleBooksSyncAction"

    def is_customizable(self):
        return False

    def config_widget(self):
        raise NotImplementedError()

    def save_settings(self, config_widget):
        raise NotImplementedError()
