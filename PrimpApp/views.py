from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.db.models import Q
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import NewUserForm, SignInForm, UserProfileForm
from .models import Profile
from django.contrib.auth.models import User
from json import loads
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

# Create your views here.


def log_out(request):
    logout(request)
    return redirect("index")

def index(request):
    if request.method == "POST":
            newuser = NewUserForm(request.POST)
            if newuser.is_valid():
                logInUser = User.objects.create_user( username = request.POST['username'],
                                                    password=request.POST['password'],
                                                    first_name = request.POST['first_name'],
                                                    last_name = request.POST['last_name'],
                                                    email = request.POST['email'],
                                                    )
                login(request, logInUser)
                return redirect("profile")
            else:
                context = {
                "errors": newuser.errors,
                "form": NewUserForm(),
                }
                return render (request, 'PrimpApp/index.html', context)
    else:
        context = {
        "form": NewUserForm()
        }
        return render(request, 'PrimpApp/index.html',context)



def log_in(request):
    if request.method == "POST":
        logInUser = authenticate(username=request.POST['username'], password=request.POST["password"])
        if logInUser is not None:
            login(request, logInUser)
            return redirect("home")
        else:
            messages.error(request, "Wrong username or password")
            return redirect("log_in")
    context = {
        "form": SignInForm()
    }
    return render(request, "PrimpApp/log_in.html", context)

def home(request):
    Stylist = Profile.objects.filter(is_stylist=True)
    Stylist_serialized = serializers.serialize('json',Stylist)
    currentUser = request.user.profile
    context = {'Stylist': Stylist,
                'stylists': Stylist_serialized,
                'currentUser': currentUser}
    return render(request, "PrimpApp/home.html", context)

def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            tempImageFile = request.FILES
            if not tempImageFile:
                tempImageFile = ''
            else:
                tempImageFile = tempImageFile['Profile_Picture']
            userprofile = Profile(DateOfBirth=request.POST['DateOfBirth'], Profile_Picture = tempImageFile, user=request.user)
            userprofile.save()
        return redirect("home")

    else:
        context = {
            'form': UserProfileForm()
        }
    return render(request, "PrimpApp/profile.html", context)


def edit_profile(request):
    try: ProfileInstance = request.user.profile
    except Profile.DoesNotExist:
        ProfileInstance = Profile(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=ProfileInstance)
        if form.is_valid():
            tempImageFiles = request.FILES
            if not tempImageFiles:
                tempImageFiles = ''
            else:
                tempImageFiles = tempImageFiles['Profile_Picture']

            profile_form = Profile(Profile_Picture = tempImageFiles,
                                    DateOfBirth = request.POST['DateOfBirth'],
                                    user = request.user,
                                    is_stylist = request.POST['is_stylist'],
                                    latitude = request.POST['latitude'],
                                    longitude = request.POST['longitude'],
                                    TypeofStylist = request.POST['TypeofStylist'])
            profile_form.save()
        return redirect('home')

    else:
        context = {
            'ProfileInstance': request.user.profile,
                'form': UserProfileForm(instance=ProfileInstance)
            }
    return render(request, "PrimpApp/edit_profile.html",context)


def update_location(request):

#     if request.method == "GET":
#         loggedInUser = Profile(user_id = request.user.id)
#         if loggedInUser:
#             location = {
#                  'latitude' : loggedInUser.latitude,
#                  'longitude' : loggedInUser.longitude
#             }
#             return JsonResponse(location, safe=False)

    requestedPageInfo = loads(request.body)

    if request.method == "PUT":
        userLocation = Profile(user_id=request.user.id)
        if userLocation:
            userLocation.latitude = requestedPageInfo['latitude']
            userLocation.longitude = requestedPageInfo['longitude']
            userLocation.save()
            return HttpResponse(userLocation)
        else:
            return HttpResponse("TEST")

    return HttpResponse("Hey")

def primper(request, primpID):
    thisInstance = Profile.objects.get(user_id=primpID)
    context = {
        "thisInstance": thisInstance}
    return render(request, "PrimpApp/primper.html", context)
