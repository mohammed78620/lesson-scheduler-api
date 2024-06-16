def generate_email_body(name: str, number: str) -> str:
    email_body = f"""
    Subject: Notice: Missed Bookings

    Dear {name},

    We have noticed that you missed {number} bookings recently. This affects our scheduling and other users.

    Please make sure to attend or cancel your bookings in advance. Continued missed bookings may lead to restrictions on your account.

    If you need assistance or have concerns, feel free to contact us.

    Thank you for your understanding.
    """
    return email_body
