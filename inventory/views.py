from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import Shop, Customer, Product, Order, AdminUser,Cart
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
# Main Page View
from django.contrib import messages


def mainPage(request):
    return render(request, 'mainPage.html')
# Shop Registration View
def shop_register(request):
    if request.method == 'POST':
        s_name = request.POST['s_name']
        s_contact = request.POST['s_contact']
        s_email = request.POST['s_email']
        s_password = request.POST['s_password']
        try:
            shop = Shop.objects.get(s_email=s_email)
            messages.error(request,"Shop Already exists")
            return render(request, 'shop_register.html')
        except Shop.DoesNotExist:
            pass
        shop = Shop(s_name=s_name, s_contact=s_contact, s_email=s_email, s_password=s_password)
        shop.save()
        messages.success(request,"Shop Registerd Successfully")
        return redirect('shop_login')

    return render(request, 'shop_register.html')

# Shop Login View
def shop_login(request):
    if request.method == 'POST':
        s_email = request.POST['s_email']
        s_password = request.POST['s_password']

        try:
            shop = Shop.objects.get(s_email=s_email, s_password=s_password)
            request.session['shop_id'] = shop.s_id
            messages.success(request,"Shop Login Successfully")
            return redirect('shop_dashboard')
        except Shop.DoesNotExist:
            messages.error(request,"Shop Does exists or Invalid Credentials")
            return render(request, 'shop_login.html')

    return render(request, 'shop_login.html')

# Shop Dashboard (View Products)

def shop_dashboard(request):
    shop = get_logged_in_shop(request)
    if not shop:
        return redirect("shop_login") 
    
    if 'shop_id' not in request.session:
        return redirect('shop_login')

    shop = Shop.objects.get(s_id=request.session['shop_id'])
    products = Product.objects.filter(shop=shop)
    for product in products:
        print(f"Product ID: {product.p_id}, Name: {product.p_name}")
    return render(request, 'shop_dashboard.html', {'products': products})

# Shop Logout
def shop_logout(request):
    logout(request)
    messages.success(request,"Logouted")
    return redirect('shop_login')


# Add Product View

def add_product(request):
    shop = get_logged_in_shop(request)
    if not shop:
        return redirect("shop_login") 
    print('in add product view function',request.session['shop_id'])

    if request.method == "POST":
        # 🔥 Fetch the shop instance from the logged-in user
        try:
            shop = Shop.objects.get(s_id=request.session['shop_id'])  # Match with email
        except Shop.DoesNotExist:
            messages.error(request,"Shop not found")
            return redirect("/shop/login/")  # Redirect to login if shop not found

        # ✅ Create product with the shop instance
        product =Product.objects.create(
            p_name=request.POST["p_name"],
            p_price= request.POST["p_price"],
            p_description=request.POST["p_description"],
            p_stock=request.POST["p_stock"],
            shop=shop  # 🔥 Assign the actual Shop instance, not request.user
        )
        product.save()
        print(f"New Product Added: ID={product.p_id}, Name={product.p_name}")
        messages.success(request,"Product Added successfuly")
        return redirect("/shop/dashboard/")

    return render(request, "show_dashboard.html")

# Edit Product View
def edit_product(request,p_id):
    shop = get_logged_in_shop(request)
    if not shop:
        return redirect("shop_login")  # Redirect to login if not authenticated

    if request.method=="GET":
        product = Product.objects.get(p_id=p_id)
        print(product.p_name)
        return render(request, "edit_product.html",{"product":product})
    if request.method=="POST":
        p_name = request.POST["p_name"]
        p_price = request.POST["p_price"]
        p_description = request.POST["p_description"]
        p_stock = request.POST["p_stock"]
       
        product = Product.objects.get(p_id=p_id)
        product.p_name = p_name
        product.p_price = p_price
        product.p_description = p_description
        product.p_stock = p_stock
        product.save()
        messages.success(request,"Updated Successfully")
        return redirect("/shop/dashboard/")
    return render(request, "edit_product.html")

# Delete Product View
def delete_product(request,p_id):
    if 'shop_id' not in request.session:
        return redirect('shop_login')

    shop = get_object_or_404(Shop, s_id=request.session['shop_id'])  # ✅ Get the shop correctly
    product = get_object_or_404(Product, p_id=p_id, shop=shop)   # ✅ Get the product for this shop

    product.delete()  # 🔥 Delete the product
    messages.success(request,"Product Deleted")
    return redirect('shop_dashboard')

def shop_orders(request):
    if 'shop_id' not in request.session:
        return redirect('shop_login')
    
    shop = get_object_or_404(Shop, s_id=request.session['shop_id'])
    #product=get_object_or_404(Product,shop=shop)
    orders=get_object_or_404(Order,shop=shop)
    for order in orders:
        print(order.order_id)
        redirect('/shop/dashboard/')
    render(request,"shop_dashboard",{"orders":orders})

def get_logged_in_shop(request):
    """Helper function to get the logged-in shop from session."""
    shop_id = request.session.get("shop_id")
    if shop_id:
        return Shop.objects.get(s_id=shop_id)
    return None
    
# Customer Registration View
def customer_register(request):
    
    start=True
    if request.method == 'POST':
        c_name = request.POST['c_name']
        c_mobile = request.POST['c_mobile']
        c_email = request.POST['c_email']
        c_pass = request.POST['c_pass']

        customer = Customer(c_name=c_name, c_mobile=c_mobile, c_email=c_email, c_pass=c_pass)
        customer.save()
        return redirect('customer/login')
    if not start:
        res={'error': 'Invalid credentials or Already Available'}
        start=False 
        return render(request, 'customer_register.html',res)
    else:
        return render(request, 'customer_register.html')

# Customer Login View
def customer_login(request):
    if request.method == 'POST':
        c_email = request.POST['c_email']
        c_pass = request.POST['c_pass']

        try:
            customer = Customer.objects.get(c_email=c_email, c_pass=c_pass)
            request.session['customer_id'] = customer.c_id
            return redirect('customer_dashboard')
        except Customer.DoesNotExist:
            return render(request, 'customer_login.html', {'error': 'Not exists or bad request'})

    return render(request, 'customer_login.html')

# Customer Dashboard (View Products)

def customer_dashboard(request):
    if 'customer_id' not in request.session:
        return redirect('customer_login')

    shops = Shop.objects.all()
    products = Product.objects.all()
    for product in products:
        shopname = product.shop.s_name
        print(f"Product ID: {product.p_id}, Name: {product.p_name}, Shop: {shopname}")
    return render(request, 'customer_dashboard.html', {'shops': shops, 'products': products})

# Customer Logout
def customer_logout(request):
    logout(request)
    return redirect('customer_login')

def get_logged_in_customer(request):
    """Helper function to get the logged-in customer from session."""
    customer_id = request.session.get("customer_id")
    print(f"Customer ID: {customer_id}")
    if customer_id:
        print(f"Customer ID: {customer_id}")
        return Customer.objects.get(customer_id=customer_id)
    return None

def add_to_cart(request, product_id):
    if 'customer_id' not in request.session:
        return redirect('customer_login')
    
    product = get_object_or_404(Product, pk=product_id)
    customer_id = request.session['customer_id']
    
    if request.method == "POST":
        quantity = int(request.POST['quantity'])

        # Check if requested quantity is greater than available stock
        if quantity > product.p_stock:
            messages.error(request, "Not available in that quantity.")
            return redirect('customer_dashboard')

        # Check if product is already in cart
        cart_item, created = Cart.objects.get_or_create(
            customer_id=customer_id,
            product=product,
            defaults={'quantity': quantity, 'total_price': quantity * product.p_price}
        )

        if not created:
            # Update the quantity if the item is already in the cart
            if cart_item.quantity + quantity > product.p_stock:
                messages.error(request, "Not available in that quantity.")
            else:
                cart_item.quantity += quantity
                cart_item.total_price = cart_item.quantity * product.p_price
                cart_item.save()
                
        messages.success(request, "Product added to cart.")
        return redirect('customer_dashboard')

    return redirect('customer_dashboard')
    
def view_cart(request):
    if "customer_id" not in request.session:
        return redirect("customer_login")

    customer = get_object_or_404(Customer, pk=request.session.get("customer_id"))
    cart_items = Cart.objects.filter(customer=customer)
    total_price = sum(item.total_price for item in cart_items)

    return render(request, "view_cart.html", {"cart_items": cart_items, "total_price": total_price})

def checkout(request):
    if 'customer_id' not in request.session:
        return redirect('customer_login')
    
    customer_id = request.session['customer_id']
    cart_items = Cart.objects.filter(customer_id=customer_id)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    try:
        for item in cart_items:
            # Ensure that the shop ID is taken from the product
            shop_id = item.product.shop.s_id  # This assumes Product has a ForeignKey to Shop
            
            order = Order.objects.create(
                customer_id=customer_id,
                product=item.product,
                quantity=item.quantity,
                order_status="Pending",
                total_price=item.total_price,
                shop_id=shop_id  # Ensure shop_id is not NULL
            )
            item.product.p_stock -= item.quantity  # Use item.quantity instead of item.product.quantity
            item.product.save()
            order.save()
            

        # Clear the cart after successful order placement
        Order.objects.filter(customer_id=customer_id, order_status="Pending").update(order_status="Success")

        
        # Clear the cart after successful order placement
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('checkout_success')

    except IntegrityError as e:
        messages.error(request, "An error occurred during checkout. Please try again.")
        print("Checkout Error:", e)
        return redirect('view_cart')

def checkout_success(request):
    
    return render(request, 'checkout_success.html')

def remove_from_cart(request, product_id):
    if 'customer_id' not in request.session:
        return redirect('customer_login')
    
    customer_id = request.session['customer_id']
    product = get_object_or_404(Product, pk=product_id)
    cart_item = get_object_or_404(Cart, customer_id=customer_id, product=product)

    cart_item.delete()
    messages.success(request, "Item removed from cart successfully!")
    return redirect('view_cart')

def customer_orders(request):
    if 'customer_id' not in request.session:
        return redirect('customer_login')
    
    customer_id = request.session['customer_id']
    orders = Order.objects.filter(customer_id=customer_id)
    return render(request, 'customer_orders.html', {'orders': orders})

def cancel_order(request, order_id):
    if 'customer_id' not in request.session:
        return redirect('customer_login')
    
    customer_id = request.session['customer_id']
    order = get_object_or_404(Order, pk=order_id, customer_id=customer_id)
    
    # Refund stock
    product = order.product
    product.p_stock += order.quantity
    product.save()

    order.delete()
    messages.success(request, "Order Cancled successfully!")
    return redirect('customer_orders')

def shop_orders(request):
    if 'shop_id' not in request.session:
        return redirect('shop_login')
    
    shop_id = request.session['shop_id']
    orders = Order.objects.filter(shop_id=shop_id)
    return render(request, 'shop_orders.html', {'orders': orders})

def update_order_status(request, order_id):
    if 'shop_id' not in request.session:
        return redirect('shop_login')
    
    shop_id = request.session['shop_id']
    order = get_object_or_404(Order, pk=order_id, shop_id=shop_id)
    
    if request.method == 'POST':
        order.order_status = request.POST['status']
        order.save()
        return redirect('shop_orders')
    
    return render(request, 'update_order_status.html', {'order': order})



# Admin Login View
def admin_login(request):
    if 'admin_id' not in request.session:
        redirect("admin_login")
    if request.method == 'POST':
        admin_email = request.POST['admin_email']
        admin_password = request.POST['admin_password']

        try:
            admin = AdminUser.objects.get(admin_email=admin_email, admin_password=admin_password)
            request.session['admin_id'] = admin.admin_id
            messages.success(request,"loged in")
            return redirect('admin_dashboard')
        except AdminUser.DoesNotExist:
            messages.error(request,"Invalid credentials")
            return render(request, 'admin_login.html')

    return render(request, 'admin_login.html')

# Admin Dashboard (View Shops & Orders)
def admin_dashboard(request):
    if 'admin_id' not in request.session:
        messages.success(request,"Loged in first")
        return redirect('admin_login')

    shops = Shop.objects.all()
    orders = Order.objects.all()
    products=Product.objects.all()
    return render(request, 'admin_dashboard.html', {'shops': shops, 'orders': orders,'products':products})

# Admin Logout
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
# Compare this snippet from inventory_project/inventory/templates/shop_register.html:
# {% extends 'base.html' %}
def place_order(request, product_id):
    if 'customer_id' not in request.session:
        return redirect('customer_login')

    customer = Customer.objects.get(c_id=request.session['customer_id'])
    product = Product.objects.get(p_id=product_id)
    shop = product.shop  # Get the shop that owns the product

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        
        if quantity > product.stock:
            return render(request, 'place_order.html', {'product': product, 'error': 'Not enough stock!'})

        # Reduce stock count
        product.stock -= quantity
        product.save()

        # Create order entry
        order = Order(customer=customer, shop=shop, product=product, quantity=quantity, status='Pending')
        order.save()
        return redirect('customer_orders')

    return render(request, 'place_order.html', {'product': product})

# View Customer Orders
def customer_orders(request):
    if 'customer_id' not in request.session:
        return redirect('customer_login')

    customer = Customer.objects.get(c_id=request.session['customer_id'])
    orders = Order.objects.filter(customer=customer)
    return render(request, 'customer_orders.html', {'orders': orders})

# Cancel an Order
# def cancel_order(request, order_id):
#     if 'customer_id' not in request.session:
#         return redirect('customer_login')

#     order = Order.objects.get(order_id=order_id)
    
#     # Refund stock
#     product = order.product
#     product.stock += order.quantity
#     product.save()

#     order.delete()
#     return redirect('customer_orders')

# View Shop Orders
def shop_orders(request):
    if 'shop_id' not in request.session:
        return redirect('shop_login')

    shop = Shop.objects.get(s_id=request.session['shop_id'])
    orders = Order.objects.filter(shop=shop)
    return render(request, 'shop_orders.html', {'orders': orders})

# Update Order Status (Shop Owner)
def update_order_status(request, order_id):
    if 'shop_id' not in request.session:
        return redirect('shop_login')

    order = Order.objects.get(order_id=order_id)

    if request.method == 'POST':
        order.order_status = request.POST['status']
        order.save()
        messages.success(request,"Order {{order.order_status}}")
        return redirect('shop_orders')

    return render(request, 'update_order_status.html', {'order': order})

# Compare this snippet from inventory_project/inventory/views.py:
# def product_list(request):
def product_list(request):
    shop_id = request.GET.get('shop')  # Get the shop filter from the URL query parameters
    products = Product.objects.all()

    if shop_id:
        products = products.filter(shop_id=shop_id)

    shops = Shop.objects.all()  # Fetch all shops for dropdown selection

    return render(request, 'product_list.html', {'products': products, 'shops': shops})

def all_orders(request):
    if 'admin_id' not in request.session:
        return redirect('admin_login')
    orders = Order.objects.all()
    return render(request, 'shop_orders.html', {'orders': orders})