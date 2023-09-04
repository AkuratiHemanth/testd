import pyparsing as pp

pp.ParserElement.enable_packrat()

class SavedTextNode:
    def __init__(self, s, loc, tokens):
        start_pos = tokens[0]
        if len(tokens) == 3:
            end_pos = tokens[2]
        else:
            end_pos = loc
        self.text = s[start_pos:end_pos]
        assert len(tokens[1]) == 1
        self.tokens = tokens[1][0]

def SavedText(node):
    return pp.Located(node).add_parse_action(SavedTextNode)

program = pp.Forward()
program_chunk = pp.Forward()


def format_chat_template(text):
    user_role = "{{#user}}"
    assistant_role = "{{#assistant}}"
    gen_command = "{{gen 'write'}}"
    

    if not text.startswith(user_role):
        text = user_role + text
    
    if not text.endswith(gen_command):
        text += assistant_role + gen_command
    
    text = text.replace("{{gen ", "{{/user}} {{#assistant}}{{gen ")
    return text
