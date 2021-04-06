from django.shortcuts import render
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,ListAPIView,GenericAPIView
from rest_framework import status
from .serializers import *
from rest_framework.response import Response
from io import BytesIO
from barcode.writer import SVGWriter,ImageWriter    
import barcode
# Create your views here.

class SpareView(ListAPIView):
    serializer_class = SpareSerializer

    def get_queryset(self):
        return Spare.objects.all()

class SpareEach(ListAPIView):
    serializer_class = SpareSerializer
    lookup_url_kwarg = "transno"

    def get_queryset(self):
        transno = self.kwargs.get(self.lookup_url_kwarg)
        print(transno)
        return Spare.objects.filter(transNo=transno)


class SpareUpdate(GenericAPIView):
    serializer_class = SpareUpdateSerializer
    lookup_url_kwarg = "transno"

    def put(self,request,transno):
        transno = self.kwargs.get(self.lookup_url_kwarg)
        alltrans = Spare.objects.filter(transNo=transno)
        for eachtrans in alltrans:
            eachtrans.status='deleted'
            eachtrans.save()
        if alltrans:
            Spareprint.objects.create(transno=transno)
            
        return Response(status=status.HTTP_200_OK,data={"msg":"Successfully Updated"})


def PrintView(request):
    allRequested = Spare.objects.filter(transNo=1)

    # from barcode import EAN13
    # from barcode.writer import ImageWriter

    # with open('static/barcode/1.png', 'wb') as f:
    #    EAN13('123456789102', writer=ImageWriter()).write(f)

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
    return render(request,'printout.html',{'data':fullC,'transno':'120000200','svg':svg.decode('utf-8')})
