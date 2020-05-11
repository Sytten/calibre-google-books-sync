from PyQt5.Qt import QObject, pyqtSignal


class BaseWorker(QObject):
    finished = pyqtSignal()
    readyForNext = pyqtSignal()
    progress = pyqtSignal(int)
    uploadProgress = pyqtSignal(int, int)
    uploaded = pyqtSignal(int)
    skipped = pyqtSignal(int)
    failed = pyqtSignal(int, str)
    aborted = pyqtSignal(str)

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger

    def start(self):
        self.network = QNetworkAccessManager()
        self.readyForNext.connect(self.sync)

        self.count = 0
        self.readyForNext.emit()

    def sync():
        """Must be implemented by each worker"""
        raise NotImplementedError()
