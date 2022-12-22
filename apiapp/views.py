from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from .models import PostModel
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions, authentication
from .authentication import TokenAuthentication
from access.serializers import UserSerializer
from accounts.models import User
from django.contrib.auth import login, logout
from rest_framework.authtoken.views import Token
import requests



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Using Class based Views ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class PostCreateList(generics.ListCreateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer  
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication]

post_create_list = PostCreateList.as_view()


class PostRetrieveDeleteUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer  
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication]
    
post_retrieve_delete_update = PostRetrieveDeleteUpdate.as_view()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
user_create = UserCreate.as_view()


@api_view(['GET'])
def user_login(request:Request):
    email = request.data['email']
    password = request.data['password']
    
    queryset = get_object_or_404(User, email = email, password = password)
    serializer = UserSerializer(instance = queryset, many = False)
    data = serializer.data
    
    if data:
        login(request, queryset)
        #Generate Token Here
        token = getAuthToken(email, password)
        return Response(data={"message":"Sucessfuly logged in user", "token" :token}, status=status.HTTP_202_ACCEPTED)
        
    return Response(data={"message":"User does not exists"}, status=status.HTTP_404_NOT_FOUND)
  
def getAuthToken(email, password):    
    auth_endpoint = "http://localhost:8000/auth/"
    auth_response = requests.post(auth_endpoint, json={"username":email, "password": password})
    print("Printing...")
    print(auth_response)
    if auth_response.status_code == 200:
        token = auth_response.json()['token']
        return token
    


@api_view(['GET'])
def user_logout(request:Request):
    value = logout(request)
    print("logging out...")
    print(value)    
    return Response(data={"message":"Successfully logged out"}, status=status.HTTP_200_OK)
    
    
    



#~~~~~~~~~~~~~~~~~~~~~~~~~~Using Mixins and GenericAPIView class ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# class PostCreateList(generics.GenericAPIView,
#                      mixins.CreateModelMixin,
#                      mixins.ListModelMixin):
    
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer
    
#     def get(self, response:Response, *args, **kwargs):
#         return self.list(response, *args, **kwargs)
    
#     def post(self, response:Response, *args, **kwargs):
#         return self.create(response, *args, **kwargs)

# post_create_list = PostCreateList.as_view()


# class PostRetrieveDelete(generics.GenericAPIView,
#                          mixins.DestroyModelMixin,
#                          mixins.RetrieveModelMixin):
    
#     queryset = PostModel.objects.all()
#     serializer_class = PostSerializer
    
#     def get(self, response:Response, *args, **kwargs):
#         return self.retrieve(response, *args, **kwargs)
    
#     def delete(self, response:Response, *args, **kwargs):
#         return self.destroy(response, *args, **kwargs)
    
# post_retrieve_delete = PostRetrieveDelete.as_view()

# class PostUpdate(generics.GenericAPIView,
#                  mixins.UpdateModelMixin):
    
#     queryset = PostModel.objects.all()
#     serializer_class =  PostSerializer
    
#     def put(self, response:Response, *args, **kwargs):
#         return self.update(response, *args, **kwargs)

# post_update = PostUpdate.as_view()







#~~~~~~~~~~~~~~~~~~~~~~~~~~`Using Decorators `~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# @api_view(['GET', 'POST'])
# def PostCreateList(request:Request):
#     if request.method == 'GET':        
#         query_set = PostModel.objects.all()
#         postSerializer = PostSerializer(instance = query_set, many = True)
#         data = {
#             "message":"All posts returned" ,
#             "data":postSerializer.data
#         }
#         return Response(data = data, status=status.HTTP_200_OK)
#     data = request.data
#     postSerializer = PostSerializer(data = data)
#     if postSerializer.is_valid():
#         postSerializer.save()
#         data = {
#             "message":"Successfully saved the data",
#             "data":postSerializer.data
#         }
#         return Response(data = data, status=status.HTTP_201_CREATED)
#     return Response(data={"message":"Invalid formation"}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE', 'GET'])
# def PostRetrieveDelete(request:Request, pk:int):
#     if request.method == 'GET':
#         query_set = get_object_or_404(PostModel, pk = pk)
#         postSerializer = PostSerializer(instance = query_set, many = False)
#         data = {
#             "message":"Retrieved a single post",
#             "data":postSerializer.data
#         }
#         return Response(data = data, status=status.HTTP_200_OK)
    
#     query_set = get_object_or_404(PostModel, pk = pk)
#     query_set.delete()
#     data = {
#         "message":"Successfully deleted the specified post"
#     } 
#     return Response(data = data, status = status.HTTP_200_OK)

# @api_view(['PUT'])
# def PostUpdate(request:Request, pk:int):
#     query_set = get_object_or_404(PostModel, pk = pk)
#     data = request.data
#     postSerializer = PostSerializer(instance = query_set, data = data)
#     if postSerializer.is_valid():
#         postSerializer.save()
#         data = {
#             "message":"Successfully deleted the post"
#         }
#         return Response(data = data, status=status.HTTP_200_OK)
#     return Response(data={"message":"Invalid input request"}, status=status.HTTP_400_BAD_REQUEST)
    
        
        
        

