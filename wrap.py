from random import choice, random, randint
import re

NAME = 'wrap'
AUTHOR = 'aji <http://ajitek.net>'
VERSION = '1.0'
LICENSE = 'MIT'
DESC = 'wraps your lines'

CMD_DESC = 'wrap'
CMD_ARGS = '[-<width>] <text>'
CMD_ARGS_DESC = ''' Wraps your lines, dawg. '''

def wrap(w, ln):
    s = ''
    for word in ln.split():
        if len(word) + 1 > w:
            if len(s) > 0:
                yield s[1:]
            yield word
            s = ''
            continue
        nx = s + ' ' + word
        if len(nx) > w:
            yield s[1:]
            s = ' ' + word
        else:
            s = nx
    if len(s) > 0:
        yield s[1:]

def send_line(b, ln):
    weechat.command(b, '/say ' + ln)

def cmd_wrap(data, buf, args):
    width = 70
    text = args

    m = re.match('-(\d+) (.*)', args)
    if m is not None:
        width, text = m.groups()
        width = int(width)

    for line in wrap(width, text):
        send_line(buf, line)

    return weechat.WEECHAT_RC_OK

if __name__ == '__main__':
    import weechat
    weechat.register(NAME, AUTHOR, VERSION, LICENSE, DESC, '', '')
    weechat.hook_command('wrap', CMD_DESC, CMD_ARGS, CMD_ARGS_DESC,
                         '', 'cmd_wrap', '')
