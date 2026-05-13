from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    category = []
    trending = False
    offer = False

    if request.user.is_authenticated:
        no_of_cp = CartModel.objects.filter(host=request.user).count()
    else:
        no_of_cp = 0

    # Search Operation:#
    if 'search' in request.GET:
        search = request.GET['search']
        all_products =Products.objects.filter(Q(pname__icontains = search)| Q(pdesc__icontains = search))
        # print(all_products.exists())
        if not all_products.exists():
            return render(request,'home.html',{'msg':True,'search_bar':True})
    # Category :#
    elif 'category' in request.GET:
        c = request.GET['category']
        all_products = Products.objects.filter(pcategory = c)
    #Trending :#
    elif 'trending' in request.GET:
        all_products = Products.objects.filter( trending = True)
        trending = True

    elif 'offer' in request.GET:
        all_products = Products.objects.filter( offer = True)
        offer = True
    else:
        all_products = Products.objects.all()

    # category = []
    a = Products.objects.all()
    for i in a:
        if i.pcategory not in category:
            category+=[i.pcategory]
    return render(request,'home.html',{'all_products':all_products,'category':category,'search_bar':True,'no_of_cp':no_of_cp,'offer':offer,'trending':trending})

@login_required(login_url='login_')
def cart(request):
    # no_of_cp = CartModel.objects.filter(host=request.user).count()
    TA=0
    cartproducts = CartModel.objects.filter(host = request.user)
    # print(cartproducts)
    count = cartproducts.count()
    # print(cartproducts.count())
    for i in cartproducts:
        TA+=i.totalprice
    return render(request,'cart.html',{'cartproducts':cartproducts,'TA':TA,'count':count})

#Increment button in cart :#
def increment(request,id):
    a = CartModel.objects.get(id=id)
    a.quantity+=1
    a.totalprice+=a.price
    a.save()
    return redirect('cart')

#Decrement button in cart :#
def decrement(request,id):
    a = CartModel.objects.get(id=id)
    if a.quantity>1:
        a.quantity-=1
        a.totalprice-=a.price
        a.save()
    else:
        a.delete()
    return redirect('cart')

@login_required(login_url='login_')
def addtocart(request,id):
    product = Products.objects.get(id=id)
    try:
        cp = CartModel.objects.get(pname = product.pname,host = request.user)
        cp.quantity+=1
        cp.totalprice+=cp.price
        cp.save()
    except:
        CartModel.objects.create(
        pimage = product.pimage,
        pname = product.pname,
        price = product.price,
        pcategory = product.pcategory,
        quantity = 1,
        totalprice = product.price,
        host = request.user
    )
    return redirect('home')


@login_required(login_url='login_')
def remove(request,id):
    a = CartModel.objects.get(id=id)
    if a.quantity>1:
        a.quantity-=1
        a.totalprice+=a.price
        a.save()
    else:
        a.delete()
    return redirect('cart')

def support(request):
    return render(request,'support.html')

def knowus(request):
    return render(request,'knowus.html')