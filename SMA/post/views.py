from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from .models import UserProfile ,Post

# Get the custom username model (if you're using a custom user model)
username = get_user_model()

# Index view
@login_required(login_url='signin')
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=UserProfile.objects.get(user=user_object)
    return render(request, 'index.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method=='POST':
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']
        new_post=Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    return HttpResponse('<h1> Upload View</h1>')
@login_required(login_url="signin")
def settings(request):
    user_profile=UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image')==None:
            email=user_profile.POST['email']
            image=user_profile.profileimg
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.email=email
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        if request.FILES.get('image') !=None:
            image=request.FILES.get('image')
            email=request.POST['email']
            bio=request.POST['bio']
            location=request.POST['location']
            
            user_profile.profileimg=image
            user_profile.email=email
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()

        return redirect('settings')
        
    return render(request,'setting.html' ,{'user_profile':user_profile})

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        # Validate email format (basic check)
        if not email or '@' not in email:
            messages.error(request, 'Please provide a valid email address')
            return redirect('signup')

        # Check if email already exists in the User model
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect('signup')

        # Check if username already exists in the User model
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('signup')

        # Check password strength (basic check)
        if len(password) <3:
            messages.error(request, 'Password must be at least 3 characters long')
            return redirect('signup')

        # Create new user if everything is valid
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Create a profile object for the new user
            new_profile = UserProfile.objects.create(user=user)  # No need to pass email again
            new_profile.save()

            # Automatically log the user in after successful signup
            login(request, user)

            messages.success(request, "Sign-up successful! You are now logged in.")
            return redirect('settings')  # Redirect to a user dashboard or home page

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('signup')

    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('signin')

    return render(request, 'signin.html')

# Logout view
def logout(request):
    auth_logout(request)
    return redirect('signin')
