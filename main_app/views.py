from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Service, Testimonial, ServiceRequest, FAQ


# ===============================
# الصفحات العامة
# ===============================

def index(request):
    services = Service.objects.all()[:12]
    testimonials = Testimonial.objects.all()[:4]
    faqs = FAQ.objects.all()

    return render(request, 'index.html', {
        'services': services,
        'testimonials': testimonials,
        'faqs': faqs,
    })


def services(request):
    all_services = Service.objects.all()

    category = request.GET.get('category')
    search = request.GET.get('search')

    if category:
        all_services = all_services.filter(category=category)

    if search:
        all_services = all_services.filter(name__icontains=search)

    categories = Service.objects.values_list('category', flat=True).distinct()

    return render(request, 'services.html', {
        'services': all_services,
        'categories': categories,
        'selected_category': category,
        'search': search,
    })


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    related_services = Service.objects.filter(
        category=service.category
    ).exclude(id=service.id)[:4]

    return render(request, 'service_detail.html', {
        'service': service,
        'related_services': related_services,
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        ServiceRequest.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            service=request.POST.get('service'),
            message=request.POST.get('message'),
        )
        return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')


# ===============================
# السلة (Cart)
# ===============================

def cart(request):
    cart = request.session.get('cart', {})
    services = Service.objects.filter(id__in=cart.keys())

    items = []
    total = 0

    for service in services:
        quantity = cart[str(service.id)]
        price = service.discount_price if service.discount_price else service.price
        subtotal = float(price) * quantity
        total += subtotal

        items.append({
            'service': service,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {
        'items': items,
        'total': total,
    })


def add_to_cart(request, service_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        service_id = str(service_id)
        quantity = int(request.POST.get('quantity', 1))

        cart[service_id] = cart.get(service_id, 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'cart_count': sum(cart.values())
        })

    return JsonResponse({'success': False})


def remove_from_cart(request, service_id):
    cart = request.session.get('cart', {})
    service_id = str(service_id)

    if service_id in cart:
        del cart[service_id]
        request.session.modified = True

    return JsonResponse({
        'success': True,
        'cart_count': sum(cart.values())
    })


def update_cart(request, service_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        service_id = str(service_id)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart[service_id] = quantity
        else:
            cart.pop(service_id, None)

        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'cart_count': sum(cart.values())
        })

    return JsonResponse({'success': False})


def checkout(request):
    if request.method == 'POST':
        request.session['cart'] = {}
        request.session.modified = True
        return JsonResponse({'success': True})

    return render(request, 'checkout.html')


def get_cart_count(request):
    cart = request.session.get('cart', {})
    return JsonResponse({'count': sum(cart.values())})


# ===============================
# الإدارة (Admin Views)
# ===============================

def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def add_service(request):
    if request.method == 'POST':
        Service.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            discount_price=request.POST.get('discount_price') or None,
            category=request.POST.get('category'),
            is_featured=bool(request.POST.get('is_featured'))
        )
        return redirect('services')

    return render(request, 'admin/add_service.html')
