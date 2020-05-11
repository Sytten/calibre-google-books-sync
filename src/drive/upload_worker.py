from calibre_plugins.google_books_sync.worker import BaseWorker
from calibre_plugins.google_books_sync.books.book import Book


class DriveUploadWorker(BaseWorker):
    BASE_URL = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"

    def __init__(self, db, logger, book_ids):
        super().__init__(db, logger)
        self.pending_book_ids = book_ids = book_ids

    def sync(self):
        if len(self.pending_book_ids) == 0:
            self.finished.emit()
            return

        self.progress.emit(self.count)
        self.count += 1

        self.book_id = self.pending_book_ids.pop()

        self.logger.info(
            "Upload book: book_id={}; title={}".format(
                self.book_id, self.db.get_proxy_metadata(self.book_id).title
            )
        )

        book = Book(self.db, self.book_id)

        if book.file_path:
            self.file_path = book.file_path
            self.check()
        else:
            self.failed.emit(self.book_id, "unsupported format")
            self.readyForNext.emit()
