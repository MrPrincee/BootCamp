from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Post


def home_view(request):
    return  HttpResponse("Hello, world. You're at the polls page.")
#test
def api_view(request):
    data = {
        "message": "Hello, world. You're at the polls page.",
        "status":"Success"
    }
    return JsonResponse(data)

def post_list_view(request):
    posts = Post.objects.all()
    return render(request,'post_list.html',{'posts':posts})



