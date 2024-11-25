import re


def change(s: str) -> str:
    pat = r'/[_*[\]()~`>#\+\-=|{}.!]'
    s = s.replace('\n','').replace('\t','').replace('\r', '')
    for i in pat:
        s.replace(i, f"\\{i}")
    return s
