from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Item, OrderItem, Order


class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = "home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity updated.")
            return redirect("core:item-detail", slug=slug)
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("core:item-detail", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:item-detail", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed to your cart.")
            return redirect("core:item-detail", slug=slug)
        else:
            # add a message user does not have order
            messages.info(request, "This item was not in your cart.")
            return redirect("core:item-detail", slug=slug)
    else:
        # add a message user does not have order
        messages.info(request, "You do not have an active order.")
        return redirect("core:item-detail", slug=slug)



def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "item-list.html", context)


def checkout(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "checkout-page.html", context)


def product(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "product-page.html", context)