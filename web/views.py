from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, Avg, F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout

from web.forms import RegistrationForm, AuthForm, PetForm, PostForm, PostFilterForm
from web.models import Pet, Post
from web.services import filter_posts

User = get_user_model()


@login_required
def main_view(request):
    posts = Post.objects.all().order_by('-post_date')

    filter_form = PostFilterForm(request.GET)
    filter_form.is_valid()
    posts = filter_posts(posts, filter_form.cleaned_data)

    total_count = posts.count()
    posts = posts.prefetch_related("pets").select_related("user")
    page_number = request.GET.get("page", 1)
    paginator = Paginator(posts, per_page=10)

    return render(request, 'web/main.html', {
        "posts": paginator.get_page(page_number),
        "user": request.user,
        "total_count": total_count,
        "filter_form": filter_form
    })


@login_required
def analytics_view(request):
    overall_stat = Post.objects.exclude(opened=False).aggregate(
        count=Count("id"),
        max_date=Max("end_date"),
        min_date=Min("start_date"),
        avg_time=Avg(F("end_date") - F("start_date")),
        avg_price=Avg("price"),
        avg_pets_num=Avg("pets")
    )

    days_stat = (
        Post.objects.exclude(opened=False)
        .annotate(days_num=F("end_date") - F("start_date"))
        .values("days_num")
        .annotate(
            count=Count("id"),
            avg_price=Avg("price"),
            avg_pets_num=Avg("pets")
        )
        .order_by('days_num')
    )

    return render(request, "web/analytics.html", {
        "overall_stat": overall_stat,
        "days_stat": days_stat
    })


def registration_view(request):
    form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, "web/registration.html", {"form": form, "is_success": is_success})


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                return redirect("main")
    return render(request, "web/auth.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("main")


@login_required
def pet_edit_view(request, id=None):
    pet = get_object_or_404(Pet, user=request.user, id=id) if id is not None else None
    form = PetForm(instance=pet)
    if request.method == 'POST':
        form = PetForm(data=request.POST, files=request.FILES, instance=pet, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("pets_add")
    return render(request, "web/pet_form.html", {"form": form})


@login_required
def profile_view(request):
    user = request.user
    items = Pet.objects.filter(user=user)
    return render(request, "web/profile.html", {"items": items, "user": user})


@login_required
def post_edit_view(request, id=None):
    post = Post.objects.get(id=id) if id is not None else None

    if request.user.id != post.user.id:
        return render(request, "web/post.html", {"post": post})

    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=post, initial={"user": request.user})
        if form.is_valid():
            form.save()
            return redirect("main")
    return render(request, "web/post_form.html", {"form": form})


@login_required
def post_delete_view(request, id):
    post = get_object_or_404(Post, user=request.user, id=id)
    post.delete()
    return redirect('main')
