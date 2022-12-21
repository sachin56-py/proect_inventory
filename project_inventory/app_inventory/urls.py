from django.urls import path
from . import views
from .views import ItemApiView

urlpatterns = [
    # items
    path("items/", views.item_index, name="items.index"),
    path("items/show/<int:id>/", views.item_show, name="items.show"),
    path("items/create/", views.item_create, name="items.create"),
    path("items/edit/<int:id>/", views.item_edit, name="items.edit"),
    path("items/delete/<int:id>/", views.item_delete, name="items.delete"),
    path("items/update/", views.item_update, name="items.update"),

    # users
    path("users/login/", views.user_login, name="users.login"),
    path("users/register/", views.user_register, name="users.register"),
    path("users/logout/", views.user_logout, name="users.logout"),

    # API
    path("api/items/", ItemApiView.as_view(), name="api.items.list"),
]
