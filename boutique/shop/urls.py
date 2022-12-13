from django.urls import path
from . import views, forms
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('', views.index, name='index'),
    path("", views.ItemView.as_view(), name="index"),
    path('register', views.register, name='register'),

    path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("account", views.account, name='account'),
    #path("account/update/<int:pk>", views.UpdateAccount.as_view(), name="update-account"),
    path("update_account", views.update_account, name="update-account"),
    path("password_change", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=forms.MyPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path("categories", views.CategoryListView.as_view(), name="categories"),
    path("category/<int:category_id>", views.CategoryItemsView.as_view(), name="category"),
    path("create_category", views.CategoryCreateView.as_view(), name="create-category"),
    path("create_item", views.CreateItem.as_view(), name="create-item"),
    path("item/<int:item_id>", views.item, name="item"),
    path("update_item/<int:pk>", views.UpdateItem.as_view(), name="update-item"),
    path("review", views.review, name="review"),
    path("cart", views.cart, name="cart"),
    path("add_to_cart/<int:item_id>", views.add_to_cart, name="add-to-cart"),
    path("remove_from_cart/<int:item_id>", views.remove_from_cart, name="remove-from-cart"),
    path("about", views.about, name="about"),

    path("api/add_to_cart/<int:item_id>", views.api_add_to_cart, name="api-add-to-cart"),
    path("api/remove_from_cart/<int:item_id>", views.api_remove_from_cart, name="api-remove-from-cart"),
    path("api/counters", views.api_counters, name="api-counters"),

]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
