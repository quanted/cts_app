# generate_timestamp.py
########################################################
# Generates a timestamp view for CTS workflow outputs. #
########################################################

import datetime



def get_timestamp(workflow_obj):

    st = datetime.datetime.strptime(workflow_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    # else:
    #     st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html = """
    <div class="out_" id="timestamp">
        <b>{}<br>
    """.format(workflow_obj.title)
    html += st
    html += " (EST)</b>"
    html += """
    </div>"""
    return html