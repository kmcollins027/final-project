from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail, BadHeaderError

from .models import User, Item, Category, Cart
from . import forms
from .forms import ContactForm

def index(request):
    return render(request, "shop/index.html", {"users": User.objects.all()})


class ItemView(ListView):
    model = Item
    template_name = "shop/index.html"
    context_object_name = "items"

    def get_queryset(self):
        if 'sorted' in self.request.GET:
            choice = self.request.GET['sorted']
            if choice == 'price_sorted_low':
                return Item.objects.all().order_by('price')
            if choice == 'price_sorted_high':
                return Item.objects.all().order_by('-price')
            if choice == 'name_sorted_A':
                return Item.objects.all().order_by('title')
            if choice == 'name_sorted_Z':
                return Item.objects.all().order_by('-title')
        return Item.objects.all()

    def get_context_data(self):
        context = super().get_context_data()
        return context


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "shop/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "shop/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "shop/register.html")

@login_required(login_url='login')
def account(request):
    return render(request, "shop/account.html")

def update_account(request):
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        form = forms.UserAccountUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("account"))

    else:
        form = forms.UserAccountUpdateForm(instance=user)
        
    return render(request, "shop/update_account.html", {"form": form})

class UpdateAccount(UpdateView):
    model = User
    fields = ['email','first_name', 'last_name', 'image']
    success_url = reverse_lazy("account")
    template_name_suffix = '_update_form'


class LoginView():
    template_name = 'registration/login.html'
    redirect_field_name = 'shop/index'

class LogoutView():
    template_name = 'registration/logout.html'
    redirect_field_name = 'shop/index'

class PasswordChangeView():
    template_name = 'registration/password_change_form.html'
    success_url = 'registration/password_change_done.html'

class PasswordChangeDoneView():
    template_name = 'registration/password_change_done.html'

class PasswordResetView():
    template_name = 'registration/password_reset_form.html'
    success_url = 'registration/password_reset_done.html'

class PasswordResetDoneView():
    template_name = 'registration/password_reset_done.html'

class PasswordResetConfirmView():
    template_name = 'registration/password_reset_confirm.html'
    success_url = 'registration/password_reset_complete.html'

class PasswordResetCompleteView():
    template_name = 'registration/password_reset_complete.html'

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'image']
    success_url = reverse_lazy("categories")

class CategoryListView(ListView):
    model = Category
    template_name = "shop/categories.html"
    context_object_name = "categories"

class CategoryItemsView(ListView):
   model = Item
   template_name = "shop/category_items.html"
   context_object_name = "items"
 
   def get_queryset(self):
       return Item.objects.filter(categories=self.kwargs["category_id"])
 
   def get_context_data(self):
       context = super().get_context_data()
       category_id = self.kwargs["category_id"]
       category = Category.objects.get(id=category_id)
       context['category'] = category
       #context['banner'] = f'{category.name} Category ({self.get_queryset().count()} listings)'
       return context

class CreateItem(CreateView):
    model = Item
    template_name = 'shop/new_item.html'
    fields = ['title', 'description', 'price', 'categories', 'image']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateItem(UpdateView):
    model = Item
    template_name = 'shop/update_item.html'
    fields = ['title', 'description', 'price', 'categories', 'image']
    success_url = reverse_lazy('index')
    
    
def item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    for category in item.categories.all():
        category_id = Category.objects.get(id=category.id)
        related_items = Item.objects.filter(categories=category_id)

    return render(request, "shop/item.html", {"item": item, 
                           "related_items": related_items,
                           "save_id": item_id,
                           })

def review(request):
    return render(request, "shop/review.html")


def add_to_cart(request, item_id):
    if request.method == 'POST':
        quantity = request.POST.get('inputQuantity')

        item_listing = get_object_or_404(Item, pk=item_id)
        Cart.objects.create(user=request.user, item_id=item_listing.id, quantity=quantity)

        return HttpResponseRedirect(reverse("item", args=[item_id]))

def remove_from_cart(request, item_id):
    if request.method == "POST":
        quantity = request.POST.get('inputQuantity')

        item_listing = get_object_or_404(Cart, pk=item_id)
        item_listing.delete()
        return redirect(cart)

def about(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry" 
            body = {
            'first_name': form.cleaned_data['first_name'], 
            'last_name': form.cleaned_data['last_name'], 
            'email': form.cleaned_data['email'], 
            'message':form.cleaned_data['message'], 
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'djangoemail027@gmail.com', ['djangoemail027@gmail.com']) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect ("index")
      
    form = ContactForm()
    return render(request, "shop/about.html", {'form':form})



def api_add_to_cart(request, item_id):
    if request.method == 'POST':
        quantity = request.POST.get('inputQuantity')
        #print(quantity)

        item_listing = get_object_or_404(Item, pk=item_id)
        Cart.objects.create(user=request.user, item_id=item_listing.id, quantity=quantity)
        return JsonResponse({
            'quantity': quantity,
        })
    #return JsonResponse({'error': 'something went wrong'})

def api_remove_from_cart(request, item_id):
    if request.method == "POST":
        quantity = request.POST.get('inputQuantity')
        #print(quantity)

        item_listing = get_object_or_404(Cart, pk=item_id)
        item_listing.delete()
        return JsonResponse({
            'quantity': quantity,
        })
    return JsonResponse({'error': 'something went wrong'})

@login_required(login_url='login')
def cart(request):
    shopping_cart = Cart.objects.filter(user=request.user)
    cart = Item.objects.filter(id__in=shopping_cart)
    return render(request, "shop/cart.html", {
        'shopping_cart': shopping_cart,
        'cart': cart,
        'count': len(shopping_cart),
        })


def api_counters(request):
    counts = {'cart': Cart.objects.filter(user=request.user).count()}
    cart = Cart.objects.filter(user=request.user)
    for item in cart:
        counts['cart'] += (item.quantity - 1)

    print(f'api_counters called. returning {counts}')
    return JsonResponse(counts)
