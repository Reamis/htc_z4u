import re

white_space = re.compile(r"(\t| )+\n")

pattern = re.compile(
    r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
    re.DOTALL | re.MULTILINE
)

pattern_white_space = re.compile(r'\s+')


def removeCCppComment(text):

    def replacer(match):
        s = match.group(0)
        # Matched string is
        # //...EOL or /*...*/  ==> Blot out all non-newline chars
        if s.startswith('/'):
            return ' '
        # Matched string is '...' or "..."  ==> Keep unchanged
        else:
            return s

    return re.sub(pattern, replacer, text)


def get_hash(text, strip):
    cleaned_up_text = removeCCppComment(text)
    # drop whitespaces
    cleaned_up_text = re.sub(pattern_white_space, '\n', cleaned_up_text)
    if strip:
        # for compare case
        return cleaned_up_text.strip()
    else:
        # for search patern case
        return cleaned_up_text


def replace_space_at_start(text):
    splited = text.split("\n")
    for i in xrange(len(splited)):
        pos = 0
        while pos < len(splited[i]) and splited[i][pos] == ' ':
            pos = pos + 1
        if pos > 0:
            tabs = int(pos/8)
            splited[i] = ("\t" * tabs) + splited[i][tabs * 8:]
    return "\n".join(splited)


def cleanup(text):
    text = re.sub(white_space, "\n", text)
    return replace_space_at_start(text)
