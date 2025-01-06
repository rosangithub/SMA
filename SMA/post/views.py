from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from itertools import chain
import random


from .models import UserProfile ,Post,LikePost,FollowerCount

# Get the custom username model (if you're using a custom user model)
username = get_user_model()

# Index view
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowerCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = UserProfile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

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


    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user_object)


    username_profile_list = []
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = UserProfile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
        print(f"Final Profile List: {username_profile_list}")

    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id=request.GET.get('post_id')
    post=Post.objects.get(id=post_id)
    like_filter=LikePost.objects.filter(post_id=post_id,username=username).first()
    if like_filter==None:
        new_like=LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')




@login_required(login_url="signin")
def settings(request):
    user_profile=UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image')==None:
            email=request.POST['email']
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

@login_required(login_url='signin')
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile, created = UserProfile.objects.get_or_create(user=user_object)
    # user_profile = UserProfile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower=request.user.username
    user=pk
    if FollowerCount.objects.filter(follower=follower,user=user).first():
        button_text='Unfollow'
    else:
        button_text='Follow'
    user_followers=len(FollowerCount.objects.filter(user=pk))
    user_following=len(FollowerCount.objects.filter(follower=pk))

    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'user_follower':user_followers,
        'user_following':user_following
    }
  
    return render(request,'profile.html',context)
@login_required(login_url='signin')
def follow(request):
    if request.method=="POST":
        follower=request.POST['follower']
        user=request.POST['user']

        if FollowerCount.objects.filter(follower=follower,user=user).first():
            delete_follower=FollowerCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower=FollowerCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
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


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user_object)

    # Initialize the username_profile_list to avoid UnboundLocalError
    username_profile_list = []

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            # Corrected the field name to user_id
            profile_lists = UserProfile.objects.filter(user_id=ids)
            # Use extend instead of append to avoid nested lists
            username_profile_list.extend(profile_lists)

        # No need for list(chain(*username_profile_list)) since extend was used
        print(f"Final Profile List: {username_profile_list}")

    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowerCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    # Ensure we are excluding followed users and the current user
    new_suggestions_list = [x for x in all_users if x not in user_following_all and x != request.user]
    random.shuffle(new_suggestions_list)

    username_profile_list = []

    for users in new_suggestions_list:
        # Update this to use the correct field for filtering the profile
        profile_lists =UserProfile.objects.filter(user=users)
        username_profile_list.append(profile_lists)

    # Flatten the list of profiles
    suggestions_username_profile_list = list(chain(*username_profile_list))

    # Debugging: Check if suggestions list is being populated
    print(f"Suggestions List: {suggestions_username_profile_list[:4]}")

    return render(request, 'index.html', {
        'user_profile': user_profile,
        'posts': feed_list,
        'suggestions_username_profile_list': suggestions_username_profile_list[:4]
    })
