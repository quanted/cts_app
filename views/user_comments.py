from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail
from .links_left import ordered_list
import os
import logging
import datetime
import time
import json
import requests
import smtplib
import bleach
from .misc import generate_error_page


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
QED_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

recaptcha_verify_url = "https://google.com/recaptcha/api/siteverify"  # POST


def handle_contact_post(request):
    """
    Handles CTS contacts page comment submission form POST.
    Stores comments in a json file.
    TODO: Use DB instead of reading/writing to file.
    TODO: Cron job that sends email out, say weekly.
    """
    name = bleach.clean(request.POST.get("name"))
    from_email = bleach.clean(request.POST.get("email"))
    comment = bleach.clean(request.POST.get("comment"))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    recaptcha_response = request.POST.get("g-recaptcha-response")

    valid_recaptcha = validate_recaptcha(recaptcha_response)

    if not validate_recaptcha:
        html = generate_error_page("Recaptcha not valid", "Sorry, the comment was not submitted. Please try again.")
        response = HttpResponse()
        response.write(html)
        return response

    comment_obj = {
        "name": name,
        "from_email": from_email,
        "comment": comment,
        "timestamp": timestamp
    }

    subject = "CTS comment from {}".format(from_email)
    message = """
    User: {}\n
    Email: {}\n
    Submitted: {}\n
    Server: {}\n
    Comment: {}\n
    """.format(
        name,
        from_email,
        timestamp,
        os.getenv("CTS_REST_SERVER").split("://")[1],
        comment
    )

    if os.getenv('ENV_NAME') in ["epa_aws_dev", "epa_aws_stg", "epa_aws_prd"]:
        email_response = send_email_epa(subject, message)
    else:
        email_response = send_email(subject, message)

    if "error" in email_response:
        html = generate_error_page("Error validating recaptcha", "Sorry, the comment was not submitted. Please try again.")
        response = HttpResponse()
        response.write(html)
        return response

    return contacts_submission_view(request)

def validate_recaptcha(recaptcha):
    """
    Checks user response to verify recaptcha validity.
    """
    if len(recaptcha) <= 0:
        # error
        return False

    secret_key = get_key(os.path.join(QED_ROOT, "secrets", "secret_key_recaptcha.txt"))

    if not secret_key:
        secret_key = os.getenv("CTS_RECAPTCHA_KEY")

    post_obj = {
        "secret": secret_key,  # shared key b/w site and recaptcha
        "response": recaptcha  # user resp token provided by the recaptcha client-side integration on your site
    }

    try:
        response = requests.post(url=recaptcha_verify_url, data=post_obj)
        result = json.loads(response.content)
    except Exception as e:
        logging.error("user_comments validate_recaptcha error: {}".format(e))
        return False

    if not "success" in result or result["success"] != True:
        return False
    else:
        return True 

def get_key(key_path):
    """
    Gets site/secret keys on disk.
    """
    try:
        with open(key_path, "r") as file:
            return file.read()
    except Exception as e:
        logging.error("user_comments get_key error: {}".format(e))
        return False

def send_email(subject, message):

    to_email = os.getenv("CTS_EMAIL_RECIPIENTS").replace(" ", "").split(",")  # list of recipients
    smtp_email = os.getenv("CTS_EMAIL")
    smtp_pass = get_key(os.path.join(QED_ROOT, "secrets", "secret_key_cts_email.txt"))

    if not smtp_pass:
        smtp_pass = os.getenv("CTS_EMAIL_PASS")

    smtp_email_server = "smtp.gmail.com"
    smtp_email_port = 465

    msg = "\r\n".join(
        [
            "From: {}".format(smtp_email),
            "To: {}".format(to_email),
            "Subject: {}".format(subject),
            "",
            message,
        ]
    )

    try:
        server = smtplib.SMTP_SSL(smtp_email_server, smtp_email_port)
        server.ehlo()
        server.login(smtp_email, smtp_pass)
        server.sendmail(smtp_email, to_email, msg)
        server.close()
        return {"success": "Email sent."}
    except Exception as e:
        logging.warning("Error sending reset email: {}".format(e))
        return {"error": "Unable to send email."}

def send_email_epa(subject, message):

    to_email = os.getenv("CTS_EMAIL_RECIPIENTS").replace(" ", "").split(",")  # list of recipients
    smtp_email = os.getenv("CTS_EMAIL")
    smtp_email_server = "smtp.epa.gov"
    smtp_email_port = 25

    msg = "\r\n".join(
        [
            "From: {}".format(smtp_email),
            "To: {}".format(to_email),
            "Subject: {}".format(subject),
            "",
            message,
        ]
    )

    try:
        server = smtplib.SMTP(smtp_email_server, smtp_email_port)
        server.ehlo()
        server.sendmail(smtp_email, to_email, msg)
        server.close()
        return {"success": "Email sent."}
    except Exception as e:
        logging.warning("Error sending reset email: {}".format(e))
        return {"error": "Unable to send email."}

def contacts_submission_view(request):
    """
    Page that displays after an email has been sent by
    the user on the contacts page.
    """
    html = render_to_string('01cts_epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {"version": os.getenv("CTS_VERSION")})
    html += render_to_string('06cts_ubertext_start_index_drupal.html', {
        'TITLE': "Thank you for your comments!",
        'TEXT_PARAGRAPH': """An email has been sent to the CTS team.<br>
            If a return email address was provided, we'll get back to you as soon as possible.<br><br>
            <!--Return to <a href="/cts">homepage</a>.-->
            <form action="/cts" method="get">
                <input type="submit" value="Go back CTS homepage" />
            </form>
            """
    })
    html += render_to_string('07ubertext_end_drupal.html', {})
    html += ordered_list(model='cts')  # fills out 05ubertext_links_left_drupal.html
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('09epa_drupal_cts_css.html')
    html += render_to_string('09epa_drupal_cts_scripts.html')
    html += render_to_string('10epa_drupal_footer.html', {})
    response = HttpResponse()
    response.write(html)
    return response
