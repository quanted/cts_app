from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail
from .links_left import ordered_list
import os
import logging
import datetime
import time
import json

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))



def handle_contact_post(request):
    """
    Handles CTS contacts page comment submission form POST.
    Stores comments in a json file.
    TODO: Use DB instead of reading/writing to file.
    TODO: Cron job that sends email out, say weekly.
    """
    comments, comments_json = None, None
    comments_file_path = os.path.join(PROJECT_ROOT, 'cts_comments.json')
    post_data = request.POST
    name = request.POST.get('name', "none") or "none"  # additional or accounts for blank string
    from_email = request.POST.get('email', "none") or "none"
    comment = request.POST.get('comment')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    comment_obj = {
        'name': name,
        'from_email': from_email,
        'comment': comment,
        'timestamp': timestamp
    }

    try:
        comments_file = open(comments_file_path, 'r')
        comments_content = comments_file.read()
        comments_file.close()
        comments_json = json.loads(comments_content)
    except FileNotFoundError as e:
        comments_file = open(comments_file_path, 'w')
        comments_json = {}
    except Exception as e:
        logging.warning("Exception occurred handling contact submission: {}".format(e))
        return

    if not comments_json:
        # Writes first entry to comments file:
        main_comments_obj = {'num_comments': 1, 'comments': [comment_obj]}
        comments_file.write(json.dumps(main_comments_obj))  # list of comments_json objects
        comments_file.close()
        return contacts_submission_view(request)

    # Adds comment to existing comments file:
    comments_json['comments'].append(comment_obj)
    comments_json['num_comments'] += 1
    comments_file = open(comments_file_path, 'w')
    comments_file.write(json.dumps(comments_json))
    comments_file.close()
    return contacts_submission_view(request)



# def send_email_using_smtp():
#     """
#     Handled contacts page comment submission by sending email
#     to cts email using an smtp server.
#     """
#     to_email = ""  # address to send comment to
#     post_data = request.POST
#     name = str(request.POST.get('name', "no-name"))
#     from_email = str(request.POST.get('email', "<none>"))
#     comment = str(request.POST.get('comment'))
#     email_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     subject = "{}-{}".format(name, email_timestamp)
    
#     # TODO: Add validation for name, email addresses, and comments (check
#     # for injected headers, code, etc.). Ensure spam and multiple-requests attacks
#     # are blocked.

#     email_body = render_to_string('cts_email_submission_template.html', {
#         'name': name,
#         'from_email': from_email,
#         'email_timestamp': email_timestamp,
#         'comment': comment
#     })

#     if comment:
#         try:
#             send_mail(subject, email_body, from_email, [to_email], html_message=email_body)
#             time.sleep(1)  # NOTE: Not sure if neccessary, and not sure if works as intended, which is to prevent a high-freq spamming to our email system.
#         except BadHeaderError:
#             return HttpResponse("Invalid header found.")
#         return contacts_submission_view(request)
#     else:
#         return HttpResponse("Make sure all fields are entered and valid.")



def contacts_submission_view(request):
    """
    Page that displays after an email has been sent by
    the user on the contacts page.
    """
    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})
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