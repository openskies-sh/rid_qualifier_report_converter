import json
import dominate
from dominate.tags import *
from pathlib import Path
import pathlib
import os, sys
import tldextract
import arrow
import argparse

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Process RID Qualifier report json')
    parser.add_argument('-f','--file', dest='file',
                    help='A path to the report.json that you have genreated')
    args = parser.parse_args()
    cur_dir = pathlib.Path(__file__).parent.absolute()
    os.chdir(cur_dir)

    try:
        report_file = args.file
    except TypeError as te:        
        sys.exit()
    
    try: 
        assert os.path.isfile(report_file)
    except TypeError as te: 
        print("Report JSON not found")
        sys.exit()
            
    except AssertionError as ae: 
        print("Valid file not supplied")
        sys.exit()
    else: 
        with open(report_file, 'r') as raw_report:
            report_json = json.load(raw_report)

        injection_targets = report_json['setup']['configuration']['injection_targets']
        observers = report_json['setup']['configuration']['observers']
        evaluation = report_json['setup']['configuration']['evaluation']
        findings = report_json['findings']
        
    formatted_now = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')

    output_directory = Path('output')    
    output_directory.mkdir(parents=True, exist_ok=True)

    input_directory = Path('input')    
    input_directory.mkdir(parents=True, exist_ok=True)


    doc = dominate.document(title='RID Qualifier Report')
    with doc.head:
        link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css')
        script(type='text/javascript', src='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js')

    with doc.body:
        with main():
            with div(cls="container py-4"):
                with div(cls="p-5 mb-4 bg-light rounded-3", id='header'):
                    div(cls="container-fluid py-5")            
                    h1(cls="display-5 fw-bold").add('RID Qualifier Report')
                    p(cls="col-md-12 fs-4").add('Details on tests conducted on a USS Service Provider to assess capability and compliance against Network Remote-ID as specified by ASTM F3411 Remote-ID standard')
                    a(cls="btn btn-primary", href="https://github.com/interuss/dss/tree/master/interfaces/automated-testing/rid").add("Learn More")
                 
                
                heading_table = table(cls='table', id='test_details')
                with heading_table.add(thead()).add(tr()):
                   th(cls="col").add('Service Provider Details')
                   th(cls="col").add('Observer Details')
                    

                evaluation_criteria_test_time_table = table(cls='table', id='evaluation_details')
                with evaluation_criteria_test_time_table.add(thead()).add(tr()):
                   th(cls="col").add('Evaluation Criteria')
                   th(cls="col").add('Test Details')
                    
                with heading_table.add(tbody()):
                    l = tr()
                    with l.add(td()):
                        l_table = table(cls='table table-borderless')
                        for injection_target in injection_targets:
                            base_url = injection_target['injection_base_url']
                            ext = tldextract.extract(base_url)

                            with l_table.add(tr()):
                                with td():
                                    p(cls='text-muted').add('Name')
                                td().add(injection_target['name'])
                            with l_table.add(tr()):
                                with td():
                                    p(cls='text-muted').add('URL')
                                td().add(base_url)
                            with l_table.add(tr()):
                                with td():
                                    p(cls='text-muted').add('DSS Audience')
                                td().add(code(''.join(ext[:2])))
                            
                    with l.add(td()):
                        l_table = table(cls='table table-borderless')
                        for observer in observers:    
                            obs_base_url = observer['observation_base_url']
                            obs_ext = tldextract.extract(obs_base_url)

                            with l_table.add(tr()):
                                with td():
                                    p(cls='text-muted').add('Name')
                                td().add(observer['name'])
                            with l_table.add(tr()):
                                with td():
                                    p(cls='text-muted').add('URL')
                                td().add(obs_base_url)
                            with l_table.add(tr()):
                                with td():
                                    p(cls='text-muted').add('DSS Audience')
                                td().add(code(''.join(obs_ext[:2])))
                        
                with evaluation_criteria_test_time_table.add(tbody()):
                    l = tr()
                    with l.add(td()):
                        l_table = table(cls='table table-borderless')
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Min. Query Diagonal (meters)')
                            td().add(evaluation['min_query_diagonal'])
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Propogation Latency (seconds)')
                            td().add(evaluation['max_propagation_latency'])
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Polling Interval (seconds)')
                            td().add(evaluation['min_polling_interval'])
                        
                    with l.add(td()):
                        l_table = table(cls='table table-borderless')
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Start')
                            td().add(b('2021-05-11 13:23:58'))
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('End')
                            td().add(b('2021-05-11 13:43:50'))
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Locale')
                            td().add(b(report_json['setup']['configuration']['locale']))
                            
                
                with div(cls="pt-4", id='observed_issues'):
                    h2("Observed Issues")
                    p(cls="fs-5 col-md-12 text-muted").add("The list below shows observed issues during the test. Even if there are issues, it may mean that the system is working as designed, it is recommended that an expert review and assess the performance.")
                    br()
                    
                
                issues_table = table(cls='table', id='issues_table')

                
                with issues_table.add(thead()).add(tr()):
                   th(cls="col").add('#')
                   th(cls="col").add('Response Code')
                   th(cls="col").add('Severity')
                   th(cls="col").add('Error Code')
                   th(cls="col").add('Flight ID')
                   th(cls="col").add('Summary')
                    
                with issues_table.add(tbody()):
                    if findings['issues']:
                        
                        for idx, issue in enumerate(findings['issues']):    
                            l = tr()
                            with l:
                                with td():
                                    p(cls='text-muted').add((idx+1))
                                td().add(issue['queries'][0]['response']['code'])
                                td().add(issue['severity'])
                                td().add(issue['test_code'])
                                td().add(issue['subject'])
                                td().add(issue['summary'])
                    else:
                        l = tr()
                        with l:
                            with td():
                                p(cls='text-muted').add("No Issues found in report.json")
                        
                            td().add()
                            td().add()
                            td().add()
                            td().add()
                            td().add()
                        

                with footer(cls="pt-3 mt-4 text-muted border-top"):            
                    p('Report generated on: ' + formatted_now)
                


    with open('output/report.html', 'w') as output:
        output.write(doc.render())
