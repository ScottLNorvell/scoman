import os

import jinja2



def render_str(template, **params):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
    t = jinja_env.get_template(template)
    return t.render(params)