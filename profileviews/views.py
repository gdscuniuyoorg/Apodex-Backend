# from .models import User
from django.urls import reverse
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render
from user_app.models import UserProfile  


# Create your views here.
def getprofile(request, user_id):
    """ View: Shows requested user profile """

    user_data = get_object_or_404(UserProfile, pk=user_id)
    
    # Additional logic for fetching about and image fields
    about = user_data.profile.about  # Assuming you have a related profile model
    image = user_data.profile.image  # Assuming you have a related profile model

    # Create page control
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "profileviews/user_profile.html", {
        "user_data": user_data,
        "about": about,
        "image": image,
        "page_obj": page_obj,
    })

def getprofiles(request):
    """ View: Shows all profiles on the site """

    profiles = UserProfile.objects.all()  # Replace with your actual model name

    # Create page control
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "profileviews/profiles.html", {
        "profiles": profiles,
        "page_obj": page_obj,
    })
