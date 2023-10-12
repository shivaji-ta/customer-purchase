from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customer.serializers import CustomerSerializer, User
from rest_framework import generics


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer


class CustomerRetriveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer


# class CustomerView(APIView):
#     def get_object(self,id):
#         try:
#             obj = User.objects.get(pk=id)
#         except:
#             obj = None
#         return obj
#     def get(self,request):
#         customers = User.objects.all()
#         serializer = CustomerSerializer(customers,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)

#     def post(self,request):
#         serializer = CustomerSerializer(data=request.POST)
#         if serializer.is_valid(raise_exception=True):
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
    
#     def put(self, request,id):
#         user = self.get_object(id)
#         if user:
#             serializer = CustomerSerializer(user,data=request.POST)
#         else:
#             return Response({'error':'User not found'},status=status.HTTP_404_NOT_FOUND)
        

    