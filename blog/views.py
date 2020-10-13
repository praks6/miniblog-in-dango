from django.shortcuts import render,HttpResponse
from .models import Post,Author,Subscribe,Contact,Comment,SubComment,Categories
import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .form import UserRegisterForm,UserUpdateForm,Profile
from django.contrib import messages

# Create your views here.
def index(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        if email:
            Subscribe(email=email).save()
    
    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    trends = Post.objects.filter(time_upload__gte = week_ago,publish=True).order_by('-read')
    TopAuthor = Author.objects.order_by('-rate')[:4]
    AuthorPost = [Post.objects.filter(author=author,publish=True).first() for author in TopAuthor]

    all_post = Paginator(Post.objects.filter(publish=True),3)
    page = request.GET.get('page')
    try:
        posts = all_post.page(page)
    except PageNotAnInteger:
        posts = all_post.page(1)
    except EmptyPage:
        posts = all_post.page(all_post.num_pages)

    parms = {
        'title':'Home | Blog',
        'posts': posts,
        'trends': trends[:5],
        'author_post':AuthorPost,
        'popular_post':Post.objects.filter(publish=True).order_by('-read')[:5],
        
    }
    return render(request,'index.html',parms)


def about(request):
    week_ago = datetime.date.today() - datetime.timedelta(days=7)
    trends = Post.objects.filter(time_upload__gte = week_ago,publish=True).order_by('-read')
    TopAuthor = Author.objects.order_by('-rate')[:4]
    AuthorPost = [Post.objects.filter(author=author,publish=True).first() for author in TopAuthor]
    parms = {
        'title':'About | Blog',
        'trends': trends[:5],
        'author_post':AuthorPost,
    }
    return render(request,'about.html',parms)


def contact(request):
	if request.method == 'POST':
		name = f"{request.POST.get('fname')} {request.POST.get('lname')}"
		email = request.POST.get('email')
		mob = request.POST.get('mob')
		mess = request.POST.get('mess','default')

		Contact(name=name,email=email,mobile=mob,message=mess).save()
	return render(request, 'contact.html')

    

def post(request, id, slug):
	try:
		post = Post.objects.get(pk=id, slug=slug)
	except:
		raise Http404("Post Does Not Exist")	

	post.read+=1
	post.save()

	if request.method == 'POST':
		comm = request.POST.get('comm')
		comm_id = request.POST.get('comm_id') #None

		if comm_id:
			SubComment(post=post,
					user = request.user,
					comm = comm,
					comment = Comment.objects.get(id=int(comm_id))
				).save()
		else:
			Comment(post=post, user=request.user, comm=comm).save()


	comments = []
	for c in Comment.objects.filter(post=post):
		comments.append([c, SubComment.objects.filter(comment=c)])
	parms = {
		'comments':comments,
		'post':post,
		'pop_post': Post.objects.order_by('-read')[:9],
        'categories':Categories.objects.all(),
		}
	return render(request, 'blog-single.html', parms)
    

def search(request):
    q=request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=q)|Q(overview__icontains=q)).distinct()
    parms = {
        'posts':posts,
        'title':f'Search Results For {q}',
        'popular_post':Post.objects.filter(publish=True).order_by('-read')[:5],
    }
    return render(request,'all.html',parms)


def view_all(request,query):
    acpt = ['trending','popular']
    q = query.lower()
    if q in acpt:
        if q == acpt[0]:
            week_ago = datetime.date.today() - datetime.timedelta(days=7)
            posts = Post.objects.filter(time_upload__gte = week_ago,publish=True).order_by('-read')
            parms = {'posts':posts,'title':"Trending Posts",'popular_post':Post.objects.filter(publish=True).order_by('-read')[:5],}
        elif q == acpt[1]:
            posts = Post.objects.filter(publish=True).order_by('-read')
            parms = {'posts':posts,'title':"Popular Posts",'popular_post':Post.objects.filter(publish=True).order_by('-read')[:5],}
        else:
            pass
    return render(request,'all.html',parms)



#user registration 
def register(request):
    form=UserCreationForm()
    if request.method == "POST":
        regForm = UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
    else:
        form=UserCreationForm()
    return render(request,'registration/register.html',{'form':form})


	
@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,instance=request.user)
		p_form = Profile(request.POST,request.FILES,instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			u_form = UserUpdateForm(instance=request.user)
			p_form = Profile(instance=request.user.profile)
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = Profile(instance=request.user.profile)
	parms ={
		'uform':u_form,
		'pform':p_form
	}
	return render(request,'account/profile.html',parms)
