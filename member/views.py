from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from .serializers import MemberRegisterSerializer

# Create your views here.

class MemberRegisterView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    # with APIView
    # def post(self, request):
    #     serializer = MemberRegisterSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         print(f'serializer.data > {serializer.data}') # {'username': 'jaehyukpyon3', 'tel': 'jaehyuk.pyon3@gmail.com'}
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    #     # Response({'detail': 'error msg'}, status=xxxx)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer_class = MemberRegisterSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)
