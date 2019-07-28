from django import template
from django.template import TemplateSyntaxError, Node

register = template.Library()


@register.tag
def has_perm(parser, token):
    # Separating the tag name from the "test" parameter.
    try:
        tag, test = token.contents.split()
    except (ValueError, TypeError):
        raise TemplateSyntaxError(
            "'%s' tag takes two parameters" % tag)

    default_states = ['has_perm', 'else']
    end_tag = 'endhas_perm'

    # Place to store the states and their values
    states = {}

    # Let's iterate over our context and find our tokens
    while token.contents != end_tag:
        current = token.contents
        states[current.split()[0]] = parser.parse(default_states + [end_tag])
        token = parser.next_token()

    test_var = parser.compile_filter(test)
    return MyNode(states, test_var)


class MyNode(Node):
    def __init__(self, states, test_var):
        self.states = states
        self.test_var = test_var

    def render(self, context):
        # Resolving variables passed by the user
        test_var = self.test_var.resolve(context, True)

        # Rendering the right state. You can add a function call, use a
        # library or whatever here to decide if the value is true or false.
        is_true = bool(test_var)
        # TODO perms
        if test_var == "delete_spell":
            is_true = False
        else:
            is_true = True

        # TODO end perms
        if is_true:
            return self.states["has_perm"].render(context)
        elif "else" in self.states:
            return self.states["else"].render(context)
        return ''
