from .models import *
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML,CSS
from io import BytesIO
from barcode.writer import SVGWriter
import barcode



import os

dirname = 'D:/'

def generatePDF(Spare,Part,transno):
    tobeprinted = Spare.objects.filter(transNo=transno).count()
    if tobeprinted > 0:
        fullyGeneratePdf(Spare,Part,transno)
    return


def fullyGeneratePdf(Spare,Part,transno):
    allRequested = Spare.objects.filter(transNo=transno)
    fullC = []
    for eachReq in allRequested:
        qty = eachReq.qty
        spare = eachReq.spare
        partname = eachReq.partname
        realpartname = Part.objects.get(id=partname).partname
        context = {
            'qty':qty,
            'spare':spare,
            'partname':realpartname,
        }
        fullC.append(context)

    rv = BytesIO()
    code = barcode.get('code128', '10299332233', writer=SVGWriter())
    code.write(rv)

    rv.seek(0)
    # get rid of the first bit of boilerplate
    rv.readline()
    rv.readline()
    rv.readline()
    rv.readline()
    # read the svg tag into a string
    svg = rv.read()
    
    genPdf(fullC,transno,svg)
        
    
    return


def genPdf(context,transno,svg):
    html = render_to_string('printout.html',{'data':context,'transno':'12030390','svg':svg.decode('utf-8')})


    css = CSS(string='''  
    body { font-family: Courier }
        body{
        margin:10px;
        font-family: Courier;
    }
    .text-center{
        text-align: center;
        align-content: center;
    }
    .mt-5,.my-5{
        margin-top: 3rem !important;
    }
    .mb-5,
    .my-5 {
    margin-bottom: 3rem !important;
    }
  
    .mt-10{
        margin-top: 4.5rem !important;
    }

    .my-3{
    margin-bottom: 1rem !important;
    margin-top: 1rem !important;
    }
    .text-uppercase{
        text-transform:uppercase
    }

    .t45{
        width:45%
    }
    .t10{
        width:10%
    }
    th,td{
    word-break: break-all;
    border-top: 1px solid black
    }
    tr{
        text-align:left
    }

    table{
        border-bottom: 1px solid black;
        width:100%
    }

    .px-2 {
    padding-right: 0.5rem !important;
    padding-left: 0.5rem !important;
    }

    .py-2,td,th {
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    }
    @page{
        margin:0px;
        width:80mm;
    }
    ''',)

    pdf = HTML(string=html).write_pdf(stylesheets=[css])

    if os.path.exists(dirname):

        f = open(os.path.join(dirname, transno+'.pdf'), 'wb')
        f.write(pdf) 
        

        os.startfile(dirname+transno+'.pdf',"print")
        

    return HttpResponse({'msg':'success'})