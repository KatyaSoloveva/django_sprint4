from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView, UpdateView, ListView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .forms import CommentForm, PostForm
from .models import Category, Post, User
from .constants import PAGINATE_BY
from core.utils import get_optimized_posts, get_optimized_published_posts
from core.mixins import CommentMixin, OnlyAuthorMixin, PostMixin


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = PAGINATE_BY
    queryset = get_optimized_published_posts(Post.objects)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class PostUpdateView(PostMixin, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class PostDeleteView(PostMixin, DeleteView):
    pass


class PostDetailView(ListView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    paginate_by = PAGINATE_BY

    def get_post(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if post.author != self.request.user and not post.is_published:
            raise Http404
        return post

    def get_queryset(self):
        return self.get_post().comments.select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['post'] = self.get_post()
        return context


class ProfileListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = PAGINATE_BY

    def get_author(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        author = self.get_author()
        posts = get_optimized_posts(author.posts)
        if self.request.user != author:
            return get_optimized_published_posts(author.posts)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_author()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ('username', 'first_name', 'last_name', 'email')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = PAGINATE_BY

    def get_category(self):
        return get_object_or_404(Category,
                                 is_published=True,
                                 slug=self.kwargs['category_slug'])

    def get_queryset(self):
        return get_optimized_published_posts(self.get_category().posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class CommentCreateView(CommentMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(CommentMixin, OnlyAuthorMixin, UpdateView):
    pass


class CommentDeleteView(CommentMixin, OnlyAuthorMixin, DeleteView):
    pass
