#!/usr/bin/python

import weechat

NAME = 'rix'
AUTHOR = 'aji <http://ajitek.net>'
VERSION = '1.0'
LICENSE = 'MIT'
DESC = 'rix ur friends'

CMD_DESC = 'repeat a command at some interval'
CMD_ARGS = '[<time> <command>]'
CMD_ARGS_DESC = '''
use with no arg to turn off. with "time" value and command,
run command at one line per time (in secs)'''

# the weechat half

targets = {}

def do_rix(data, remaining_calls):
    if not data in targets:
        return
    tgt = targets[data]

    weechat.command(data, tgt['cmd'])

    return weechat.WEECHAT_RC_OK

def add_target(buf, dur, cmd):
    tgt = { }

    if buf in targets:
        tgt = targets[buf]
    else:
        targets[buf] = tgt

    tgt['cmd'] = cmd
    first_set = True
    if 'timer' in tgt:
        weechat.unhook(tgt['timer'])
        first_set = False
    tgt['timer'] = weechat.hook_timer(dur, 0, 0, 'do_rix', buf)
    if first_set: # timer doesn't fire when first set
        do_rix(buf, 0)

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

def cmd_rix(data, buf, args):
    args = args.split(None, 1)

    if len(args) == 0 or args[0].lower() == 'off':
        cancel_target(buf)
        return weechat.WEECHAT_RC_OK

    dur = int(float(args[0]) * 1000)
    if dur < 10:
        weechat.prnt(buf, 'too fast!')
        return weechat.WEECHAT_RC_ERROR
    add_target(buf, dur, args[1])

    return weechat.WEECHAT_RC_OK

if __name__ == '__main__':
    weechat.register(NAME, AUTHOR, VERSION, LICENSE, DESC, '', '')
    weechat.hook_command('rix', CMD_DESC, CMD_ARGS, CMD_ARGS_DESC,
                         '', 'cmd_rix', '')
