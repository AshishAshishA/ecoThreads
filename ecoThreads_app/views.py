from .models import Category, City, Area, Address, Orders
from .forms import OrderForm, UpdateStatusForm

from django.http import HttpResponseForbidden

from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from allauth.account import views as auth_views

from django.http import JsonResponse

def get_areas(request, city_id):
    areas = list(Area.objects.filter(city_id=city_id).values('id', 'name'))
    return JsonResponse(areas, safe=False)


class DashboardView(TemplateView):
    template_name = 'customer/dashboard.html'

dashboard = DashboardView.as_view()

class CreateOrderView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    raise_exception = False
    login_url='login'
    redirect_field_name = 'next'
    permission_required = []

    model = Orders
    form_class = OrderForm
    template_name = 'customer/create_order.html'

    def form_valid(self, form):
        print('validating form')
        form.instance.user = self.request.user
        address = Address(
            area=form.cleaned_data['area'],
            pin_code=form.cleaned_data['pin_code'],
            latitude=form.cleaned_data['latitude'],
            longitude=form.cleaned_data['longitude']
        )
        address.save()
        print('address saved',address)
        form.instance.address = address
        return super().form_valid(form)

    def get_success_url(self):
        order = self.object
        return reverse('review-order', args=[order.id])


createOrder = CreateOrderView.as_view()

class ReviewOrderView(DetailView):
    model = Orders
    template_name = 'customer/review_order.html'
    context_object_name = 'order'

reviewOrder = ReviewOrderView.as_view()

class UpdateOrderView(UpdateView):
    model = Orders
    form_class = OrderForm
    template_name = 'customer/create_order.html'

    def get_success_url(self):
        order = self.object
        return reverse('review-order', args=[order.id])

updateOrder = UpdateOrderView.as_view()

class MyOrdersView(ListView):
    model = Orders
    template_name = 'customer/order_list.html'
    context_object_name = 'orders'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        print(self.request.user)

        context['orders'] = context['orders'].filter(user__username = self.request.user)

        return context

myOrders = MyOrdersView.as_view()

class OrderDeleteView(DeleteView):
    model = Orders
    template_name = 'customer/review_order.html'
    
    success_url = reverse_lazy('my-orders')

deleteOrder = OrderDeleteView.as_view()


# allauth authentication
class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        next_url = self.request.POST.get('next')
        # print(self.request)

        if next_url:
            return next_url
        else:
            return reverse_lazy('dashboard')

allauth_login = CustomLoginView.as_view()

class CustomSignUpView(auth_views.SignupView):
    def get_success_url(self):
        next_url = self.request.POST.get('next')

        if next_url:
            return next_url
        else:
            return reverse_lazy('dashboard')

allauth_signup = CustomSignUpView.as_view()


#staff section
class StaffDashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    raise_exception = False
    login_url = 'login'
    permission_required = ['ecoThreads_app.view_orders','ecoThreads_app.change_orders']
    permission_denied_message="404 NOT FOUND"
    redirect_field_name = 'next'

    template_name = 'staff/dashboard.html'

    

staff_dashboard = StaffDashboardView.as_view()
        
class OrderListView(ListView):
    model = Orders
    template_name = 'staff/orders_list.html'
    context_object_name = 'orders'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        if 'status' in self.kwargs.keys():
            context['orders'] = context['orders'].filter(status=self.kwargs['status'])

        return context

orders_list = OrderListView.as_view()

class UpdateOrderStatusView(UpdateView):
    model = Orders
    form_class = UpdateStatusForm
    template_name = 'staff/update_status.html'
    success_url = reverse_lazy('orders_list')

update_status = UpdateOrderStatusView.as_view()

class MapView(ListView):
    model = Orders
    template_name = 'staff/map.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        points=list()

        orders = Orders.objects.all()

        if 'status' in self.kwargs.keys():
            orders = Orders.objects.filter(status=self.kwargs['status'])

        for order in orders:
            points.append(
                {'lat':order.address.latitude, 'lng':order.address.longitude}
            )

        # print(points)
        
        context['points'] = points

        return context

map_view = MapView.as_view()


# def map_view(request):
#     points = [
#         {'lat': 22.7128, 'lng': 77.0060},  # Example points, replace with your data
#         {'lat': 23.0522, 'lng': 78.2437},
#         {'lat': 22.5074, 'lng': 76.1278},
#         {'lat': 23.0522, 'lng': 79.2437},
#         {'lat': 23.5074, 'lng': 78.1278},
#         # Add more points as needed
#     ]
#     return render(request, 'map.html', {'points': points})
