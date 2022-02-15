from .song import Song

class Queue:
    def __init__(self):
        self._queue = []
        self._pos = 0

    def __len__(self) -> int:
        return len(self.queue[self.pos:])

    @property
    def is_empty(self) -> bool:
        if len(self._queue[self._pos + 1:]) == 0:
            return True
        else:
            return False

    @property
    def queue(self) -> list[Song]:
        return self._queue

    @property
    def pos(self) -> int:
        return self._pos

    @pos.setter
    def pos(self, new):
        if isinstance(new, int):
            self._pos = new
        else:
            raise TypeError(new)

    def clear(self):
        song = self.queue[self.pos]
        self.queue.clear()
        self.queue.append(song)

    def move(self, source_index, dest_index):
        song = self.queue[source_index]
        self.queue.remove(song)
        self.queue.insert(dest_index, song)

    def add(self, song: Song):
        self.queue.append(song)

    def remove(self, song: Song):
        self.queue.remove(song)

    def get(self, index = None) -> Song:
        if index is None:
            index = self.pos
        return self.queue[index]

    def previous(self) -> Song:
        self.pos -= 1
        return self.get()

    def next(self) -> Song:
        self.pos += 1
        return self.get()