from random import choice, randint

NAME = 'shibe'
AUTHOR = 'aji <http://ajitek.net>'
VERSION = '1.0'
LICENSE = 'MIT'
DESC = 'wow such colors'

CMD_DESC = 'doge'
CMD_ARGS = '<text>'
CMD_ARGS_DESC = '''
   wow
            such shibe
  doge chats
                    talking
    wow'''

COLORS = ['3','4','6','7','8','9','10','11','12','13']

def gen_prefix():
    return ' ' * randint(0, 40) + '\3' + choice(COLORS).rjust(2, "0")

def cmd_shibe(data, buf, args):
    weechat.command(buf, gen_prefix() + args)
    return weechat.WEECHAT_RC_OK

if __name__ == '__main__':
    import weechat
    weechat.register(NAME, AUTHOR, VERSION, LICENSE, DESC, '', '')
    weechat.hook_command('shibe', CMD_DESC, CMD_ARGS, CMD_ARGS_DESC,
                         '', 'cmd_shibe', '')
