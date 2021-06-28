import json
import dominate
from dominate.tags import *
from pathlib import Path
import pathlib
import os, sys
import arrow
import argparse

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f','--file', dest='file',
                    help='sum the integers (default: find the max)')
    args = parser.parse_args()
    cur_dir = pathlib.Path(__file__).parent.absolute()
    os.chdir(cur_dir)
    file = args.file
    try: 
        assert os.path.isfile(file)
    except AssertionError as ae: 
        sys.exit(0)
        
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
                    button(cls="btn btn-primary").add("Learn More")
                 
                
                heading_table = table(cls='table', id='test_details')
                with heading_table.add(thead()).add(tr()):
                   th(cls="col").add('Service Provider Details')
                   th(cls="col").add('Observer Details')
                    

                evaluation_criteria_test_time_table = table(cls='table', id='evaluation_details')
                with evaluation_criteria_test_time_table.add(thead()).add(tr()):
                   th(cls="col").add('Evaluation Criteria')
                   th(cls="col").add('Test Time')
                    
                with heading_table.add(tbody()):
                    l = tr()
                    with l.add(td()):
                        l_table = table(cls='table')
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Name')
                            td().add(b('USS1'))
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('URL')
                            td().add(b('http://uss1.com'))
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('DSS Audience')
                            td().add(b('sp.uss1.com'))
                        
                    with l.add(td()):
                        l_table = table(cls='table')
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Name')
                            td().add(b('DP1'))
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('URL')
                            td().add(b('https://dp1.com'))
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('DSS Audience')
                            td().add(b('dp.dp1.com'))
                    
                with evaluation_criteria_test_time_table.add(tbody()):
                    l = tr()
                    with l.add(td()):
                        l_table = table(cls='table')
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Min. Query Diagonal')
                            td().add(b('100 mts.'))
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Propogation Latency')
                            td().add(b('10 secs'))
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Polling Interval')
                            td().add(b('5 secs'))
                        
                    with l.add(td()):
                        l_table = table(cls='table')
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('Start')
                            td().add(b('2021-05-11 13:23:58'))
                        with l_table.add(tr()):
                            with td():
                                p(cls='text-muted').add('End')
                            td().add(b('2021-05-11 13:43:50'))
                            
                
                with div(cls="mb-4", id='observed_issues'):
                    h2("Observed Issues")
                    p(cls="fs-5 col-md-12").add("Quickly and easily get started with Bootstrap's compiled, production-ready files with this barebones example featuring some basic HTML and helpful links. Download all our examples to get started.")
                    
                    
                with footer(cls="pt-3 mt-4 text-muted border-top"):            
                    p('Report generated on: ' + formatted_now)


    with open('output/report.html', 'w') as output:
        output.write(doc.render())
