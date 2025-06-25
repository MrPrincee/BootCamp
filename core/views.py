from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Post
from django.views import View

def fetch_data(model):
    return list(model.objects.all().values())


class HomeView(View):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the polls page.")

class ApiView(View):
    def get(self,request):
        data = {
            "message": "Hello, world. You're at the polls page.",
            "status": "Success"
        }
        return JsonResponse(data)

class PostListView(View):
    def get(self, request):
        return render(request,'post_list.html',{'posts':fetch_data(Post)})



class GetPostView(View):
    def get(self, request):
        return JsonResponse({"posts":fetch_data(Post)})

