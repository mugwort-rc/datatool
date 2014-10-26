# -*- coding: utf-8 -*-

from base import ParserBase

class LineTextParser(ParserBase):
    def __init__(self, *args, **kwargs):
        super(LineTextParser, self).__init__(*args, **kwargs)

    def countup(self):
        length = 0
        size = self.stream.datasize()
        readed = 0
        while size > readed:
            data = self.stream.nextdata()
            readed += len(data)
            length += self._linecount(data)
        self.stream.reset()
        return length

    def _linecount(self, data):
        cret = False
        try:
            data.index('\r')
            cret = True
        except ValueError:
            cret = False
        result = 0
        pos = 0
        while True:
            if cret:
                try:
                    cr = data.index('\r', pos)
                    lf = data.index('\n', pos)
                    ret = min(cr, lf)
                    crlf = 0
                    if ret == cr and data[ret+1] == '\n':  # is it CRLF?
                        crlf = 1
                    pos = ret + 1 + crlf
                    result += 1
                except ValueError:
                    cret = False
                    continue
            else:
                try:
                    ret = data.index('\n', pos)
                    pos = ret + 1
                    result += 1
                except ValueError:
                    break  # end of line
        return result

class CSVTextParser(LineTextParser):
    def countup(self):
        length = 0
        for row in csv.reader(self.stream.ptr()):
            length += 1
        self.stream.reset()
        return length

