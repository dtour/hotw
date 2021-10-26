import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import url_for

def send_reset_email(user):
    token = user.get_reset_token()

    message = Mail(
    from_email='dtour@hotw.app',
    to_emails=[user.email],
    subject='Password Reset Request',
    html_content=
    f'''To reset your password, visit the following link within the next hour:
<br> {url_for('reset_token', token=token, _external=True)}
    
<br> If you did not make this request then simply ignore this email and no changes will be made.
'''
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    sg.send(message)

def send_join_group_email(group, inviter, invitee):
    token = group.get_join_group_token()

    message = Mail(
    from_email='dtour@hotw.app',
    to_emails=[invitee],
    subject=f'{inviter.email} has invited you to join their Highlight of the Week group',
    html_content=
    f'''To join {inviter.email}'s group, please click on the link below:
<br> {url_for('join_group', token=token, _external=True)}
    
'''
    )

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    sg.send(message)

    pass