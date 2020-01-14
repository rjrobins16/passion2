from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.db.models import Q
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import NewUserForm, SignInForm, AllUsersForm, AllUsersForm2
from .models import AllUser
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
    #sends current logged in user to page
    currentUserlat = request.user.alluser.lat
    currentUserlng= request.user.alluser.lng
    #sends all stylist to page
    Stylist = AllUser.objects.filter(AccountType='P')
    Stylist_serialized = serializers.serialize('json', Stylist)
    context = {
        'Stylist':Stylist,
        'stylists': Stylist_serialized,
        'currentUserlat': currentUserlat,
        'currentUserlng': currentUserlng}
    return render(request, "PrimpApp/home.html", context)

def filter_stylist(request):
    currentUser = request.user.alluser
    usercoords = {currentUser.lat, currentUser.lng}




def profile(request):

    if request.method == "POST":
        form = AllUsersForm2(request.POST)
        if form.is_valid():
            tempImageFile = request.FILES
            if not tempImageFile:
                tempImageFile = ''
            else:
                tempImageFile = tempImageFile['Profile_Picture']
            userprofile = AllUser(user=request.user,
                                  AccountType = request.POST['AccountType'],
                                  DateOfBirth=request.POST['DateOfBirth'],
                                  Profile_Picture = tempImageFile,
                                  address=request.POST['address'],
                                  city = request.POST['city'],
                                  state = request.POST['state'],
                                  zip = request.POST['zip'],

              )
            userprofile.save()
        return redirect("home")

    else:
        context = {
            'form': AllUsersForm2()
        }
    return render(request, "PrimpApp/profile.html", context)


def edit_profile(request):
    try: ProfileInstance = request.user.alluser
    except AllUser.DoesNotExist:
        ProfileInstance = AllUser(user=request.user)

    if request.method == "POST":
        form = AllUsersForm(request.POST, request.FILES, instance=ProfileInstance)
        if form.is_valid():
            tempImageFiles = request.FILES
            if not tempImageFiles:
                tempImageFiles = ''
            else:
                tempImageFiles = tempImageFiles['Profile_Picture']

            profile_form = AllUser(Profile_Picture = tempImageFiles,
                                    AccountType = request.user.alluser.AccountType,
                                    TypeofStylist=request.user.alluser.TypeofStylist,
                                    BusinessName = request.user.alluser.BusinessName,
                                    lat = request.user.alluser.lat,
                                    lng = request.user.alluser.lng,
                                    DateOfBirth = request.POST['DateOfBirth'],
                                    address = request.POST['address'],
                                    city = request.POST['city'],
                                    state = request.POST['state'],
                                    zip = request.POST['zip'],
                                    user = request.user)
            profile_form.save()
        return redirect('home')

    else:
        context = {
            'ProfileInstance': request.user.alluser,
                'form': AllUsersForm(instance=ProfileInstance)
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
        userLocation = AllUser(user_id=request.user.id)
        if userLocation:
            userLocation.lat = requestedPageInfo['lat']
            userLocation.lng = requestedPageInfo['lng']
            userLocation.save()
            return HttpResponse(userLocation)
        else:
            return HttpResponse("TEST")

    return HttpResponse("Hey")

def primper(request, primpID):
    thisInstance = StylistProfile.objects.get(user_id=primpID)
    context = {
        "thisInstance": thisInstance}
    return render(request, "PrimpApp/primper.html", context)
