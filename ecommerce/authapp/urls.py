from django.urls import path, include
from .views import (
    SignUpView,
    UserLoginView,
    UserProfileView,
    UserLogoutView,
    ChangePasswordView,
    UserListView,
    UserDetialView,
    UpdateUserView,
    DeleteUserView,
    DashboardView,
    # dispatch_dashboard  # Add this import
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepass/', ChangePasswordView.as_view(), name='change password'),
    path('users_list/', UserListView.as_view(), name='users list'),
    path('user_detail/<int:pk>/', UserDetialView.as_view(), name='user detail'),
    path('update/<int:pk>/', UpdateUserView.as_view(), name='user update'),
    path('delete/<int:pk>/', DeleteUserView.as_view(), name='user delete'),
    # path('dashboard/', dispatch_dashboard, name='dispatch_dashboard'),  # Add this URL
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Adjust this URL as needed
    path('pro/', include('Product.urls')),
]
