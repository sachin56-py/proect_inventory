from django.shortcuts import render, redirect
from .forms import ItemCreateForm, UserLoginForm, UserRegisterForm
from .models import Item, AppUser
from datetime import datetime
from django.core.mail import send_mail

# api packages
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from .serializers import ItemSerializer, AppUserSerializer

# creating your views here
# API via class based view
class ItemApiView(APIView):
    def get(self, request):
        item_list = Item.objects.all()
        serializer = ItemSerializer(item_list, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        # one method
        data_post = {
            "title": request.POST.get("title"),
            "particular": request.POST.get("particular"),
            "lf": request.POST.get("lf"),
            "price": request.POST.get("price"), 
            "quantity": request.POST.get("quantity"), 
            "total": request.POST.get("total"),
            "user": 2,
            "added_at": datetime.now()
        }
        # another method
        # data_post = request.POST
        serializer = ItemSerializer(data=data_post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemIdApiView(APIView):

    # to get model object by id
    def get_object(self, id):
        try:
            data=Item.objects.get(id=id)
            return data
        except Item.DoesNotExist:
            return None

    # data edit and show via API by id
    def get(self, request, id):
        item_instance = self.get_object(id)

        if not item_instance:
            return Response({"error": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # data update from API
    def put(self, request, id):
        item_instance = self.get_object(id)

        if not item_instance:
            return Response({"error": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        data_put = {
            "title": request.POST.get("title"),
            "particular": request.POST.get("particular"),
            "lf": request.POST.get("lf"),
            "price": request.POST.get("price"), 
            "quantity": request.POST.get("quantity"), 
            "total": request.POST.get("total"),
            "user": 1,
            "added_at": datetime.now()
        }
        serializer = ItemSerializer(item_instance, data = data_put, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        item_instance = self.get_object(id)
        if not item_instance:
            return Response({"error": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)

        item_instance.delete()  # built in function to delete data items
        return Response({"msg": "Item Deleted Successfully!!"}, status=status.HTTP_200_OK)

# Create your views here.
def item_index(request):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    item_list = Item.objects.all()
    context = {"item_list": item_list}
    return render(request, "items/index.html", context)

def item_show(request, id):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    data = Item.objects.get(id=id)
    context = {"data": data}
    return render(request, "items/show.html", context)

def item_edit(request, id):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    data = Item.objects.get(id=id)
    context = {"data": data}
    return render(request, "items/edit.html", context)

def item_update(request):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    if request.method == "POST":
        item = Item.objects.get(id=request.POST.get("id")) # pretty beautful code
        user = AppUser.objects.get(id=1)
        item.title = request.POST.get("title")
        item.particular = request.POST.get("particular")
        item.lf = request.POST.get("lf")
        item.price = request.POST.get("price")
        item.quantity = request.POST.get("quantity")
        item.total = request.POST.get("total")
        item.added_at = datetime.now()
        item.user = user 
        item.save()
    return redirect("items.index")

def item_delete(request, id):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    data = Item.objects.get(id=id)
    data.delete()
    return redirect("items.index")

def item_create(request):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    form = ItemCreateForm()
    context = {"form": form}     
    if request.method == "POST":
        item = Item()
        user = AppUser.objects.get(id=1)    # could not understand this code why 1?
        item.title = request.POST.get("title")
        item.particular = request.POST.get("particular")
        item.lf = request.POST.get("lf")
        item.price = request.POST.get("price")
        item.quantity = request.POST.get("quantity")
        item.total = request.POST.get("total")
        item.added_at = datetime.now()
        item.user = user 
        item.save()
        context.setdefault("msg", "Item created successfully!!")
    return render(request, "items/create.html", context)

def user_login(request):
    form = UserLoginForm()
    context = {"form": form}
    if request.method=="POST":
        req_email = request.POST.get("email")
        req_password = request.POST.get("password")
        user = AppUser.objects.get(email=req_email)
        if user.email==req_email and user.password==req_password:
            request.session["session_email"] = user.email
            
            # this code can also be written as
            # 2) -> request.session.setdefault("session_email", user.email)
            # 3) -> request.session.update({"session_email": user.email})
            return redirect("items.index")
        else:
            return redirect("users.login")
    return render(request, "users/login.html", context)

def user_logout(request):
    if not request.session.has_key("session_email"):
        return redirect("users.login")
    del request.session["session_email"]
    return redirect("users.login")

def user_register(request):

    form = UserRegisterForm()
    context = {"form": form}
    if request.method == "POST":
        user = AppUser()
        # another method to post object data
        user.full_name = request.POST["full_name"]
        user.email = request.POST["email"]
        user.contact = request.POST["contact"]
        user.password = request.POST["password"]
        user.save()
        context.setdefault("msg", "Account registered successfully!!")
        send_mail(
            "Account creation!!", # subject
            "Hello "+ user.full_name+"!! Your account has been created successfully.", # message
            "sachinmnm11@gmail.com", # sender
            [user.email] # receiver       
        )

    return render(request, "users/register.html", context)
