from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.reverse import reverse

from api.models import Order


@login_required(login_url='/admin/login/')
def index(request):
    return render(request, 'dashboard.html')


@login_required(login_url='/admin/login/')
def get_orders(request):
    orders = Order.objects.all()
    return render(request, 'orders.html', context={'orders': orders})


@login_required(login_url='/admin/login/')
def get_order(request, pk):
    order = Order.objects.get(pk=pk)
    return render(request, 'order.html', context={'order': order})


@csrf_exempt
def available_in_warehouse(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.warehouse_confirmation = True
    order.save()
    return HttpResponseRedirect(reverse('order', [order_id]))


@csrf_exempt
def deliver(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delivered = True
    order.save()
    return HttpResponseRedirect(reverse('order', [order_id]))


@csrf_exempt
def enable_return(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.returned = True
    order.save()
    return HttpResponseRedirect(reverse('order', [order_id]))


@csrf_exempt
def disable_return(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.returned = False
    order.save()
    return HttpResponseRedirect(reverse('order', [order_id]))
