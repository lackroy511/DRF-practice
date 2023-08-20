

from users.models import Subscription


def get_users_emails_from_subs(subs: Subscription):
    
    if subs:
        emails = []
        for sub in subs:
            emails.append(sub.user.email)
    
    return emails
