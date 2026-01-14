from django.shortcuts import render,redirect
from core.models import Contact,Product,Orders,OrderUpdate
from django .contrib import messages
from math import ceil
from core import keys
# from django.conf import settings
# MERCHANT_KEYS=keys.MK
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from PayTm import Checksum
import razorpay
from django.conf import settings
from django.shortcuts import render
from core.models import Orders
# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .models import Orders, OrderUpdate
def index(request):
    allProds=[]
    catprods = Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides= n // 4 + ceil((n / 4)-(n // 4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds}    
    return render ( request,"index.html",params)
def contact(request):
    if request.method == "POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        if not name or not desc:
            messages.error(request, "Name and description are required.")
            return render(request, "contact.html")
    
        myquery = Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
        myquery.save()
        messages.info(request,"We Will get back to you soon")
        return render(request,"contact.html") 
    return render(request,"contact.html")    

def about(request):
    return render ( request,"about.html")

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
# ✅ Checkout Page (Trigger Payment)
def checkout(request):
    if request.method == "POST":
        # ✅ Capture Form Data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        amount = int(request.POST.get('amount')) * 100  # Convert to Paisa

        # ✅ Step 1: First Create Order in Database (Pending)
        order = Orders.objects.create(
            name=name,
            email=email,
            phone=phone,
            address1=address,
            city=city,
            state=state,
            zip_code=zip_code,
            amount=amount // 100,
            payment_status="Pending"
        )

        # ✅ Step 2: Create Order in Razorpay
        try:
            razorpay_order = client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": "1"
            })

            # ✅ Step 3: Attach Razorpay Order ID to Database
            order.payment_id = razorpay_order['id']
            order.save()

        except Exception as e:
            # ✅ If Payment Fails, Redirect Back
            return redirect('checkout')

        # ✅ Step 4: Send Data to Template
        return render(request, 'checkout.html', {
            'order_id': razorpay_order['id'],
            'amount': amount // 100,
            'name': name,
            'email': email,
            'key': settings.RAZORPAY_KEY_ID
        })

    # ✅ Render Checkout Page Initially
    return render(request, 'checkout.html')


# ✅ Capture Payment After Success
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        response = request.POST

        # ✅ Capture Payment ID and Order ID
        order_id = response.get('razorpay_order_id')
        payment_id = response.get('razorpay_payment_id')

        # ✅ Step 1: Find the Order in Database
        order = Orders.objects.get(payment_id=order_id)

        # ✅ Step 2: Mark Payment As Completed
        order.payment_status = 'Paid'
        order.payment_id = payment_id
        order.save()

        # ✅ Step 3: Create Order Update
        OrderUpdate.objects.create(
            order_id=order.order_id,
            update_desc="Your order has been successfully placed!"
        )

        # ✅ Step 4: Return Success Response
        return JsonResponse({'status': 'Payment Successful'})

    # ✅ If Payment Fails
    return JsonResponse({'status': 'Payment Failed'})
