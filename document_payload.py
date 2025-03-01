from uuid import uuid4

class DocumentPayload:
    def __init__(self, url: str, text: str, chunk_index: int):
        self.id = str(uuid4())
        self.url = url
        self.text = text
        self.chunk_index = chunk_index

    def to_metadata(self):
        return {
            "url": self.url,
            "chunk_index": self.chunk_index,
        }
