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

## Define the utility function to format text into structured chat templates
def format_chat_template(text):
    user_role = "{{#user}}"
    assistant_role = "{{#assistant}}"
    gen_command = "{{gen 'write'}}"
    
    # Ensure the template starts with a user role
    if not text.startswith(user_role):
        text = user_role + text
    
    # Ensure the template ends with the assistant's gen command
    if not text.endswith(gen_command):
        text += assistant_role + gen_command
    
   text = text.replace("{{gen ", "{{/user}} {{#assistant}}{{gen ")
    return text

# Example usage:
input_text = "how are things going, tell me about Delhi"
formatted_template = format_chat_template(input_text)
print(formatted_template)
