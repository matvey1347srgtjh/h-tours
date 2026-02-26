from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm, PostForm



def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            current_post_id = request.POST.get('post_id')
            target_post = Post.objects.get(id=current_post_id)
            comment = form.save(commit=False)
            comment.post = target_post
            comment.save()
            return redirect("blog-list")
    else:
        form = CommentForm()
    return render(request, 'blog-list.html', {'posts': posts, 'form': form})
    
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            
            post.save()
            return redirect('blog-list') 
    else:
        form = PostForm()
    return render(request, 'post-edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post) 
        if form.is_valid():
            post = form.save()
            return redirect('blog-list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post-edit.html', {'form': form, 'edit_mode': True})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('blog-list')
    return render(request, 'post-delete-confirm.html', {'post': post})