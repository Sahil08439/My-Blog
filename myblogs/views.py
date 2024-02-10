from django.shortcuts import render ,redirect 
from django.http import HttpResponse 
from .models import contact_info ,Blog_Category ,Subscription,blog_post
from .form import Blog_Form,CommentForm
from .form import BlogPost_Form
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Comment
from django.db.models import Q



# Create your views here.
def home(request):
    # return HttpResponse('<h1>This is My Home Page </h1>')
      #fetch the data from db
    x=Blog_Category.objects.all()
    return render(request, 'myblogs/home.html',{"category":x})

def findproduct(request):
    if request.method == 'POST':
      x = request.POST.get('prod_search')
      blogs = blog_post.objects.filter(blog_name__icontains = x)
      if blogs:
        return render(request,'myblogs/allblogs.html',{"y":blogs,"z":x})
      else:
        return render(request,'myblogs/allblogs.html',{"y":blogs,"z":x,"errmessage":"Invalid"})
  
def Contact(request):
    # return HttpResponse('<h1>This is My Contact Page </h1>')
    if request.method == 'GET':
        return render(request, 'myblogs/contact.html')
    elif request.method == 'POST':
        email = request.POST.get('user_email')
        message = request.POST.get('message')
        x = contact_info(u_email=email, u_message=message)
        x.save()
        print(email)
        print(message)
        return render(request,'myblogs/contact.html',{'feedback':'Your message has been recorded'})
    

def Support(request):
    # return HttpResponse('<h1>This is My Support Page </h1>')
    return render(request,"myblogs/support.html")

def subscription(request):
#    return HttpResponse('<h1> Sucbcribe to Our Newsletter </h1>')
   if request.method == 'GET':
        return render(request, 'myblogs/newslatter.html')
   elif request.method == 'POST':
        email = request.POST.get('email')
        
        y = Subscription(u_email=email)
        
        if(Subscription.objects.filter(u_email = email).exists()):
          return render(request,"myblogs/newslatter.html",{'feedback':'You are already subscribed'})   
        else:
          y.save()
        #   print(email)
          return render(request,"myblogs/newslatter.html",{'feedback':'You are subscribed now'})
    
def blog(request):
    x = Blog_Form()  
    if request.method == "GET":
        return render(request,'myblogs/blog.html',{"x":x})
    else:
        print("hi")
        form = Blog_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("hi")
            return redirect('home')
        else:
            return render(request,'myblogs/blog.html',{"x":x})
        
def ck(request):
    x = BlogPost_Form()
    return render(request,'myblogs/ck.html',{"x":x})
        

def allblogs(request):
    y=blog_post.objects.all()
    paginator = Paginator(y, 3) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'myblogs/allblogs.html',{"y":page_obj,"z":"ALL"})

def blog_details(request,blog_id):
    y=blog_post.objects.get(id=blog_id)
    z=y.view_count
    z=z+1
    y.view_count=z
    y.save()
    form = CommentForm()
    return render(request,'myblogs/blog_details.html',{"y":y, "form":form})

def loginuser(request):
    if request.method =='GET':
        return render(request,'myblogs/loginuser.html',{'form':AuthenticationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password')
        user = authenticate(request,username=a,password=b)
        if user is None:
            return render(request,'myblogs/loginuser.html',{'form':AuthenticationForm(),'error':'Invalid Credentials'})
        else:
            login(request,user)
            return redirect('home')
            
    
def signupuser(request):
    if request.method =='GET':
        return render(request,'myblogs/signupuser.html',{'form':UserCreationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password1')
        c = request.POST.get('password2')
        if b == c:
            # check wether user name is unique
            if(User.object.filter(username = a)):
                return render(request,'myblogs/signupuser.html',{'error':'Username already exist'})
            else:
                user = User.object.create_user(username =a,password=b)
                user.save()
                login(request,user)
                return redirect('home')

                
        else:
            #password 1 and 2 do not match
            return render(request,'myblogs/signupuser.html',{'error':'password Mismatch Try Again'})
    
def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')
    
def allblog(request):
    # Extract the category from the request parameters
    category_name = request.GET.get('category')

    # If a category is provided, filter blog posts by that category, otherwise, get all blog posts
    if category_name:
        blogs = blog_post.objects.filter(blog_cat__blog_cat=category_name)
    else:
        blogs = blog_post.objects.all()

    return render(request, 'myblogs/blog.html', {"blogs": blogs, "category": category_name})

def cat(request, cat_id):
    x = Blog_Category.objects.get(blog_cat = cat_id)
    
    blogs = blog_post.objects.filter(blog_cat=x)
    print(blogs)
    return render(request,'myblogs/allblogs.html',{"y":blogs,"z":x.blog_cat})

def add_like(request, blog_id):
    obj = get_object_or_404(blog_post, pk=blog_id)
    print (obj.like_count)
    y=obj.like_count
    y=y+1
    obj.like_count=y
    obj.save()
    return redirect('blog_details', obj.id)

def add_comment(request, blog_id):
    post = get_object_or_404(blog_post, pk=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.created_at = timezone.now()  # Now this line should work
            comment.save()
            return redirect('blog_details', blog_id=post.id)
        else:
            return HttpResponse("Error message or form with errors")

def delete_comment(request, blog_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect( 'blog_details', blog_id=blog_id)

def edit_comment(request, blog_id, comment_id):
    # Retrieve the comment object
    comment = Comment.objects.get(id=comment_id)
    
    if request.method == 'POST':
        # Process the form submission
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog_details', blog_id=blog_id)
    else:
        # Populate the form with existing comment data
        form = CommentForm(instance=comment)
    
    return render(request, 'myblogs/edit_comment.html', {'form': form})

