from django.shortcuts import render
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,ListAPIView,GenericAPIView
from rest_framework import status
from .serializers import *
from rest_framework.response import Response
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
            eachtrans.status='printing'
            eachtrans.save()
        return Response(status=status.HTTP_200_OK,data={"msg":"Successfully Updated"})