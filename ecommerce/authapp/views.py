from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import SignupForm, user_detail
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import CustomUser
from django.views.generic.detail import DetailView
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse 
from django.contrib.auth.models import Group
from .permission import Admin_group_permissions
from .forms import CustomAuthenticationForm
# local_user_group, created = Group.objects.get_or_create(name='Local Users')

# admin_group, created = Group.objects.get_or_create(name='Admin2')
# admin_group.permissions.set(Admin_group_permissions)

from django.http import HttpResponseRedirect
class AdminGroupMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        return HttpResponse('no permission')  

class SignUpView(CreateView):
    model = CustomUser
    form_class = SignupForm
    template_name = 'authapp/signup.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        local_user_group =Group.objects.get(name='Local Users')
        user.groups.add(local_user_group)
        login(self.request, user)
        messages.success(self.request, 'Account Created Successfully !!')
        return super().form_valid(form)

class DeleteUserView(AdminGroupMixin, DeleteView):
    model = CustomUser
    template_name = 'authapp/user_delete.html'
    success_url = reverse_lazy('users list')


from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator


class UpdateUserView(UpdateView):
    model = CustomUser
    fields = ['username', 'first_name', 'last_name', 'phone_number', 'email']
    template_name = 'authapp/user_update.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        user = self.get_object()  # Get the user being updated
        return  user == self.request.user
    def form_valid(self, form):
        # Here, you can add a success message
        messages.success(self.request, 'Information Update Successfully')
        return super().form_valid(form)

    # def test_func(self):
    #     return has_change_permission(self.request.user)

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)





class UserLoginView(View):
    def get(self, request):
        login_obj = CustomAuthenticationForm()
        return render(request, 'authapp/login.html', {'login_obj': login_obj})

    def post(self, request):
        auth_obj = CustomAuthenticationForm(request=request, data=request.POST)
        if auth_obj.is_valid():
            uname = auth_obj.cleaned_data['username']
            upass = auth_obj.cleaned_data['password']
            user_obj: CustomUser = authenticate(username=uname, password=upass)
            if user_obj is not None:
                
                login(request, user_obj)
                messages.success(request, 'Login Successfully')
                permission = user_obj.get_group_permissions()
                # print(permission)
                
                session = user_obj.get_session_auth_hash()
                print(session)
                # data = {
                    # "username": user_obj.username,
                    # "permissions": user_obj.peru
                # }
                return render(request, 'authapp/dashboard.html',{'user_obj':user_obj})
                # return redirect('/auth/dashboard/?permission={}'.format(permission))
                # return self.handle_redirect(request, permission)
        login_obj = CustomAuthenticationForm()
        return render(request, 'authapp/login.html', {'login_obj': auth_obj})

    # def handle_redirect(self, request, permission):
    #     if 'authapp.add_customuser' in permission:  # Replace with your specific permission check
    #         return redirect('/auth/dashboard/users_list/')
    #     else:
    #         return redirect('/auth/dashboard/')

# class DashboardView(TemplateView):
#     template_name = 'authapp/dashborad.html'
    
#     # @login_required(login_url='/auth/login/')
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user  # Pass the user object to the context
#         return context
    
class UserProfileView(View):
    @method_decorator(login_required(login_url='/auth/login/'))
    def get(self, request):
        detail = user_detail(instance=request.user)
        return render(request, 'authapp/profile.html', {'detail': detail})
    
    
class ChangePasswordView(View):
    @method_decorator(login_required(login_url='/auth/login/'))
    def get(self, request):
        form_obj = SetPasswordForm(user=request.user)
        return render(request, 'authapp/changepass.html', {'form_obj': form_obj})

    def post(self, request):
        form_obj = SetPasswordForm(user=request.user, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            update_session_auth_hash(request, form_obj.user)
            messages.success(request, 'Password updated successfully')
            return redirect('/auth/profile/')
        else:
            for field, errors in form_obj.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            return render(request, 'authapp/changepass.html', {'form_obj': form_obj})


class UserLogoutView(View):
    # @method_decorator(login_required(login_url='/auth/login/'))
    def get(self, request):
        logout(request)
        return redirect('/auth/login/')

class UserListView(AdminGroupMixin, ListView):
    model = CustomUser
    template_name = 'authapp/user_list.html'
    context_object_name = 'users'
    ordering = ['username']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        users = CustomUser.objects.exclude(pk=self.request.user.pk).exclude(groups__name='Admin').exclude(is_superuser=True)
        context['users'] = users
        return context



class UserDetialView(AdminGroupMixin, DetailView):
    model = CustomUser  
    context_object_name = 'user'
    template_name = 'authapp/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        viewed_user = context['user']

        # Check if the viewed profile is the user's own profile
        is_own_profile = self.request.user == viewed_user

        # Check if the user has permission to delete users
        can_delete_user = self.request.user.has_perm('authapp.delete_customuser')

        context['is_own_profile'] = is_own_profile
        context['can_delete_user'] = can_delete_user

        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'authapp/dashboard.html'
    login_url = 'login'





from django.contrib.auth.decorators import login_required

from Product.models import Product 




    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.user.is_authenticated:
    #         # Check if the user has permission to view products
    #         if self.request.user.has_perm('authapp.view_product'):
    #             # Fetch the list of products (customize the query)
    #             products = Product.objects.all()
    #             context['products'] = products

    #         # Check if the user has permission to view users
    #         if self.request.user.has_perm('authapp.view_customuser'):
    #             # Fetch the list of users (customize the query)
    #             users = CustomUser.objects.exclude(pk=self.request.user.pk).exclude(groups__name='Admin').exclude(is_superuser=True)
    #             context['users'] = users
    #         if self.request.user.has_perm('authapp.add_customuser') or \
    #            self.request.user.has_perm('authapp.change_customuser') or \
    #            self.request.user.has_perm('authapp.delete_customuser'):
    #             context['can_curd_users'] = True
    #         # Pass the user's profile to the template
    #         context['user_profile'] = self.request.user

    #     return context

@login_required
def dispatch_dashboard(request):
    user = request.user
    if user.has_perm('authapp.view_customuser'):
        # User has the required permission to access the dashboard.
        return redirect('dashboard')
    else:
        # Handle the case where the user does not have the required permission.
        # You can redirect them to another view or show an error message.
        return redirect('login')  # Redirect to the login page for now.




# view_all_users_permission = Permission.objects.get(codename='view_customuser')
# admin_group.permissions.add(view_all_users_permission)

# change_user_details_permission = Permission.objects.get(codename='change_customuser')
# admin_group.permissions.add(change_user_details_permission)

# delete_user_permission = Permission.objects.get(codename='delete_customuser')
# admin_group.permissions.add(delete_user_permission)

# add_user_permission = Permission.objects.get(codename='add_customuser')
# admin_group.permissions.add(add_user_permission)

# add_product_permission = Permission.objects.get(codename='add_product')
# admin_group.permissions.add(add_product_permission)

# update_product_permission = Permission.objects.get(codename='change_product')
# admin_group.permissions.add(update_product_permission)

# delete_product_permission = Permission.objects.get(codename='delete_product')
# admin_group.permissions.add(delete_product_permission)

# view_product_permission = Permission.objects.get(codename='view_product')
# admin_group.permissions.add(view_product_permission)





# from django.contrib.auth.decorators import user_passes_test

# def has_view_permission(user):
#     return user.has_perm('authapp.view_customuser')

# def has_change_permission(user):
#     return user.has_perm('authapp.change_customuser')

# def has_delete_permission(user):
#     return user.has_perm('authapp.delete_customuser')

# def has_add_permission(user):
#     return user.has_perm('authapp.add_customuser')
