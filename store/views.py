from django.shortcuts import render,redirect
from .models import Product,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,changePasswordForm
from django import forms
from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = changePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated. Please log in again!")
                return redirect('login')  # Redirect to login page after updating the password
            else:
                # Display all form errors without redirecting
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
                
                # Re-render the form with errors
                return render(request, 'update_password.html', {'form': form})
        else:
            form = changePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('home')  # Redirect to the home page if not authenticated

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if request.method == 'POST':
            if user_form.is_valid():
                user_form.save()
                # No need to re-login the user unless the password or session needs updating
                messages.success(request, "Your profile has been updated successfully!")
                return redirect('home')
            else:
                # Handle form errors
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        
        # Render form with or without POST data
        return render(request, 'update_user.html', {'user_form': user_form})
    
    else:
        messages.error(request, "You must be logged in to access this page!")
        return redirect('home')

# def update_user(request):
#     if request.user.is_authenticated:
#         current_user = User.objects.get(id=request.user.id)
#         user_from = UpdateUserForm(request.POST or None, instance=current_user)

#         if user_from.is_valid():
#             user_from.save()
#             login(request,current_user)
#             messages.success(request, "User Has been Update!!!")
#             return redirect('home')
#         return render(request, 'update_user.html',{'user_from':user_from})
#     else:
#         messages.success(request, "You Must be Logged in to access that page!!!")
#         return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def category_summary(request):
    categories = Category.objects.all() 
    return render(request,'category_summary.html',{"categories":categories})

def category(request,foo):
    # Replace Hyphens with space
    foo = foo.replace('-','')
    # Grap the catagory from the url
    try:
        #look Up The Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category })
    
    except:
        messages.success(request,("That Category Doest't exit....!"))
        return redirect('home')

def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,("you have been logged in !"))
            return redirect('home')
        else:
            messages.success(request,("there was an error, please try again !"))
            return redirect('login')
    else:
        
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("you have been logged out... Thanks"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You have successfully registered! Welcome!"))
            return redirect('home')
        else:
            messages.success(request, ("Whoops! there was a problem registering ,Please try again!"))
            return redirect('register')

    return render(request,'register.html',{'form':form})
