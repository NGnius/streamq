'''
Encoding and decoding to user-readable identifiers ("codes") from integer identifiers

Created 2019-05-31 by NGnius
'''

READABLE_CHARS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    ]

class Code():
    def __init__(self, id=None, code=None):
        if id is not None:
            self.id = id
            self.code = id2code(id)
        elif code is not None:
            self.code = code
            self.id = code2id(code)

    def __eq__(self, other):
        if not isinstance(other, Code):
            return False
        return (self.id == other.id) and (self.code == other.code)

    def __str__(self):
        return self.code

def code2id(code):
    pos = 0
    result = 0
    radix = len(READABLE_CHARS)
    code = code.upper()
    for c in code:
        result += (radix**pos)*READABLE_CHARS.index(c)
        pos += 1
    return result

def id2code(id):
    result = ''
    radix = len(READABLE_CHARS)
    m_id = int(id)
    if id == 0:
        return str(READABLE_CHARS[id])
    while m_id != 0:
        rem = m_id % radix
        result += READABLE_CHARS[rem]
        m_id = m_id // radix
    return result
