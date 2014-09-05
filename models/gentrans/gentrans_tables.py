"""
.. module:: gentrans_tables
   :synopsis: A useful module indeed.
"""

# import numpy
from django.template import Context, Template
# from django.utils.safestring import mark_safe
# import logging
# import time
import datetime
from django.template.loader import render_to_string

# logger = logging.getLogger("gentransTables")

def getheaderpvu():
    headings = ["Parameter", "Value", "Units"]
    return headings

def getheaderpvr():
	headings = ["Parameter", "Acute", "Chronic","Units"]
	return headings

# def getheaderpvrqaqc():
#     headings = ["Parameter", "Acute", "Acute-Expected", "Chronic", "Chronic-Expected","Units"]
#     return headings

# def getheadersum():
#     headings = ["Parameter", "Mean", "Std", "Min", "Max", "Unit"]
#     return headings

def gethtmlrowsfromcols(data, headings):
    columns = [data[heading] for heading in headings]

    # get the length of the longest column
    max_len = len(max(columns, key=len))

    for col in columns:
        # padding the short columns with None
        col += [None,] * (max_len - len(col))

    # Then rotate the structure...
    rows = [[col[i] for col in columns] for i in range(max_len)]
    return rows

def getdjtemplate():
    dj_template ="""
    <table class="out_">
    {# headings #}
        <tr>
        {% for heading in headings %}
            <th>{{ heading }}</th>
        {% endfor %}
        </tr>
    {# data #}
    {% for row in data %}
    <tr>
        {% for val in row %}
        <td>{{ val|default:'' }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
    </table>
    """
    return dj_template

def gett1data(gentrans_obj):
    data = { 
        "Parameter": ['Number of Decimals', 'pH Lower Limit', 'pH Upper Limit', 'pH Step Size','Generate Major Microspecies at pH', 'Isoelectric Point (pl) pH Step Size of Charge Distribution', 'Maximum Number of Structures', 'at pH', 'Maximum Number of Structures'],
        "Value": [gentrans_obj.pKa_decimals, gentrans_obj.pKa_pH_lower, gentrans_obj.pKa_pH_upper, gentrans_obj.pKa_pH_increment, gentrans_obj.pH_microspecies, gentrans_obj.isoelectricPoint_pH_increment, gentrans_obj.tautomer_maxNoOfStructures, gentrans_obj.tautomer_maxNoOfStructures_pH, gentrans_obj.stereoisomers_maxNoOfStructures],
        "Units": ['', '', '', '', '', '', '', ''],
    }
    return data

# def gett1dataqaqc(sip_obj):
#     data = { 
#         "Parameter": ['Chemical Name',mark_safe('Solubility (in water @25&deg;C)'),mark_safe('Mammalian LD<sub>50</sub>'),'Body Weight of Tested Mammal','Body Weight of Assessed Mammal','Mammalian NOAEL',mark_safe('Avian LD<sub>50</sub>'),'Body Weight of Tested Bird','Body Weight of Assessed Bird','Mineau Scaling Factor','Avian NOAEC',],
#         "Value": [sip_obj.chemical_name_expected,sip_obj.sol,sip_obj.ld50_m,sip_obj.bw_mamm,sip_obj.aw_mamm,sip_obj.noael,sip_obj.ld50_a,sip_obj.bw_bird,sip_obj.aw_bird,sip_obj.mineau,sip_obj.noaec,],
#         "Units": ['','mg/L','mg/kg-bw','g','g','mg/kg-bw','mg/kg-bw','g','g','','mg/kg-diet'],
#     }
#     return data

def gett2data(gentrans_obj):
    data = { 
        "Parameter": ['Basic pKa Value(s)', 'Acidic pKa Value(s)'],
        "Value": [gentrans_obj.basicpKaValues, gentrans_obj.acidicpKaValues],
        "Units": [''],
    }
    return data

# def gett2dataqaqc(sip_obj):
#     data = { 
#         "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
#         "Acute": ['%.3e' % sip_obj.dose_mamm_out, '%.4f' % sip_obj.at_mamm_out, '%.4f' % sip_obj.acute_mamm_out, '%s' % sip_obj.acuconm_out,],
#         "Acute-Expected": ['%.3e' % sip_obj.dose_mamm_out_expected,'%.4f' % sip_obj.at_mamm_out_expected,'%.4f' % sip_obj.acute_mamm_out_expected,'%s' % sip_obj.acuconm_out_expected,],
#         "Chronic": ['%.3e' % sip_obj.dose_mamm_out, '%.4f' % sip_obj.act_out, '%.4f' % sip_obj.chron_mamm_out, '%s' % sip_obj.chronconm_out,],
#         "Chronic-Expected": ['%.3e' % sip_obj.dose_mamm_out_expected,'%.4f' % sip_obj.act_out_expected,'%.4f' % sip_obj.chron_mamm_out_expected,'%s' % sip_obj.chronconm_out_expected,],
#         "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
#     }
#     return data

# def gett3data(sip_obj):
#     data = { 
#         "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
#         "Acute": ['%.5e' % sip_obj.dose_bird_out, '%.4f' % sip_obj.at_bird_out,'%.4f' % sip_obj.acute_bird_out, '%s' % sip_obj.acuconb_out,],
#         "Chronic": ['%.5e' % sip_obj.dose_bird_out, '%.4f' % sip_obj.det_out,'%.4f' % sip_obj.chron_bird_out, '%s' % sip_obj.chronconb_out,],
#         "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
#     }
#     return data

# def gett3dataqaqc(sip_obj):
#     data = { 
#         "Parameter": ['Upper Bound Exposure', 'Adjusted Toxicity Value', 'Ratio of Exposure to Toxicity', 'Conclusion',],
#         "Acute": ['%.5e' % sip_obj.dose_bird_out, '%.4f' % sip_obj.at_bird_out,'%.4f' % sip_obj.acute_bird_out, '%s' % sip_obj.acuconb_out,],
#         "Acute-Expected": ['%.5e' % sip_obj.dose_bird_out_expected, '%.4f' % sip_obj.at_bird_out_expected, '%.4f' % sip_obj.acute_bird_out_expected, '%s' % sip_obj.acuconb_out_expected,],
#         "Chronic": ['%.5e' % sip_obj.dose_bird_out, '%.4f' % sip_obj.det_out,'%.4f' % sip_obj.chron_bird_out, '%s' % sip_obj.chronconb_out,],
#         "Chronic-Expected": ['%.5e' % sip_obj.dose_bird_out_expected,'%.4f' % sip_obj.det_out_expected,'%.4f' % sip_obj.chron_bird_out_expected,'%s' % sip_obj.chronconb_out_expected,],
#         "Units": ['mg/kg-bw', 'mg/kg-bw', '', '',],
#     }
#     return data


# def gettsumdata_out(dose_bird_out, dose_mamm_out, at_bird_out, 
#                     at_mamm_out, det_out, act_out, acute_bird_out, acute_mamm_out, 
#                     chron_bird_out, chron_mamm_out):
#     data = {
#         "Parameter": ['Upper Bound Exposure - Avian', 'Upper Bound Exposure - Mammalian',
#                     'Adjusted Toxicity Value (Acute) - Avian',
#                     'Adjusted Toxicity Value (Acute) - Mammalian',
#                     'Adjusted Toxicity Value (Chronic) - Avian',
#                     'Adjusted Toxicity Value (Chronic) - Mammalian',
#                     'Ratio of Exposure to Toxicity (Acute) - Avian',
#                     'Ratio of Exposure to Toxicity (Acute) - Mammalian',
#                     'Ratio of Exposure to Toxicity (Chronic) - Avian',
#                     'Ratio of Exposure to Toxicity (Chronic) - Mammalian',],

#         "Mean": [
#                  '%.2e' % numpy.mean(dose_bird_out), '%.2e' % numpy.mean(dose_mamm_out), '%.2e' % numpy.mean(at_bird_out),
#                  '%.2e' % numpy.mean(at_mamm_out), '%.2e' % numpy.mean(act_out), '%.2e' % numpy.mean(det_out),
#                  '%.2e' % numpy.mean(acute_bird_out), '%.2e' % numpy.mean(acute_mamm_out),
#                  '%.2e' % numpy.mean(chron_bird_out), '%.2e' % numpy.mean(chron_mamm_out),],

#         "Std": ['%.2e' % numpy.std(dose_bird_out), '%.2e' % numpy.std(dose_mamm_out), '%.2e' % numpy.std(at_bird_out),
#                 '%.2e' % numpy.std(at_mamm_out), '%.2e' % numpy.std(act_out), '%.2e' % numpy.std(det_out),
#                 '%.2e' % numpy.std(acute_bird_out), '%.2e' % numpy.std(acute_mamm_out),
#                 '%.2e' % numpy.std(chron_bird_out), '%.2e' % numpy.std(chron_mamm_out),],

#         "Min": ['%.2e' % numpy.min(dose_bird_out), '%.2e' % numpy.min(dose_mamm_out), '%.2e' % numpy.min(at_bird_out),
#                 '%.2e' % numpy.min(at_mamm_out), '%.2e' % numpy.min(act_out), '%.2e' % numpy.min(det_out),
#                 '%.2e' % numpy.min(acute_bird_out), '%.2e' % numpy.min(acute_mamm_out),
#                 '%.2e' % numpy.min(chron_bird_out), '%.2e' % numpy.min(chron_mamm_out),],

#          "Max": ['%.2e' % numpy.max(dose_bird_out), '%.2e' % numpy.min(dose_mamm_out), '%.2e' % numpy.min(at_bird_out),
#                 '%.2e' % numpy.max(at_mamm_out), '%.2e' % numpy.max(act_out), '%.2e' % numpy.min(det_out),
#                 '%.2e' % numpy.max(acute_bird_out), '%.2e' % numpy.min(acute_mamm_out),
#                 '%.2e' % numpy.max(chron_bird_out), '%.2e' % numpy.max(chron_mamm_out),],

#         "Unit": ['mg/kg-bw', 'mg/kg-bw','mg/kg-bw', 'mg/kg-bw', 'mg/kg-bw', 'mg/kg-bw', '','', '', '',],
#     }
#     return data


pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
# pvrheadingsqaqc = getheaderpvrqaqc()
# sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(gentrans_obj):
    # html_all = render_to_string(timestamp)
    html_all = table_1(gentrans_obj)      
    html_all = html_all + table_2(gentrans_obj)
    #html_all = html_all + table_3(gentrans_obj)
    return html_all

# def table_all_qaqc(sip_obj):
#     html_all = table_1_qaqc(sip_obj)
#     html_all = html_all + table_2_qaqc(sip_obj)
#     html_all = html_all + table_3_qaqc(sip_obj)
#     return html_all

def timestamp(gentrans_obj="", batch_jid=""):
    if gentrans_obj:
        st = datetime.datetime.strptime(gentrans_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>SIP <a href="http://www.epa.gov/oppefed1/models/terrestrial/sip/sip_user_guide.html">Version 1.0</a> (Beta)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html

def table_1(gentrans_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Application and Chemical Information</H4>
                <div class="out_ container_output">
        """
        t1data = gett1data(gentrans_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html

# def table_1_qaqc(sip_obj):
#         html = """
#         <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
#         <div class="out_">
#             <H4 class="out_1 collapsible" id="section2"><span></span>Application and Chemical Information</H4>
#                 <div class="out_ container_output">
#         """
#         t1data = gett1dataqaqc(sip_obj)
#         t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
#         html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
#         html = html + """
#                 </div>
#         </div>
#         """
#         return html

def table_2(gentrans_obj):
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section3"><span></span>Chemical Speciation Output</H3>
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section4"><span></span>pKa Values</H4>
                <div class="out_ container_output">
        """
        t2data = gett2data(gentrans_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
        return html  

# def table_2_qaqc(sip_obj):
#         html = """
#         <br>
#         <H3 class="out_1 collapsible" id="section3"><span></span>SIP Output</H3>
#         <div class="out_1">
#             <H4 class="out_1 collapsible" id="section4"><span></span>Mammalian Results (%s g)</H4>
#                 <div class="out_ container_output">
#         """%(sip_obj.aw_mamm)
#         t2data = gett2dataqaqc(sip_obj)
#         t2rows = gethtmlrowsfromcols(t2data,pvrheadingsqaqc)
#         html = html + tmpl.render(Context(dict(data=t2rows, headings=pvrheadingsqaqc)))
#         html = html + """
#                 </div>
#         """
#         return html  

# def table_3(sip_obj):
#         html = """
#             <H4 class="out_1 collapsible" id="section4"><span></span>Avian Results (%s g)</H4>
#                 <div class="out_ container_output">
#         """%(sip_obj.aw_bird)
#         t3data = gett3data(sip_obj)
#         t3rows = gethtmlrowsfromcols(t3data,pvrheadings)
#         html = html + tmpl.render(Context(dict(data=t3rows, headings=pvrheadings)))
#         html = html + """
#                 </div>
#         </div>
#         """
#         return html

# def table_3_qaqc(sip_obj):
#         html = """
#             <H4 class="out_1 collapsible" id="section4"><span></span>Avian Results (%s g)</H4>
#                 <div class="out_ container_output">
#         """%(sip_obj.aw_bird)
#         t3data = gett3dataqaqc(sip_obj)
#         t3rows = gethtmlrowsfromcols(t3data,pvrheadingsqaqc)
#         html = html + tmpl.render(Context(dict(data=t3rows, headings=pvrheadingsqaqc)))
#         html = html + """
#                 </div>
#         </div>
#         """
#         return html


# def table_all_sum(sumheadings, tmpl, bw_quail,bw_duck,bwb_other,bw_rat,bwm_other,sol,
#                     avian_ld50,mammalian_ld50,aw_bird,mineau,aw_mamm,noaec,noael,
#                     dose_bird_out, dose_mamm_out, at_bird_out, 
#                     at_mamm_out, det_out, act_out, acute_bird_out, acute_mamm_out, 
#                     chron_bird_out, chron_mamm_out):
#     html_all_sum = table_sum_input(sumheadings, tmpl, bw_quail,bw_duck,bwb_other,bw_rat,bwm_other,sol,
#                     avian_ld50,mammalian_ld50,aw_bird,mineau,aw_mamm,noaec,noael)
#     html_all_sum += table_sum_output(sumheadings,tmpl,dose_bird_out,dose_mamm_out,at_bird_out, 
#                     at_mamm_out,det_out,act_out,acute_bird_out,acute_mamm_out,chron_bird_out,chron_mamm_out)
#     return html_all_sum

# def table_sum_input(sumheadings, tmpl, bw_quail,bw_duck,bwb_other,bw_rat,bwm_other,sol,
#                     avian_ld50,mammalian_ld50,aw_bird,mineau,aw_mamm,noaec,noael):
#         html = """
#         <H3 class="out_1 collapsible" id="section1"><span></span>Summary Statistics</H3>
#         <div class="out_">
#             <H4 class="out_1 collapsible" id="section4"><span></span>Batch Inputs</H4>
#                 <div class="out_ container_output">
#         """
#         tsuminputdata = gettsumdata(bw_quail,bw_duck,bwb_other,bw_rat,bwm_other,sol,avian_ld50,mammalian_ld50,aw_bird,mineau,aw_mamm,noaec,noael)
#         tsuminputrows = gethtmlrowsfromcols(tsuminputdata, sumheadings)
#         html = html + tmpl.render(Context(dict(data=tsuminputrows, headings=sumheadings)))
#         html = html + """
#                 </div>
#         """
#         return html

# def table_sum_output(sumheadings, tmpl, dose_bird_out, dose_mamm_out, at_bird_out, 
#                     at_mamm_out, det_out, act_out, acute_bird_out, acute_mamm_out, 
#                     chron_bird_out, chron_mamm_out):
#         html = """
#         <br>
#             <H4 class="out_1 collapsible" id="section3"><span></span>SIP Outputs</H4>
#                 <div class="out_ container_output">
#         """
#         tsumoutputdata = gettsumdata_out(dose_bird_out, dose_mamm_out, at_bird_out, 
#                     at_mamm_out, det_out, act_out, acute_bird_out, acute_mamm_out, 
#                     chron_bird_out, chron_mamm_out)
#         tsumoutputrows = gethtmlrowsfromcols(tsumoutputdata, sumheadings)
#         html = html + tmpl.render(Context(dict(data=tsumoutputrows, headings=sumheadings)))
#         html = html + """
#                 </div>
#         </div>
#         """
#         return html

