from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^myorders/$', views.my_orders, name='my_orders'),
    
    url(r'^dashboard/admin/users/$', views.users_admin, name='users_admin'),
    url(r'^dashboard/admin/orders/$', views.orders_admin, name='orders_admin'),
    url(r'^dashboard/admin/foods/$', views.foods_admin, name='foods_admin'),
    url(r'^dashboard/admin/$', views.dashboard_admin, name='dashboard_admin'),
    
    # url(r'^dashboard/admin/users/add_user/$', views.add_user, name='add_user'),
    url(r'^dashboard/admin/foods/add_food/$', views.add_food, name='add_food'),
    url(r'^dashboard/admin/foods/editFood/(?P<foodID>\d+)/$', views.edit_food, name='edit_food'),
    url(r'^dashboard/admin/foods/foodDetails/(?P<foodID>\d+)/$', views.food_details, name='food_details'),
    
    url(r'^dashboard/admin/orders/confirm_order/(?P<orderID>\d+)/$', views.confirm_order, name='confirm_order'),
    url(r'^dashboard/admin/orders/confirm_delivery/(?P<orderID>\d+)/$', views.confirm_delivery, name='confirm_delivery'),
    
    url(r'^delete_item/(?P<ID>\d+)/$', views.delete_item, name='delete_item'),
    url(r'^placeOrder/$', views.placeOrder, name='placeOrder'),
    url(r'^addTocart/(?P<foodID>\d+)/$', views.addTocart, name='addTocart'),
]
