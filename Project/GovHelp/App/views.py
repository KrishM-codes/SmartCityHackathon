from django.shortcuts import redirect, render
from .models import Query
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .serializers import QuerySerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
import io
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    return render(request,'App/home.html')

@csrf_exempt
def queries(request):
    if request.method=='GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pydata = JSONParser().parse(stream)
        uname = pydata.get('uname',None)

        if uname is not None:
            uid = User.objects.get(username=uname)
            queries = Query.objects.filter(Posted_by_id=uid.id)
        else:
            queries = Query.objects.all()
    
        serializer = QuerySerializer(queries, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data,content_type = 'application/json')

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
    
    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pydata = JSONParser().parse(stream)
        id = pydata.get('id')
        query = Query.objects.get(id=id)
        serializer=QuerySerializer(query,data=pydata,partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Query Updated!'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data,content_type='application/json')
        
    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pydata = JSONParser().parse(stream)
        id = pydata.get('id')
        query = Query.objects.get(id=id)
        query.delete()
        res = {'msg':'Query Deleted!'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data,content_type='application/json')

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