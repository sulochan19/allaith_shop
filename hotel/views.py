from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from .models import Customer, Order, Food, Cart, OrderContent
from .forms import SignUpForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            customer = Customer.objects.create(customer=user)
            customer.save()
            return redirect('login')
        else:
            print("invalid form")
        
    else:
        form = SignUpForm()
        
    return render(request, 'registration/signup.html', {'form': form})

@login_required
@staff_member_required
def dashboard_admin(request):
    orders = Order.objects.count()
    customers = Customer.objects.count()
    completed_orders = Order.objects.filter(payment_status="Completed")
    top_customers = Customer.objects.filter().order_by('-total_sale')
    latest_orders = Order.objects.filter().order_by('-order_timestamp')
    sales = 0
    for order in completed_orders:
        sales += order.total_amount

    context = {
        'orders':orders,
        'customers':customers,
        'sales':sales,
        'top_customers': top_customers,
        'latest_orders':latest_orders,
    }
    return render(request, 'admin_temp/index.html', context)

@login_required
@staff_member_required
def users_admin(request):
    customers = Customer.objects.filter()
    print(customers)
    return render(request, 'admin_temp/users.html', {'users':customers})

@login_required
@staff_member_required
def orders_admin(request):
    orders = Order.objects.filter().order_by('-order_timestamp')
    orders_with_contents = []
    for order in orders:
        order_contents = OrderContent.objects.filter(order=order)
        orders_with_contents.append({
            'order': order,
            'contents': order_contents
        })
    return render(request, 'admin_temp/orders.html', {'orders_with_contents': orders_with_contents})

@login_required
@staff_member_required
def foods_admin(request):
    foods = Food.objects.filter()
    return render(request, 'admin_temp/foods.html', {'foods':foods})

def index(request):
    food = Food.objects.filter().order_by('-num_order')
    items = Cart.objects.filter(user=request.user.id).count()
    return render(request, 'index.html', {'food':food,'item_count':items})


@login_required
@staff_member_required
def confirm_order(request, orderID):
    order = Order.objects.get(id=orderID)
    order.confirmOrder()
    order.save()
    customerID = order.customer.id
    customer = Customer.objects.get(id=customerID)
    customer.total_sale += order.total_amount
    customer.orders += 1
    customer.save()
    return redirect('hotel:orders_admin')

@login_required
@staff_member_required
def confirm_delivery(request, orderID):
    order = Order.objects.get(id=orderID)
    order.confirmDelivery()
    order.save()
    return redirect('hotel:orders_admin')

@login_required
@staff_member_required
def edit_food(request, foodID):
    food = Food.objects.filter(id=foodID)[0]
    if request.method == "POST":
        if request.POST['base_price'] != "":
            food.base_price = request.POST['base_price']

        status = request.POST.get('disabled')
        print(status)
        if status == 'on':
            food.status = "Disabled"
        else:
            food.status = "Enabled"
        
        food.save()
    return redirect('hotel:foods_admin')

# @login_required
# @staff_member_required
# def add_user(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_pass = request.POST['confirm_password']
#         username = email
        
#         if(email == "") or (password == "") or (confirm_pass == ""):
#             customers = Customer.objects.filter()
#             error_msg = "Please enter valid details"
#             return render(request, 'admin_temp/users.html', {'users': customers, 'error_msg': error_msg})

#         if password == confirm_pass:
#             user = User.objects.create(username=username, email=email, password=password)
#             user.save()
#             cust = Customer.objects.create(customer=user)
#             cust.save()
#             success_msg = "New user successfully created"
#             customers = Customer.objects.filter()
#             return render(request, 'admin_temp/users.html', {'users': customers, 'success_msg': success_msg})

#     return redirect('hotel:users_admin')

@login_required
@staff_member_required
def add_food(request):
    if request.method == "POST":
        name = request.POST['name']
        status = request.POST['status']
        content = request.POST['content']
        base_price = request.POST['base_price']
        sale_price = request.POST['sale_price']
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)

        if (name == "") or (status is None) or (content == "") or (base_price == ""):
            foods = Food.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'admin_temp/foods.html', {'foods': foods, 'error_msg': error_msg})

        food = Food.objects.create(name=name, status=status, content_description=content, base_price=base_price, sale_price=sale_price, image=filename)
        food.save()
        foods = Food.objects.filter()
        success_msg = "Please enter valid details"
        return render(request, 'admin_temp/foods.html', {'foods': foods, 'success_msg': success_msg})
    return redirect('hotel:foods_admin')

def food_details(request, foodID):
    food = Food.objects.get(id=foodID)
    return render(request, 'user/single.html', {'food':food})

@login_required
def addTocart(request, foodID):
    food = Food.objects.get(id=foodID)
    user = User.objects.get(id=request.user.id)
    cart = Cart.objects.create(food=food, user=user)
    cart.save()
    return redirect('hotel:index')

@login_required
def delete_item(request, ID):
    item = Cart.objects.get(id=ID)
    item.delete()
    return redirect('hotel:cart')

@login_required
def cart(request):
    user = User.objects.get(id=request.user.id)
    items = Cart.objects.filter(user=user)
    item_count = Cart.objects.filter(user=request.user.id).count()
    total = 0
    for item in items:
        total += item.food.sale_price
        
    return render(request, 'cart.html', {'items': items, 'total':total,'item_count': item_count})

@login_required
def placeOrder(request):
    customer = Customer.objects.get(customer=request.user)
    items = Cart.objects.filter(user=request.user)
    if items:
        for item in items:
            food = item.food
            if food.quantity_available > 0:
                order = Order.objects.create(customer=customer, order_timestamp=timezone.now(), payment_status="Pending", 
                delivery_status="Pending", total_amount=food.sale_price)
                order.save()
                orderContent = OrderContent(food=food, order=order)
                orderContent.save()
                item.food.quantity_available -= 1
                item.food.save()
                item.delete()
    return redirect('hotel:index')

@login_required
def my_orders(request):
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(customer=user)
    orders = Order.objects.filter(customer=customer).order_by('-order_timestamp')

    orders_with_contents = []
    for order in orders:
        order_contents = OrderContent.objects.filter(order=order)
        orders_with_contents.append({
            'order': order,
            'contents': order_contents
        })

    return render(request, 'orders.html', {'orders_with_contents': orders_with_contents})


        
