from __future__ import print_function

__copyright__ = "2020, Emile Fugulin <code@efugulin.com>"
__license__ = "GPL v3"

from datetime import datetime

from calibre_plugins.bookfusion.config import prefs


class Logger:
    def info(self, msg):
        self._log(msg, "INFO")

    def _log(self, msg, level):
        if prefs["debug"]:
            line = "[%s] %s %s" % (level, datetime.now(), msg)
            print(line)
