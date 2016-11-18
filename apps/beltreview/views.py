from django.shortcuts import render, redirect, reverse
from . import models
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "beltreview/index.html")

def register(request):
    if ("first_name" not in request.POST):
        messages.error(request, "Please log in or register!")
        return redirect(reverse("index"))
    else:
        request.session['first_name'] = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        registered = models.User.objects.register(request, request.session['first_name'], last_name, email, password, confirm)
        if (registered):
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            query = models.User(first_name = request.session['first_name'], last_name = last_name, email = email, password_hash = hashed)
            query.save()
            request.session['user'] = query.pk
            return redirect(reverse("home"))
        else:
            return redirect(reverse("index"))

def login(request):
    if ("email" not in request.POST):
        messages.error(request, "Please log in or register!")
        return redirect(reverse("index"))
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = models.User.objects.all().get(email = email)
        if bcrypt.hashpw(password.encode(), user.password_hash.encode()) == user.password_hash.encode():
            request.session['first_name'] = user.first_name
            request.session['user'] = user.pk
            return redirect(reverse("home"))
        else:
            messages.error(request, "Unable to log in!")
            return redirect(reverse("index"))

def add(request):
    authors = models.Author.objects.all()
    context = {
        'authors' : authors
    }
    return render(request, "beltreview/new.html", context)

def create(request):
    title = request.POST["title"]
    author = request.POST["author"]
    review = request.POST["review"]
    stars = request.POST["stars"]
    author_split = author.split(" ")
    first_name = author_split[0]
    last_name = author_split[1]
    author_query = models.Author(first_name = first_name, last_name = last_name)
    author_query.save()
    book_query = models.Book(author = author_query, title = title)
    book_query.save()
    user_query = models.User.objects.all().get(pk = request.session['user'])
    review = models.Review(content = review, book = book_query, stars = stars, reviewer = user_query)
    review.save()
    return redirect(reverse("display", kwargs={'book_id': book_query.pk }))

def display(request, book_id):
    book = models.Book.objects.all().get(pk = book_id)
    author = book.author.first_name + " " + book.author.last_name
    reviews = models.Review.objects.all().filter(book = book_id)
    context = {
        'book_id' : book_id,
        'title' : book.title,
        'author' : author,
        'reviews' : reviews
    }
    return render(request, "beltreview/display.html", context)

def delete(request):
    review_id = request.POST['review_id']
    return redirect(reverse("destroy", kwargs={'review_id': review_id}))

def destroy(request, review_id):
    review = models.Review.objects.all().get(pk = review_id)
    book_id = review.book.pk
    review.delete()
    return redirect(reverse("display", kwargs={'book_id': book_id }))

def add_review(request):
    book_id = request.POST["book_id"]
    review_content = request.POST["review"]
    stars = request.POST["stars"]
    user_query = models.User.objects.all().get(pk = request.session['user'])
    book =  models.Book.objects.all().get(pk = book_id)
    review_query = models.Review(content = review_content, book = book, stars = stars, reviewer = user_query)
    review_query.save()
    return redirect(reverse("display", kwargs={'book_id': book_id }))

def display_user(request, user_id):
    user = models.User.objects.all().get(pk = user_id)
    total_reviews = user.reviewed.count()
    reviews = models.Review.objects.all().filter(reviewer__pk = user_id)
    context = {
        'user' : user,
        'total_reviews' : total_reviews,
        'reviews' : reviews
    }
    return render(request, "beltreview/display_user.html", context)

def logout(request):
    request.session['user'] = ''
    request.session['first_name'] = ''
    return redirect(reverse("index"))

def home(request):
    reviews = models.Review.objects.all().order_by('-created_at')[:3]
    books = models.Book.objects.exclude(reviews__isnull = True)
    context = {
        'reviews' : reviews,
        'all_books' : books
    }
    return render(request, "beltreview/home.html", context)
