import datetime
import json
import random
import uuid

from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from quot_app.models import userlogin,  UOM , Company , Customer, Item
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST

from . import models
from .forms import CustomerForm
from .models import Quot


def index(request):
    return render(request,"index.html")
def successPage(request):
    return render(request,'successPage.html')
def home(request):
    return render(request,"home.html")
def quotation(request):
    return render(request,"addquotation.html")


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login the user
            login(request, user)
            # Redirect to a success page or dashboard
            return redirect('index')  # Replace 'dashboard' with your actual URL name
        else:
            # Handle invalid login
            return render(request, 'home.html', {'error_message': 'Invalid username or password.'})

    # If it's not a POST request, render the initial form or page
    return render(request, 'userlogin.html')



def uom(request):
    if request.method == "POST":
        uom=request.POST.get('uom')

        UOM.objects.create(
            uom=uom)
    return render(request, 'UOM.html')


def company(request):
    if request.method == "POST":
        companyName = request.POST.get('companyName')
        printCompanyName = request.POST.get('company')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        address3 = request.POST.get('address3')
        address4 = request.POST.get('address4')
        pincode = request.POST.get('pincode')
        contact = request.POST.get('contact')
        gstRegType = request.POST.get('gstRegType')
        salesEntry = request.POST.get('salesEntry')
        saleInclusive = request.POST.get('saleInclusive')
        blankSaleItems = request.POST.get('blankSaleItems')
        makeRoundOff = request.POST.get('makeRoundOff')
        showDiscount = request.POST.get('showDiscount')
        showGstDetails = request.POST.get('showGstDetails')
        gstIn=request.POST.get('gstIn')


        Company.objects.create(
                companyName=companyName,
                printCompanyName=printCompanyName,
                address1=address1,
                address2=address2,
                address3=address3,
                address4=address4,
                pincode=pincode,
                contact=contact,
                gstRegType=gstRegType,
                salesEntry=salesEntry,
                saleInclusive=saleInclusive,
                blankSaleItems=blankSaleItems,
                makeRoundOff=makeRoundOff,
                showDiscount=showDiscount,
                showGstDetails=showGstDetails,
                 gstIn=gstIn)


        # Redirect to the same page to avoid form resubmission
        return redirect('company')

    else:
        # If it's a GET request, render the empty form
        companies = Company.objects.all()  # Fetch all existing companies for displaying in the table
        context = {'companies': companies}
        return render(request, 'company.html', context)

def delete_company(request,id):
    # Handle deletion of a company
    company = get_object_or_404(Company, pk=id)
    if request.method == 'POST':
        company.delete()
        return redirect('company')

    # If the request method is not POST (e.g., GET), redirect back to the list
    return redirect('company')

def delete_quotation(request,id):
    # Handle deletion of a company
    quot = get_object_or_404(Quot, pk=id)
    if request.method == 'POST':
        quot.delete()
        return redirect('company')

    # If the request method is not POST (e.g., GET), redirect back to the list
    return redirect('company')



def customer(request):
    if request.method == "POST":
        customerName = request.POST.get('customerName')
        companyName = request.POST.get('companyName')
        email = request.POST.get('email')
        gstin = request.POST.get('gstin')
        phoneNumber = request.POST.get('phoneNumber')
        country = request.POST.get('country')
        state=request.POST.get('state')
        address = request.POST.get('address')
        gstRegType=request.POST.get('gstRegType')

        Customer.objects.create(
            customerName=customerName,
            companyName=companyName,
            email=email,
            gstin=gstin,
            phoneNumber=phoneNumber,
            country=country,
            state=state,
            address=address,
            gstRegType= gstRegType
        )

        return redirect('customer_list')
    return render(request, 'customer.html')

def customer_list(request):
        data = Customer.objects.all()
        return render(request, 'customer_list.html', {'data': data})


def edit_customer(request, pk):
    rdata = get_object_or_404(Customer, id=pk)
    if request.method == "POST":
        companyName = request.POST.get('t1')
        gstRegType = request.POST.get('t2')
        Customer.objects.filter(id=pk).update(
            companyName=companyName,
            gstRegType=gstRegType
        )
        base_url = reverse('customer_list')
        return redirect(base_url)
    return render(request, 'edit_customer.html', {'rdata': rdata})

def edit_company(request, pk):
    data = get_object_or_404(Company, id=pk)
    if request.method == "POST":
        companyName = request.POST.get('v1')
        gstRegType = request.POST.get('v2')
        Company.objects.filter(id=pk).update(
            companyName=companyName,
            gstRegType=gstRegType
        )
        base_url = reverse('company_list')
        return redirect(base_url)
    return render(request, 'edit_company.html', {'data': data})

def delete_customer(request, customer_id):
    # Handle deletion of a company
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')

    # If the request method is not POST (e.g., GET), redirect back to the list
    return redirect('customer_list')

def item(request):
    if request.method == "POST":
        itemid=request.POST.get('itemid')
        itemName = request.POST.get('itemName')
        hsnCode = request.POST.get('hsnCode')
        uom = request.POST.get('uom')
        isGoodOrService = request.POST.get('isGoodOrService')
        ratePerUnit = request.POST.get('ratePerUnit')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        totalGstPercent = request.POST.get('totalGstPercent')
        sgstPercent = request.POST.get('sgstPercent')
        cgstPercent= request.POST.get('cgstPercent')
        igstPercent= request.POST.get('igstPercent')

        Item.objects.create(
            itemid=itemid,
            itemName=itemName,
            hsnCode=hsnCode,
            uom=uom,
            isGoodOrService=isGoodOrService,
            ratePerUnit=ratePerUnit,
            quantity=quantity,
            description=description,
            totalGstPercent=totalGstPercent,
            cgstPercent=cgstPercent,
            sgstPercent=sgstPercent,
            igstPercent=igstPercent)

        return redirect('item_list')

    else:
        # If it's a GET request, render the empty form
        items = Item.objects.all()  # Fetch all existing companies for displaying in the table
        context = {'items': items}
        return render(request, 'item.html', context)

def item_list(request):
    data=Item.objects.all()
    return render(request,'item_list.html',{'data':data})
def edit_item(request, pk):
    rdata = get_object_or_404(Item, id=pk)
    if request.method == "POST":
        itemName = request.POST.get('t1')
        hsnCode = request.POST.get('t2')
        Item.objects.filter(id=pk).update(
            itemName=itemName,
            hsnCode=hsnCode
        )
        base_url = reverse('item_list')
        return redirect(base_url)
    return render(request, 'edit_item.html', {'rdata': rdata})





def delete_item(request, item_id):
    # Handle deletion of a company
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')

    # If the request method is not POST (e.g., GET), redirect back to the list
    return redirect('item_list')

from django.http import JsonResponse
 # Adjust import based on your project structure


def uom(request):
    if request.method == "POST":
        uom= request.POST.get('uom_list')

        UOM.objects.create(
            uom=uom
        )

        return redirect('UOM')

    else:
        # If it's a GET request, render the empty form
        uoms = UOM.objects.all()  # Fetch all existing companies for displaying in the table
        context = {'uoms': uoms}
        return render(request, 'UOM.html', context)

def uom_list(request):
    data=Item.objects.all()
    return render(request,'item_list.html',{'data':data})


def customer_name(request):
    cName=Customer.objects.all()
    return render(request,'addquotation.html',{'cName':cName})
  # Use this decorator if CSRF token verification is not required



@csrf_exempt  # Use this decorator if CSRF token verification is not required
def fetch_customer_data(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customerName')  # Assuming 'customerName' is sent via POST

        try:
            customer = Customer.objects.get(customerName=customer_name)  # Adjust based on your model field
            data = {
                'companyName': customer.companyName,
                'email': customer.email,
                'gstRegType': customer.gstRegType,
                'gstin':customer.gstin,
                'phoneNumber': customer.phoneNumber,
                'country': customer.country,
                'state':customer.state,
                'address': customer.address,
            }
            print(f"Data fetched: {data}")
            return JsonResponse(data)
        except Customer.DoesNotExist:
            print("Customer not found")
            return JsonResponse({'error': 'Customer not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def fetch_item_data(request):
    item_name = request.POST.get('itemName')
    items = Item.objects.filter(itemName=item_name)
    if items.exists():
        item = items.first()
        data = {
            'hsnCode': item.hsnCode,
            'quantity':item.quantity,
            'ratePerUnit': item.ratePerUnit,
            'totalGstPercent': item.totalGstPercent,
            'sgstPercent': item.sgstPercent,
            'cgstPercent': item.cgstPercent,
            'igstPercent': item.igstPercent,
            'uom':item.uom,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Item not found'})

def fetch_item_names(request):
    if request.method == 'GET':
        term = request.GET.get('q', '')
        items = Item.objects.filter(Q(itemName__icontains=term)).values_list('itemName', flat=True).distinct()
        return JsonResponse(list(items), safe=False)
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt  # Adding csrf_exempt for simplicity; ensure CSRF protection is handled appropriately in production
def save_purchase_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])

            # Generate a unique quot_number
            quot_number = random.randint(111111, 999999)

            # Save customer details from the received data
            customer_name = data.get('customerName')
            company_name = data.get('companyName')
            email = data.get('email')
            gst_reg_type = data.get('gstRegType')
            gstin = data.get('gstin')
            phone_number = data.get('phoneNumber')
            address = data.get('address')
            country = data.get('country')
            state = data.get('state')

            quotation_entries = []
            for item in items:
                # Create a new Quotation entry for each item
                quotation_entry = Quot(
                    customerName=customer_name,
                    companyName=company_name,
                    email=email,
                    gstRegType=gst_reg_type,
                    gstin=gstin,
                    phoneNumber=phone_number,
                    address=address,
                    country=country,
                    state=state,
                    itemName=item.get('itemName'),
                    hsnCode=item.get('hsnCode'),
                    ratePerUnit=item.get('ratePerUnit'),
                    quantity=item.get('quantity'),
                    totalGstPercent=item.get('totalGstPercent'),
                    sgstPercent=item.get('sgstPercent'),
                    cgstPercent=item.get('cgstPercent'),
                    igstPercent=item.get('igstPercent'),
                    quot_Number=quot_number,
                    uom=item.get('uom'),
                )
                quotation_entries.append(quotation_entry)

            # Bulk insert the quotation entries to improve performance
            Quot.objects.bulk_create(quotation_entries)

            # Return the quot_number in the response
            return JsonResponse({'quot_number': quot_number})

        except Exception as e:
            # Handle exceptions and errors appropriately
            print(f"Error saving quotation: {str(e)}")
            return JsonResponse({'error': 'Error saving quotation. Please try again.'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)



def receipt_view(request, quot_Number):
    # Fetch company details
    companies = Company.objects.all()

    # Fetch quotation details
    quotations = Quot.objects.filter(quot_Number=quot_Number)

    subtotal = 0
    total_gst = 0

    # Calculate total for each quotation item and accumulate subtotal and total GST
    for quotation in quotations:
        # Calculate total for this quotation item
        quotation.total = quotation.quantity * quotation.ratePerUnit

        # Accumulate subtotal
        subtotal += quotation.total

        # Calculate GST amount for this quotation item
        gst_amount = (quotation.totalGstPercent / 100) * quotation.total

        # Accumulate total GST
        total_gst += gst_amount

        # Update the quotation object with GST amount
        quotation.gst_amount = gst_amount

    # Calculate grand total (subtotal + total GST)
    grand_total = subtotal + total_gst

    context = {
        'companies': companies,
        'quotations': quotations,
        'subtotal': subtotal,
        'total_gst': total_gst,
        'grand_total': grand_total,
    }

    return render(request, 'receipt.html', context)


def Quotation_list(request):
    data = Quot.objects.all()
    return render(request, 'Quotation_list.html', {'data': data})

def edit_Quotation(request, pk):
    data = get_object_or_404(Quot, id=pk)
    if request.method == "POST":
        companyName = request.POST.get('q1')
        gstRegType = request.POST.get('q2')
        Quot.objects.filter(id=pk).update(
            companyName=companyName,
            gstRegType=gstRegType
        )
        base_url = reverse('Quotation_list')
        return redirect(base_url)
    return render(request, 'edit_quotation.html', {'data': data})

def company_list(request):
        data = Company.objects.all()
        return render(request, 'company_list.html', {'data': data})