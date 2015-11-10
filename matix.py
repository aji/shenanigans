#!/usr/bin/python

from random import choice, randint
import weechat

NAME = 'matix'
AUTHOR = 'aji <http://ajitek.net>'
VERSION = '1.0'
LICENSE = 'MIT'
DESC = 'matix has u'

CMD_DESC = 'toggle matix to a buffer'
CMD_ARGS = '[off | <time>]'
CMD_ARGS_DESC = '''
use with no arg or "off" to turn off. with "time" value,
send to channel at one line per time (in secs)'''

# the algorithm thing

alphabet = '!@#$%^&*()[]{}?+=\\|",'

def cell_display(c):
    #return '  0123456789abcdefghijklmnopqrstuvwxyz'[c+1]
    if c == 0:
        return ' '
    ch = choice(alphabet)
    if c == -1:
        return '\2' + ch + '\2'
    return '\3' + choice('39') + ch + '\3'

def cell_step(c):
    if c == 0 or c == -1:
        return int(randint(0, 10+c) / 10)
    else:
        return (c + 1) if randint(0, c) < 13 else -1

def cells_display(s):
    return ' '.join([cell_display(c) for c in s])

def cells_step(s):
    return [cell_step(c) for c in s]

def new_cells():
    return [(0 if randint(0, 3) else randint(0, 13)) for x in range(30)]

# the weechat half

targets = {}

def do_matix(data, remaining_calls):
    if not data in targets:
        return
    tgt = targets[data]

    weechat.command(data, cells_display(tgt['cells']))
    tgt['cells'] = cells_step(tgt['cells'])

    return weechat.WEECHAT_RC_OK

def add_target(buf, dur):
    tgt = {}

    if buf in targets:
        tgt = targets[buf]
        weechat.unhook(tgt['timer'])

    else:
        targets[buf] = tgt
        tgt['cells'] = new_cells()

        # call once, since timer won't fire when first set
        do_matix(buf, 0)

    tgt['timer'] = weechat.hook_timer(dur, 0, 0, 'do_matix', buf)

def cancel_target(buf):
    if buf not in targets:
        return

    tgt = targets[buf]
    del targets[buf]

    weechat.unhook(tgt['timer'])

def toggle_target(buf):
    if buf in targets:
        cancel_target(buf)
    else:
        add_target(buf)

def cmd_matix(data, buf, args):
    if len(args) == 0 or args.lower() == 'off':
        cancel_target(buf)
        return weechat.WEECHAT_RC_OK

    dur = int(float(args) * 1000)
    if dur < 10:
        weechat.prnt(buf, 'too fast!')
        return weechat.WEECHAT_RC_ERROR
    add_target(buf, dur)

    return weechat.WEECHAT_RC_OK

if __name__ == '__main__':
    weechat.register(NAME, AUTHOR, VERSION, LICENSE, DESC, '', '')
    weechat.hook_command('matix', CMD_DESC, CMD_ARGS, CMD_ARGS_DESC,
                         '', 'cmd_matix', '')
