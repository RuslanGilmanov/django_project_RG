from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from .models import Post, Image
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm, ImageFormSet
from taggit.models import Tag
from django.views.generic import (ListView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView
                                  )


class PostListView(ListView):
    model = Post
    template_name = 'dg_application/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'dg_application/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['Image'] = Image.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data


def post_like(request, pk):
    post = get_object_or_404(Post.objects.prefetch_related('likes'), id=pk)
    if not post.likes.filter(id=request.user.id).exists():
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def post_unlike(request, pk):
    post = get_object_or_404(Post.objects.prefetch_related('likes'), id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


@login_required()
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, prefix='image')

        if post_form.is_valid() and formset.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            post_form.save_m2m()

            for form in formset:
                if form.cleaned_data.get('image'):
                    image = form.cleaned_data['image']
                    img = Image(post=post, image=image)
                    img.save()

            return redirect('post-detail', pk=post.pk)
    else:
        post_form = PostForm()
        formset = ImageFormSet(prefix='image')

    context = {
        'form': post_form,
        'formset': formset
    }

    return render(request, 'dg_application/create_post.html', context)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'dg_application/create_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ImageFormSet = inlineformset_factory(Post, Image, fields=('image',), extra=3)
        if self.request.method == 'POST':
            context['formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = ImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = reverse_lazy('dgapp-home')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def tags_view(request, tag):
    tag = get_object_or_404(Tag, slug=tag.lower())
    posts = Post.objects.filter(tags=tag)
    context = {
        'tags': tag,
        'posts': posts,
    }

    return render(request, 'dg_application/home.html', context)
