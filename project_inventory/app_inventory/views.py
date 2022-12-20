from django.shortcuts import render, redirect
from .forms import ItemCreateForm, UserLoginForm, UserRegisterForm
from .models import Item, AppUser
from datetime import datetime
from django.core.mail import send_mail

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