from .models import *
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML

import os

dirname = '/home/bscit/Dev/printbuild/printbuild/pdfs'

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
    
    genPdf(fullC,transno)
        
    
    return


def genPdf(context,transno):
    html = render_to_string('printout.html',{'data':context})

    pdf = HTML(string=html).write_pdf()

    if os.path.exists(dirname):

        f = open(os.path.join(dirname, transno+'.pdf'), 'wb')
        f.write(pdf) 
        

    return HttpResponse({'msg':'success'})