from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from .models import Genre, Movie, Profile
from .forms import MovieForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.views import View


# Create your views here.

def main(request: HttpRequest):
    messages.info(request, "Xush kelibsiz! Asosiy sahifasidasiz.")
    genres = Genre.objects.all()
    movies = Movie.objects.filter(published=True)

    context = {
        'genres': genres,
        'movies': movies,
        'title': 'main',
    }

    return render(request, 'moviesite/main.html', context)

def about(request: HttpRequest):
    context = {
        'title': 'about',
    }

    return render(request, 'moviesite/about.html', context)

def by_genre(request: HttpRequest, genre_id):
    movies = Movie.objects.filter(genre_id=genre_id, published=True)
    genres = Genre.objects.all()
    genre = get_object_or_404(Genre, pk=genre_id)

    context = {
        'movies': movies,
        'genres': genres,
        'title': genre.type,
    }

    return render(request, 'moviesite/main.html', context)

@login_required(login_url='/login/')
def by_movie(request: HttpRequest, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id, published=True)

    movie.views += 1
    movie.save()

    context = {
        'movie': movie,
        'title': movie.title,
    }

    return render(request, 'moviesite/movie.html', context)

# POST
@permission_required('moviesite.add_movie', raise_exception=True)
def add_movie(request: HttpRequest):
    if request.user.is_staff:
        if request.method == 'POST':
            form = MovieForm(request.POST, files=request.FILES)
            if form.is_valid():
                movie = form.save()
                messages.success(request, "Maqola muvaffaqiyatli qo'shildi!")
                return redirect("by_movie", movie_id=movie.pk)
            else:
                messages.error(request, "Ma'lumotlar qo'shishda xatolik yuz berdi!")
        else:
            form = MovieForm()

        context = {
            "form": form,
            "title": "Film qo'shish"
        }
        return render(request, 'moviesite/add_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')
    
# UPDATE
@permission_required("moviesite.change_moviesite")
def update_movie(request: HttpRequest, movie_id: int):
    if request.user.is_staff:
        movie = get_object_or_404(Movie, pk=movie_id)

        if request.method == 'POST':
            form = MovieForm(request.POST, files=request.FILES, instance=movie)
            if form.is_valid():
                movie = form.save()
                messages.success(request, "Film muvaffaqiyatli yangilandi!")
                return redirect("by_movie", movie_id=movie.pk)
            else:
                messages.error(request, "Ma'lumotlar qo'shishda xatolik yuz berdi!.")
        else:
            form = MovieForm(instance=movie)

        context = {
            "form": form,
            "title": "Filmni yangilash"
        }
        return render(request, 'moviesite/update_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')
    
# DELETE
@permission_required("moviesite.delete_moviesite")
def delete_movie(request: HttpRequest, movie_id):
    if request.user.is_staff:
        movie = get_object_or_404(Movie, pk=movie_id)
        messages.warning(request, "Filmni o'chirmoqchimisiz?")
        if request.method == 'POST':
            movie.delete()
            messages.success(request, "Film muvaffaqiyatli o'chirildi!")
            return redirect("main")
        context = {
            'movie': movie,
            'title': "Filmni o'chirish"
        }
        return render(request, 'moviesite/delete_movie.html', context)
    else:
        messages.error(request, "Sizda ruxsat yo‘q!")
        return render(request, '404.html')


login_required(login_url='/login/')
def profile(request: HttpRequest, username: str):
    profile_user = get_object_or_404(User, username=username)

    context = {
        'profile_user': profile_user,
        'title': str(profile_user.username).title() + "profil"
    }

    try:
        profile = Profile.objects.get(user=profile_user)
        context["profile"] = profile
    except:
        pass

    return render(request, 'profile.html', context)

class MainView(View):
    def get(self, request):
        context = {
            "title": "Asosiy sahifa",
            "welcome": "Hush kelibsiz",
        }
        return render(request, 'moviesite/main.html', context)


def movie_detail(request: HttpRequest, movie_id: int):
    genres  = Genre.objects.all()
    movie = get_object_or_404(Movie, pk=movie_id)

    context = {
        'genres': genres,
        'movie': movie,
        'title': str(movie.title).title(),
    }

    return render(request, 'moviesite/movie_detail.html', context)