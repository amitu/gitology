from django import template
import clevercss

register = template.Library()

@register.tag(name="clevercss")
def do_clevercss(parser, token):
    nodelist = parser.parse(('endclevercss',))
    parser.delete_first_token()
    return CleverCSSNode(nodelist)

class CleverCSSNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        output = self.nodelist.render(context)
        print clevercss
        return clevercss.convert(output)

