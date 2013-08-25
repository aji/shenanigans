import weechat as w
import re
weechat = w

SCRIPT_NAME    = "welshify"
SCRIPT_AUTHOR  = "aji"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "Transform all your input to welsh, based on uppercase.py"

# script options
settings = {
}

if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
                    SCRIPT_DESC, "", ""):
    for option, default_value in settings.iteritems():
        if w.config_get_plugin(option) == "":
            w.config_set_plugin(option, default_value)

    # Hooks we want to hook
    hook_command_run = {
        "input" : ("/input return",  "command_run_input"),
    }
    # Hook all hooks !
    for hook, value in hook_command_run.iteritems():
        w.hook_command_run(value[0], value[1], "")


def command_run_input(data, buffer, command):
    """ Function called when a command "/input xxxx" is run """
    if command == "/input return": # As in enter was pressed.

        # Get input contents
        input_s = w.buffer_get_string(buffer, 'input')
        if input_s.startswith('/') and not input_s.startswith('//'):
            return w.WEECHAT_RC_OK
        # Transform it 
        input_s = ' '.join([''.join(sorted(x)) for x in input_s.split()])
        # Spit it out
        w.buffer_set(buffer, 'input', input_s)
    return w.WEECHAT_RC_OK
