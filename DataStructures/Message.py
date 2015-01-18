__author__ = 'nncsang'
import re

class Message:
    def __init__(self, message_type = None, message_args = None, message_payload = ""):
        self.type = message_type;
        self.args = message_args;
        self.payload = message_payload;

    def parse(self, buf):
        consumed = 0;
        match = re.match("(?P<type>\w+) (?P<len>\d+)(?P<args>( \S+)*)\n", buf)

        if (match):
            hlen = match.end();

            m_type = match.groupdict()["type"]
            m_len = int(match.groupdict()["len"])
            m_args = [i for i in match.groupdict()["args"].strip().split(" ") if len(i) > 0]

            if len(buf) >= hlen + m_len:
                m_payload = buf[hlen: hlen + m_len]
                consumed = hlen + m_len;

                self.type = m_type;
                self.args = m_args;
                self.payload = m_payload;

        return consumed

    def __str__(self):
        if len(self.args):
            return "%s %d %s\n" % (self.type, len(self.payload),  " ".join(map(str, self.args)) + self.payload)
        else:
            return "%s %d %s\n" % (self.type, len(self.payload), self.payload)

# m = Message("PUT", ["token_id"], "Hello World")
# print (str(m))
# m.parse("PUT 12 token_id\n Hello World")
# print(m.type)
# print(m.args)
# print(m.payload)


