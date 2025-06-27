from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from django.views import View

from django.db import transaction, connection


from collections import Counter


def fetch_data(model):
    return list(model.objects.all().values())


def get_all_posts(film_id):
    film = Film.objects.get(id=film_id)
    return list(film.post_set.all().values())

@transaction.atomic
def add_film_and_posts(film_data,post_data):
    if Film.objects.filter(title=film_data['title']).exists():
        return None
    film = Film.objects.create(**film_data)
    post_data['film'] = film
    post = Post.objects.create(**post_data)
    return film, post

def most_popular_film_id():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT film_id from core_post
        """)
        result = cursor.fetchall()
        film_ids = [row[0] for row in result]
        most_popular_film_id = Counter(film_ids).most_common(1)[0][0]
        cursor.close()
    return most_popular_film_id



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


class GetFilmPosts(View):
    def get(self,request,film_id):
        return JsonResponse({"posts":get_all_posts(film_id)})


class CreateTestData(View):
    def get(self, request):
        return self.post(request)
    def post(self,request):
        film_data = {
            'title': 'Inception2',
            'content': 'A mind-bending sci-fi thriller.'
        }

        post_data = {
            'title': 'Great Movie!',
            'content': 'Inception is one of the best films ever.'
        }

        test_data = add_film_and_posts(film_data,post_data)
        if test_data:
            return JsonResponse({
                'film_id': test_data[0].id,
                'film_title': test_data[0].title,
                'post_id': test_data[1].id,
                'post_title': test_data[1].title,
        })
        else:
            return JsonResponse({"Info":"This Film already exists!"})


class MostPopularFilmsView(View):
    def get(self, request):
        film_name = Film.objects.get(id=most_popular_film_id()).title
        return JsonResponse(
            {
                "Most Popular Film":film_name
            }
        )

