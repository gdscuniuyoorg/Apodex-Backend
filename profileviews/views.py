from .models import User
from django.urls import reverse
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import YourProfileModel  # Replace with the actual name of your profile model


# Create your views here.

def index(request):
    return render(request, "apodex/index.html")

def login_view(request):
    return

def logout_view(request):
    return


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email =request.POST["email"]

        # Password matching
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "apodex/register.html", {
                "message" : "Passwords must match"
            })

        # Create a new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "apodex/register.html", {
                "message": "Username already taken"
            })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "apodex/register.html")

def getprofile(request, user_id):
    """ View: Shows requested user profile """

    user_data = get_object_or_404(User, pk=user_id)
    
    # Additional logic for fetching about and image fields
    about = user_data.profile.about  # Assuming you have a related profile model
    image = user_data.profile.image  # Assuming you have a related profile model

    # Create page control
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "apodex/user_profile.html", {
        "user_data": user_data,
        "about": about,
        "image": image,
        "page_obj": page_obj,
    })

def getprofiles(request):
    """ View: Shows all profiles on the site """

    profiles = YourProfileModel.objects.all()  # Replace with your actual model name

    # Create page control
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "apodex/all_profiles.html", {
        "profiles": profiles,
        "page_obj": page_obj,
    })
