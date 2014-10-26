# -*- coding: utf-8 -*-

import cStringIO
import StringIO

from base import StreamBase

class SourceStream(StreamBase):
    def __init__(self):
        super(SourceStream, self).__init__()

    def __len__(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

class FileSourceStream(StreamBase):

    SIZE = 1024*1024

    def __init__(self, fp):
        super(FileSourceStream, self).__init__()
        self._fp = fp

    def __len__(self):
        cur = self._fp.tell()  # save current
        self._fp.seek(0, 2)  # seek to end
        res = self._fp.tell()  # get size
        self._fp.seek(cur)  # seek to current
        return res

    def ptr(self):
        return self._fp

    def next(self):
        return self._fp.read(self.SIZE)

    def reset(self):
        self._fp.seek(0)

class MemorySourceStream(FileSourceStream):
    def __init__(self, fp):
        if isinstance(fp, str):
            fp = cStringIO.StringIO(fp)
        elif isinstance(fp, unicode):
            try:
                fp = cStringIO.StringIO(fp)
            except UnicodeEncodeError:
                fp = StringIO.StringIO(fp)
        super(MemorySourceStream, self).__init__(fp)

