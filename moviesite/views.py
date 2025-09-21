from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views import View

from .models import Genre, Movie, Profile
from .forms import MovieForm


class HomeView(ListView):
    model = Movie
    template_name = "moviesite/main.html"
    context_object_name = "movies"
    extra_context = {"title": "Asosiy sahifa"}

    def get_queryset(self):
        return Movie.objects.filter(published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        return context


class AboutView(View):
    def get(self, request: HttpRequest):
        context = {
            "title": "about"
        }
        return render(request, "moviesite/about.html", context)


class MoviesByGenreView(ListView):
    model = Movie
    template_name = "moviesite/main.html"
    context_object_name = "movies"

    def get_queryset(self):
        return Movie.objects.filter(genre_id=self.kwargs["genre_id"], published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = get_object_or_404(Genre, pk=self.kwargs["genre_id"])
        context["genres"] = Genre.objects.all()
        context["title"] = genre.type
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = "moviesite/movie.html"
    context_object_name = "movie"
    pk_url_kwarg = "movie_id"

    def get_queryset(self):
        return Movie.objects.filter(published=True)

    def get_object(self, queryset=None):
        movie = super().get_object(queryset)
        movie.views += 1
        movie.save()
        return movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context


class AddMovieView(CreateView):
    model = Movie
    form_class = MovieForm
    template_name = "moviesite/add_movie.html"

    def form_valid(self, form):
        messages.success(self.request, "Film muvaffaqiyatli qo'shildi!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("movie_detail", kwargs={"pk": self.object.pk})


@permission_required("moviesite.change_movie", raise_exception=True)
def update_movie(request: HttpRequest, movie_id: int):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == "POST":
        form = MovieForm(request.POST, files=request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save()
            messages.success(request, "Film muvaffaqiyatli yangilandi!")
            return redirect("movie_detail", pk=movie.pk)
    else:
        form = MovieForm(instance=movie)

    context = {"form": form, "title": "Filmni yangilash"}
    return render(request, "moviesite/update_movie.html", context)


@permission_required("moviesite.delete_movie", raise_exception=True)
def delete_movie(request: HttpRequest, movie_id: int):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        movie.delete()
        messages.success(request, "Film muvaffaqiyatli o'chirildi!")
        return redirect("main")
    context = {"movie": movie, "title": "Filmni o'chirish"}
    return render(request, "moviesite/delete_movie.html", context)


@login_required(login_url="/login/")
def profile(request: HttpRequest, username: str):
    profile_user = get_object_or_404(User, username=username)
    context = {
        "profile_user": profile_user,
        "title": str(profile_user.username).title() + " profil"
    }
    try:
        profile = Profile.objects.get(user=profile_user)
        context["profile"] = profile
    except Profile.DoesNotExist:
        pass
    return render(request, "profile.html", context)
