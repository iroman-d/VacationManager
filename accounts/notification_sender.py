import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pathlib import Path
from jinja2 import Environment
from jinja2 import FileSystemLoader


def render_template(template, **kwargs):
    ''' renders a Jinja template into HTML '''
    path = Path(__file__).parent
    path = (str(path)+'/email_templates')
    env = Environment(loader=FileSystemLoader(path), keep_trailing_newline=True)
    template = env.get_template('email.html')
    output = template.render(**kwargs)

    return output


def send_email(to, subject, template):
    message = Mail(
        from_email='from_email@example.com',
        to_emails=to,
        subject=subject,
        html_content=template)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
