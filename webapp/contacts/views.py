from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from api.get_all_users import get_all_users
from api.User import User
from api.get_user_by_id import get_user_by_id

def index(request):
    return render(request, 'contacts/index.html', {'users':get_all_users()})

def add_contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")

        user = User(first_name, last_name, phone_number, address)
        user.save()

        return redirect('index')

    else:
        raise Http404

def delete_contact(request):
    if request.method == "POST":
        user_id = request.POST.get("id")
        user = get_user_by_id(user_id)
        user.delete()
        return redirect('index')
    else:
        raise Http404


def update_contact(request):
    if request.method == "POST":
        user_id = request.POST.get('id')
        user = get_user_by_id(user_id)
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        user.update(phone_number, address)
        return redirect('index')
    else:
        raise Http404