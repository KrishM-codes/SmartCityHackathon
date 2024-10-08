from django.shortcuts import redirect, render
from .models import Query
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .serializers import QuerySerializer,UserSerializer,QuerygetSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
import io
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.contrib.auth import get_user_model
import os
import json
import nltk
import numpy as np
import tensorflow as tf
import random
from django.conf import settings
from django.http import JsonResponse
from nltk.stem.lancaster import LancasterStemmer


# Chatbot ML Model
# Initialize stemmer
stemmer = LancasterStemmer()

# Load the model and intents
model_path = os.path.join(settings.BASE_DIR, 'App/models/model.h5')
intents_path = os.path.join(settings.BASE_DIR, 'App/models/intents.json')

model = tf.keras.models.load_model(model_path)

with open(intents_path, 'r') as file:
    data = json.load(file)

words = []
labels = []

# Prepare data structures
for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

words = sorted(list(set([stemmer.stem(w.lower()) for w in words if w not in "?"])))
labels = sorted(labels)

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for s_word in s_words:
        for i, w in enumerate(words):
            if w == s_word:
                bag[i] = 1

    return np.array(bag)

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user_input = body.get('text', '')

        input_data = np.array([bag_of_words(user_input, words)])
        results = model.predict(input_data)
        results_index = np.argmax(results)
        tag = labels[results_index]

        response = None
        for tg in data['intents']:
            if tg['tag'] == tag:
                response = random.choice(tg['responses'])
                break

        return JsonResponse({"response": response})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

# Create your views here.
def home(request):
    return render(request,'App/home.html')


class UserViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

class GetQuery(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, uid=None, format=None):
        if uid is not None:
            queries = Query.objects.filter(Posted_by_id=uid)
            serializer = QuerygetSerializer(queries,many=True)
            return Response(serializer.data)



# @api_view(['POST','GET','PUT','DELETE'])
class QueryAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,pk=None,format=None):
        uname = request.data.get('uname')
        if uname is not None:
            uid = User.objects.get(username=uname)
            queries = Query.objects.filter(Posted_by_id=uid.id)
            serializer = QuerySerializer(queries,many=True)
        else:
            if pk is not None:
                queries = Query.objects.get(id=pk)
                serializer = QuerySerializer(queries)
            else:
                queries = Query.objects.all()
                serializer = QuerySerializer(queries,many=True)
        return Response(serializer.data)
    
    def post(self,request,format= None):
        data = request.data
        uname = data.get('Posted_by')
        uid = User.objects.get(username = uname).id
        data['Posted_by']=uid
        serializer = QuerySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Query Posted'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk=None,format=None):
        if pk is None:
            id = request.data.get('id')
        else:
            id=pk
        query = Query.objects.get(pk=id)
        serializer = QuerySerializer(query,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Query Updated'})
        return Response(serializer.errors)
    
    def delete(self,request,pk=None,format=None):
        if pk is None:
            id = request.data.get('id')
        else:
            id=pk
        query = Query.objects.get(pk=id)
        query.delete()
        return Response({'msg':'Query Deleted'})


@csrf_exempt
def postQuery(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pydata = JSONParser().parse(stream)
        uname = pydata.get('Posted_by')
        uid = User.objects.get(username = uname).id
        pydata['Posted_by']=uid
        serializer = QuerySerializer(data=pydata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Query Posted'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json')


@login_required(login_url='login')
def dashboard(request):
    userid = request.user.pk
    userdata = User.objects.get(id=userid)
    if request.method == 'POST':
        if request.POST.get('logout'):
            logout(request)
            return redirect('/login')
    context = {'data':userdata}
    return render(request,'App/dashboard.html',context=context)


def loginUser(request):

    if request.method == 'POST':
        uname = request.POST.get('username')
        passwd = request.POST.get('password')

        if not User.objects.filter(username=uname).exists():
            messages.error(request,'Invalid Username')
            return redirect('/login') # '/login/' url redirect
        
        user = authenticate(username=uname,password=passwd)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/dashboard')
        
    return render(request,'App/login.html')

def registerUser(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
         
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/register')
         
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
         
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
         
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/register')
     
    # Render the registration page template (GET request)
    return render(request, 'App/register.html')

# @csrf_exempt
# def queries(request):
#     if request.method=='GET':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pydata = JSONParser().parse(stream)
#         uname = pydata.get('uname',None)

#         if uname is not None:
#             uid = User.objects.get(username=uname)
#             queries = Query.objects.filter(Posted_by_id=uid.id)
#         else:
#             queries = Query.objects.all()
    
#         serializer = QuerySerializer(queries, many=True)
#         json_data = JSONRenderer().render(serializer.data)
#         return HttpResponse(json_data,content_type = 'application/json')

#     if request.method == 'POST':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pydata = JSONParser().parse(stream)
#         uname = pydata.get('Posted_by')
#         uid = User.objects.get(username = uname).id
#         pydata['Posted_by']=uid
#         serializer = QuerySerializer(data=pydata)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg':'Query Posted'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data,content_type='application/json')
        
#         json_data = JSONRenderer().render(serializer.errors)
#         return HttpResponse(json_data,content_type='application/json')
    
#     if request.method == 'PUT':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pydata = JSONParser().parse(stream)
#         id = pydata.get('id')
#         query = Query.objects.get(id=id)
#         serializer=QuerySerializer(query,data=pydata,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             res = {'msg':'Query Updated!'}
#             json_data = JSONRenderer().render(res)
#             return HttpResponse(json_data,content_type='application/json')
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data,content_type='application/json')
        
#     if request.method == 'DELETE':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pydata = JSONParser().parse(stream)
#         id = pydata.get('id')
#         query = Query.objects.get(id=id)
#         query.delete()
#         res = {'msg':'Query Deleted!'}
#         json_data = JSONRenderer().render(res)
#         return HttpResponse(json_data,content_type='application/json')
