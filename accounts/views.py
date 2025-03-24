from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .forms import AdForm,CustomUserCreationForm
from .models import item



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('home')  # Redirect to home page
    else:
         form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def home(request):
    return render(request, 'accounts/index.html')  # Render the home page template

@login_required
def dashboard(request):
    # Fetch latest 5 items
    featured_items = item.objects.all()[:5]

    return render(request, 'accounts/dashboard.html', {'featured_items': featured_items})

def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def buy(request):
    # Predefined categories
    categories = ['Electronics', 'Furniture', 'Clothing', 'Books', 'Other']
    
    # Predefined locations (D1 to D24)
    locations = [f'D{i}' for i in range(1, 25)]

    # Start with all items
    items = item.objects.all()

    # Get filter and search parameters from the request
    search_query = request.GET.get('search', '')
    selected_category = request.GET.get('category', '')
    selected_location = request.GET.get('location', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Apply filters to items
    if search_query:
        items = items.filter(Q(product_title__icontains=search_query) | Q(product_description__icontains=search_query))
    if selected_category:
        items = items.filter(category=selected_category)
    if selected_location:
        if selected_location.startswith("D") and selected_location[1:].isdigit():
           district_number = selected_location[1:]  # Extract number after 'D'
           if len(district_number) == 1:  
            # If it's a single digit (D1-D9), match with D01-D09
               items = items.filter(location__startswith=f"D0{district_number}")
           else:
            # If it's already D10-D24, match locations that start with it
               items = items.filter(location__startswith=selected_location)
        else:
        # Fallback for non-standard cases
          items = items.filter(location__startswith=selected_location)
    if min_price:
        items = items.filter(price__gte=float(min_price))
    if max_price:
        items = items.filter(price__lte=float(max_price))

    # Pass data to the template
    context = {
        'app_name': 'Trade Hub',
        'categories': categories,
        'locations': locations,
        'results': items,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_location': selected_location,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'accounts/buy.html', context)

@login_required
def item_details(request, item_id):
    # Fetch item details from the database
    Item = get_object_or_404(item, product_id=item_id)

    # Context data for the details page
    context = {
        'app_name': 'Trade Hub',
        'item': Item,
    }
    return render(request, 'accounts/item_details.html', context)

# @login_required
# def post_ad(request):
#     if request.method == 'POST':
#         # Bind the form to the POST data and files
#         form = AdForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the form data to the database
#             ad = form.save(commit=False)
#             # Assign the logged-in user as the seller
#             ad.seller = request.user
#             form.save()
#             # Redirect to a success page or the homepage
#             return redirect('dashboard')  # Replace 'dashboard' with your success URL name
#         else:
#             # If the form is invalid, re-render the form with errors
#             print("Form errors:", form.errors)  # Debugging: Print form errors
#     else:
#         # If it's a GET request, create a new empty form
#         form = AdForm()
#     # Render the post_ad template with the form
#     return render(request, 'accounts/post_ad.html', {'form': form})

@login_required
def post_ad(request):
    if request.method == 'POST':
        # Bind the form to the POST data and files
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            ad = form.save(commit=False)
            # Assign the logged-in user as the seller
            ad.seller = request.user
            ad.save()  # Save the ad to the database
            return redirect('dashboard')  # Replace 'dashboard' with your success URL name
        else:
            print("Form errors:", form.errors)  # Debugging: Print form errors
    else:
        # If it's a GET request, create a new empty form
        form = AdForm()
    return render(request, 'accounts/post_ad.html', {'form': form})

@login_required
def update_details(request,product_id):
    ad1 = item.objects.get(product_id=product_id)
    if request.method == 'POST':
        form = AdForm(request.POST,request.FILES, instance = ad1)
        if form.is_valid():
            form.save()
            return redirect('My_ads')
    else :
        form = AdForm(instance=ad1)
        return render(request, 'accounts/update_ad.html', {'form': form})
    
@login_required
def delete_ad(request, product_id):
    ad1 = get_object_or_404(item, product_id=product_id)
    ad1.delete()
    return redirect('My_ads')    

@login_required
def My_ads(request):
    # Fetch item details from the database
    update_item = item.objects.filter(seller_id = request.user)
    # update_item = item.objects.all()
    # Context data for the details page
    context = { 
        'items' : update_item
    }
    return render(request, 'accounts/update.html', context)
    