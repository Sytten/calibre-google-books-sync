__copyright__ = "2020, Emile Fugulin <code@efugulin.com>"
__license__ = "GPL v3"


class Book:
    SUPPORTED_FORMATS = ["EPUB", "PDF"]

    def __init__(self, db, book_id):
        self.file_path = None
        self.format = None

        formats = db.formats(book_id)
        if len(formats) > 0:
            for supported_format in self.SUPPORTED_FORMATS:
                if supported_format in formats:
                    self.format = supported_format
                    self.file_path = db.format_abspath(book_id, self.format)
                    break
