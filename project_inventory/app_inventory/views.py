from django.shortcuts import render, redirect
from .forms import ItemCreateForm, UserLoginForm, UserRegisterForm
from .models import Item, AppUser
from datetime import datetime

# Create your views here.
def item_index(request):
    item_list = Item.objects.all()
    context = {"item_list": item_list}
    return render(request, "items/index.html", context)

def item_show(request, id):
    data = Item.objects.get(id=id)
    context = {"data": data}
    return render(request, "items/show.html", context)

def item_edit(request, id):
    data = Item.objects.get(id=id)
    context = {"data": data}
    return render(request, "items/edit.html", context)

def item_update(request):
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
    data = Item.objects.get(id=id)
    data.delete()
    return redirect("items.index")


def item_create(request):
    form = ItemCreateForm()
    context = {"form": form}     # could not understand this code
    if request.method == "POST":
        item = Item()
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
        context.setdefault("msg", "Item created successfully!!")
    return render(request, "items/create.html", context)

def user_login(request):
    form = UserLoginForm()
    context = {"form": form}
    return render(request, "users/login.html", context)

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

    return render(request, "users/register.html", context)