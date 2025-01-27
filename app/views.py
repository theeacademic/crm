from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from .models import Client
from .forms import ClientForm, SearchForm, UserRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Housemaid
from .forms import HousemaidForm
from .models import Housemaid, NextOfKin



@xframe_options_exempt
def user_login(request):
    # Your login view logic
    return render(request, 'templates/login.html', {'form': AuthenticationForm()})

# User Registration View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user
            return redirect('home')  # Redirect to the home or login page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  # Bind POST data to the form
        if form.is_valid():  # Check if the form data is valid
            form.save()  # Save the new user to the database
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')  # Redirect the user to the login page
        else:
            messages.error(request, "There were errors in your form. Please fix them.")
    else:
        form = UserRegistrationForm()  # Display an empty form for a GET request

    return render(request, 'signup.html', {'form': form})  # Render the signup page


# User Login View with Debugging
def user_login(request):
    if request.method == 'POST':
        print("Request method: POST")  # Debugging request method
        form = AuthenticationForm(data=request.POST)
        print("Form is valid:", form.is_valid())  # Debugging form validation status
        
        if form.is_valid():
            # Debugging cleaned data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print("Username:", username)
            print("Password:", password)
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            print("Authenticated user:", user)  # Debugging authentication result
            
            if user is not None:
                login(request, user)
                print("Login successful. Redirecting to 'add_customer'.")  # Debugging successful login
                # Redirect to a specific page after successful login
                return redirect('add_customer')  # Change this to the page you want to redirect to
            else:
                print("Authentication failed. Invalid username or password.")  # Debugging failed authentication
                messages.error(request, "Invalid username or password.")
        else:
            print("Form is invalid. Please check the fields.")  # Debugging invalid form
            messages.error(request, "Please fill in all fields correctly.")
    else:
        print("Request method: GET")  # Debugging request method
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

# List of Clients
@login_required
def client_list(request):
    clients = Client.objects.all()
    search_form = SearchForm(request.GET)
    if search_form.is_valid() and search_form.cleaned_data['query']:
        query = search_form.cleaned_data['query']
        clients = clients.filter(first_name__icontains=query) | clients.filter(last_name__icontains=query)
    return render(request, 'crm_app/client_list.html', {'clients': clients, 'search_form': search_form})

# Create a New Client
@login_required
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Client added successfully.")
            return redirect('saved_list')
    else:
        form = ClientForm()
    return render(request, 'crm_app/add_customer.html', {'form': form})

# Home Page View
def home(request):
    return render(request, 'login.html')

# API Action Example
def zyb_tracker_statistics_action(request):
    return JsonResponse({"message": "Action executed"})

def add_customer(request, client_id=None):
    if client_id:
        # If an ID is provided, fetch the client from the database
        client = get_object_or_404(Client, id=client_id)
        form = ClientForm(instance=client)  # Pre-fill the form with the client's details
    else:
        form = ClientForm()  # Empty form for a new customer

    if request.method == 'POST':
        if client_id:
            form = ClientForm(request.POST, instance=client)  # Update existing client
        else:
            form = ClientForm(request.POST)  # Create new client

        if form.is_valid():
            form.save()
            return redirect('saved_list')  # Redirect to the saved list page

    return render(request, 'crm_app/add_customer.html', {'form': form})

def saved_list(request):
    customers = Client.objects.all()
    saudi_maids = customers.filter(designation="Saudi Arabia house maid")
    return render(request, 'crm_app/saved_list.html', {'customers': customers, 'saudi_maids': saudi_maids})

# View for the landing page after login
@login_required
def dashboard(request):
    return render(request, 'crm_app/dashboard.html')

def saved_list(request):
    query = request.GET.get('q', '')  # Get search query from URL
    designation_filter = request.GET.get('designation', '')  # Get designation filter from URL

    # Base queryset
    clients = Client.objects.all()

    # Apply search filter
    if query:
        clients = clients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    
    # Apply designation filter
    if designation_filter:
        clients = clients.filter(designation=designation_filter)
    
    # Get unique designations for the dropdown
    designations = Client.objects.values_list('designation', flat=True).distinct()

    context = {
        'clients': clients,
        'query': query,
        'designation_filter': designation_filter,
        'designations': designations,
    }
    return render(request, 'crm_app/saved_list.html', context)

def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('saved_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'crm_app/edit_client.html', {'form': form})

def delete_customer(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        client.delete()
        return redirect('saved_list') 
@login_required
def housemaid_form_list(request):
    if request.method == 'POST':
        form = HousemaidForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Housemaid added successfully.")
            return redirect('housemaid_form_list')
        else:
            messages.error(request, "Failed to add housemaid. Please check the form.")
    else:
        form = HousemaidForm()

    housemaids = Housemaid.objects.all()
    return render(request, 'housemaid_form_list.html', {'form': form, 'housemaids': housemaids})

def delete_housemaid(request, housemaid_id):
    housemaid = get_object_or_404(Housemaid, id=housemaid_id)
    housemaid.delete()
    return redirect('housemaid_form_list')

def housemaid_list(request):
    query = request.GET.get('search', '')  # Get the search parameter
    travel_filter = request.GET.get('travel', '')  # Get the travel filter parameter

    housemaids = Housemaid.objects.all()  # Start with all objects

    # Filter by search query
    if query:
        housemaids = housemaids.filter(
            models.Q(name__icontains=query) |  # Search by name
            models.Q(passport__icontains=query)  # Search by passport
        )

    # Filter by travel
    if travel_filter:
        housemaids = housemaids.filter(travel=travel_filter)

    return render(request, 'housemaid_list.html', {
        'housemaids': housemaids,
        'query': query,
        'travel_filter': travel_filter,
    })
    
    return render(request, 'housemaid_form_list.html', {'housemaids': housemaids})


def edit_housemaid(request, housemaid_id):
    housemaid = get_object_or_404(Housemaid, id=housemaid_id)

    if request.method == 'POST':
        # Update Housemaid fields
        housemaid.name = request.POST.get('name', housemaid.name)
        housemaid.contact = request.POST.get('contact', housemaid.contact)
        housemaid.passport = request.POST.get('passport', housemaid.passport)
        housemaid.training = request.POST.get('training', housemaid.training)
        housemaid.exit = request.POST.get('exit', housemaid.exit)
        housemaid.medical = request.POST.get('medical', housemaid.medical)
        housemaid.pcc = request.POST.get('pcc', housemaid.pcc)
        housemaid.travel = request.POST.get('travel', housemaid.travel)

        housemaid.save()

        

        # Optional: Add a success message
        messages.success(request, "Housemaid details updated successfully.")
        return redirect('housemaid_form_list')

    return render(request, 'edit_housemaid.html', {
        'housemaid': housemaid,
    })


def add_housemaid(request):
    if request.method == 'POST':
        # Housemaid data
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        passport = request.POST.get('passport', '')
        training = request.POST.get('training')
        exit_status = request.POST.get('exit')
        medical = request.POST.get('medical')
        pcc = request.POST.get('pcc')
        office = request.POST.get('office')
        travel = request.POST.get('travel')
        comments = request.POST.get('comments')

        # Next of Kin data
        kin_name = request.POST.get('next_of_kin_name')
        kin_relationship = request.POST.get('next_of_kin_relationship')
        kin_contact = request.POST.get('next_of_kin_contact')
        kin_phone = request.POST.get('next_of_kin_phone')
        kin_contact2 = request.POST.get('next_of_kin_contact2')

        # Create Housemaid instance
        housemaid = Housemaid.objects.create(
            name=name,
            contact=contact,
            passport=passport,
            training=training,
            exit=exit_status,
            medical=medical,
            pcc=pcc,
            office=office,
            travel=travel,
            comments=comments
        )

        # Create Next of Kin instance
        NextOfKin.objects.create(
            housemaid=housemaid,
            name=kin_name,
            relationship=kin_relationship,
            contact=kin_contact,
            phone=kin_phone,
            contact2=kin_contact2
        )

        messages.success(request, 'Housemaid and Next of Kin added successfully!')
        return redirect('housemaid_form_list')  # Redirect to the housemaid list

    return render(request, 'housemaid_form_list.html')  # Reload the same template if needed

