from random import choice, random, randint

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

class pvec:
    def __init__(self, num):
        self.v = [1.0] * num
        self.norm()
    def norm(self):
        s = sum(self.v)
        self.v = [x / s for x in self.v]
    def pick(self):
        r = random() * sum(self.v) # sum should always be 1, but meh
        s = 0
        for i, x in enumerate(self.v):
            s += x
            if r < s:
                break
        def calc(j, x):
            fac = (1 - 4.0 / (abs(i - j) + 4.5))
            return x * fac
        self.v = [calc(j, x) for j, x in enumerate(self.v)]
        self.norm()
        weechat.prnt('', str(self.v))
        return i

spvec = pvec(40)

def gen_prefix():
    return ' ' * spvec.pick() + '\3' + choice(COLORS).rjust(2, "0")

def cmd_shibe(data, buf, args):
    weechat.command(buf, gen_prefix() + args)
    return weechat.WEECHAT_RC_OK

if __name__ == '__main__':
    import weechat
    weechat.register(NAME, AUTHOR, VERSION, LICENSE, DESC, '', '')
    weechat.hook_command('shibe', CMD_DESC, CMD_ARGS, CMD_ARGS_DESC,
                         '', 'cmd_shibe', '')
