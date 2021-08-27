from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from App_Order.models import Cart, Order
from App_Shop.models import Product
from django.contrib import messages
# Create your views here.

@login_required
def add_to_cart(request, pk):
     item = get_object_or_404(Product, pk=pk)
     order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased = False)
     order_qs = Order.objects.filter(user=request.user, ordered=False)   #checking if there is any previous order

     if order_qs.exists():
         order = order_qs[0]
         if order.orderitems.filter(item=item).exists():        #if any item exists in previious order
             order_item = order_item[0]
             # order_item.quantity += 1                #if so, increase quantity
             messages.info(request, "This item has already been added to your cart.")
             return redirect('App_Shop:home')
         else:
             order.orderitems.add(order_item[0])
             item.product_quantity-=1
             item.save()
             messages.info(request, "Product is added to your cart.")
             return redirect("App_Shop:home")
     else:
          order = Order(user=request.user)
          order.save()
          order.orderitems.add(order_item[0])
          item.product_quantity-=1
          item.save()
          messages.info(request, "Product is added to your cart.")
          return redirect("App_Shop:home")

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'App_Order/cart.html', context={'carts':carts, 'order':order})
    else:
        messages.warning(request, "No items in the car!")
        return redirect("App_Shop:home")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            item.product_quantity+=order_item.quantity
            item.save()
            messages.warning(request, "This item has been removed from your cart!")
            return redirect("App_Order:cart")
        else:
            messages.info(request, "This item is not found in your cart")
            return redirect(request, "App_Shop:home")
    else:
        messages.info(request, "You don't have any active order!")
        return redirect("App_Shop:home")

@login_required
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            if item.product_quantity==0:
                messages.warning(request, f"Sorry, we don't have any more '{item.name}' in stock.")
                return redirect("App_Order:cart")
            elif order_item.quantity >=1:
                order_item.quantity +=1
                item.product_quantity-=1            #for decreasign the quantity from total stock
                order_item.save()
                item.save()                         #for saving the current stock
                messages.info(request, f"The quantity of '{item.name}' has been updated.")
                return redirect("App_Order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart.")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have any active order!")
        return redirect("App_Shop:home")

@login_required
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item = order_item[0]
            if order_item.quantity >1:
                order_item.quantity -=1
                order_item.save()
                item.product_quantity+=1
                item.save()
                messages.info(request, f"The quantity of '{item.name}' has been updated.")
                return redirect("App_Order:cart")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                item.product_quantity+=1
                item.save()
                messages.info(request, f"{item.name} has been removed.")
                return redirect("App_Order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart.")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have any active order!")
        return redirect("App_Shop:home")
