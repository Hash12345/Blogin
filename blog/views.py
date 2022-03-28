from ast import Param
from django.shortcuts import render
from django.http import JsonResponse
from .serializers import PostSerailizer
from .models import Post
import json
import requests

# Create your views here.
def home(request):
    posts=Post.objects.order_by('-created_at')
    context={
        'posts': posts,
        'count_posts':posts.count()
    }
    return render(request, 'home.html', context)
def search_post(request):
    if request.method == 'POST':
        text=request.POST.get('text')
        posts=Post.objects.filter(title__contains=text)
        serializer=PostSerailizer(posts, many=True)
        return JsonResponse({'success': True, 'posts': serializer.data})

def all_posts(request):
    posts=Post.objects.all()
    serializer=PostSerailizer(posts, many=True )
    return JsonResponse({'success': True, 'posts': serializer.data})
def create_post(request):
    serializer= PostSerailizer(data={'title':request.POST.get('title'), 'body': request.POST.get('body')})
    serializer.is_valid(raise_exception=True)
    post=serializer.save()    
    return JsonResponse({
        'success':True,
        'message':'Post Created Successfully',
        'post': serializer.data
    })
def show_post(request, id):
    post=Post.objects.filter(id=id).first()
    if post is not None:
        serializer= PostSerailizer(instance=post)
        return JsonResponse({                
            'success':True,                
            'post': serializer.data        
        })        
    else:
        return JsonResponse({
            'success':False,
            'message':'Post doesnot exist.',
        }) 
def update_post(request, id):
    post=Post.objects.filter(id=id).first()
    if post is not None:
        serializer= PostSerailizer(instance=post, data={'title':request.POST.get('edit_title'), 'body': request.POST.get('edit_body')})
        #serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, 400)
        post=serializer.save()    
        return JsonResponse({                
            'success':True,   
            'message':'Post Updated Successfully',             
            'post': serializer.data        
        })        
    else:
        return JsonResponse({
            'success':False,
            'message':'Post doesnot exist.',
        })  
def delete_post(request, id):
    post=Post.objects.filter(id=id).first()
    if post is not None:
        id =post.id
        post.delete()
        return JsonResponse({                
            'success':True,   
            'message':'Post deleted Successfully',             
            'id': id       
        })        
    else:
        return JsonResponse({
            'success':False,
            'message':'Post doesnot exist.',
        })       
def bitcoin_USD(request):
    """
        1. fetch last 30 days bitcoint-USD exchange rate from bitstamp
        2. display the data in 2 charts
        3. chart 1 displays last 7 days high and low ohlc value
        4. chart 2 displays last 30 days close ohlc value
    """
    pair="btcusd"
    url=f'https://www.bitstamp.net/api/v2/ohlc/{pair}/'
    parameters={
        'step': '86400',
        'limit':'30',
    }
    res =requests.get(url, params=parameters)    
    closes=[]
    for result in res.json()['data']['ohlc']:
        closes.append(float(result['close']))
    ave=sum(closes)/len(closes)
    last_week=res.json()['data']['ohlc'][0:7]
    #create a variable to hold each day high and low value
    high=[]
    low=[]
    for result in last_week:
        high.append(float(result['high']))
        low.append(float(result['low']))
    weekly_max=max(high)
    weekly_min=max(low)
    difference=weekly_max - weekly_min
    return render(request, 'bitcoin-usd.html', {'closings':closes,
                    'average': round(ave, 2),
                    'high': high,
                    'low': low,
                    'weekly_max': round(weekly_max, 2),
                    'weekly_min': round(weekly_min, 2),
                    'difference': round(difference, 2)})
