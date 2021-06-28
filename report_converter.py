import json
import dominate
from dominate.tags import *
from pathlib import Path
import pathlib
import arrow
import argparse

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--file', dest='file',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
    p = pathlib.Path(__file__).parent.absolute()
    os.chdir(p)

    formatted_now = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')

    self.output_directory = Path('output', self.country_code)    
    self.output_directory.mkdir(parents=True, exist_ok=True)

    self.input_directory = Path('input', self.country_code)    
    self.inpuut_directory.mkdir(parents=True, exist_ok=True)


    doc = dominate.document(title='RID Qualifier Report')
    with doc.head:
        link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css')
        script(type='text/javascript', src='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js')

    with doc:
        with main():
            with div(cls="container py-4"):
                
                with div(cls="p-5 mb-4 bg-light rounded-3", id='header'):
                    div(cls="container-fluid py-5")            
                    h1(cls="display-5 fw-bold").add('RID Qualifier Report')
                    p(cls="col-md-8 fs-4").add('Details on tests conducted on a USS Service Provider to assess capability and compliance against Network Remote-ID as specified by ASTM F3411 Remote-ID standard')
                    
                with footer(cls="pt-3 mt-4 text-muted border-top"):            
                    p('Report generated on: ' + formatted_now)

    
    with open('report.html', 'w') as output:
        output.write(doc.render())
