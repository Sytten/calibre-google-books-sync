__copyright__ = "2020, Emile Fugulin <code@efugulin.com>"
__license__ = "GPL v3"

import webbrowser

from calibre.gui2.actions import InterfaceAction

# from calibre_plugins.google_books_sync.main import DemoDialog

from calibre_plugins.google_books_sync.src.login import GoogleLogin


class GoogleBooksSyncAction(InterfaceAction):

    name = "Google Books Sync"

    action_spec = (
        "Google Books Sync",
        None,
        "Sync yours books with Google Books",
        None,
    )

    def genesis(self):
        icon = get_icons("assets/images/icon.png")

        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)

    def show_dialog(self):
        # # The base plugin object defined in __init__.py
        # base_plugin_object = self.interface_action_base_plugin
        # # Show the config dialog
        # # The config dialog can also be shown from within
        # # Preferences->Plugins, which is why the do_user_config
        # # method is defined on the base plugin class
        # do_user_config = base_plugin_object.do_user_config

        # # self.gui is the main calibre GUI. It acts as the gateway to access
        # # all the elements of the calibre user interface, it should also be the
        # # parent of the dialog
        # d = DemoDialog(self.gui, self.qaction.icon(), do_user_config)
        # d.show()

        login = GoogleLogin()
        login.start()

    def apply_settings(self):
        from calibre_plugins.interface_demo.config import prefs

        # In an actual non trivial plugin, you would probably need to
        # do something based on the settings in prefs
        prefs
