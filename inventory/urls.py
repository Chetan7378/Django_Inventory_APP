from django.urls import path
from . import views

urlpatterns = [
    # Shop URLs
    path('shop/register/', views.shop_register, name='shop_register'),
    path('shop/login/', views.shop_login, name='shop_login'),
    path('shop/dashboard/addproduct/', views.add_product, name='add_product'),
    path('shop/dashboard/editproduct/<int:p_id>/', views.edit_product, name='edit_product'),
    path('shop/dashboard/deleteproduct/<int:p_id>/', views.delete_product, name='delete_product'),
    path('shop/dashboard/', views.shop_dashboard, name='shop_dashboard'),
    path('shop/logout/', views.shop_logout, name='shop_logout'),
    path('shop/orders/',views.shop_orders,name="shop_orders"),
    # path('shop/getAddProductForm/add_product/', views.add_product, name='add_product'),
    # path('shop/getAddProductForm/', views.getAddProductForm, name='getAddProductForm'),
    # path('shop/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    # path('shop/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),


    # Customer URLs
    path('customer/register/', views.customer_register, name='customer_register'),
    path('customer/login/', views.customer_login, name='customer_login'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/logout/', views.customer_logout, name='customer_logout'),
    path("customer/add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("customer/cart/", views.view_cart, name="view_cart"),
    path("customer/checkout/", views.checkout, name="checkout"),
    path('customer/add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('customer/orders/', views.customer_orders, name='customer_orders'),
    
    path('products/', views.product_list, name='product_list'),
    # path('customer/order/<int:order_id>/', views.customer_order, name='customer_order'),
    # path('customer/order/cancel/<int:order_id>/', views.customer_cancel_order, name='customer_cancel_order'),

    # Admin URLs
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/addorders',views.all_orders,name="all_orders"),
]
urlpatterns += [
    # Order Management
    path('order/place/<int:product_id>/', views.place_order, name='place_order'),
    path('customer/orders/', views.customer_orders, name='customer_orders'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),

    # Shop Order Management
    path('shop/orders/', views.shop_orders, name='shop_orders'),
    path('order/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path("",views.mainPage,name="mainPage"),

]
# Compare this snippet from inventory_project/inventory/views.py:
# # Shop Dashboard (View Products & Orders)
# def shop_dashboard(request):
#     if 'shop_id' not in request.session:
#         return redirect('shop_login')
#
#     shop = Shop.objects.get(s_id=request.session['shop_id'])
#     products = Product.objects.filter(shop=shop)
#     orders = Order.objects.filter(shop=shop)
#     return render(request, 'shop_dashboard.html', {'shop': shop, 'products': products, 'orders': orders})
#
# # Shop Logout View
# def shop_logout(request):     logout(request)
#     return redirect('shop_login')     # Customer Registration View
# def customer_register(request):