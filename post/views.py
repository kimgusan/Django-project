import math

from django.db import transaction
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from member.models import Member
from post.models import Post, PostFile


class PostWriteView(View):
    def get(self, request):
        return render(request, 'post/write.html')

    @transaction.atomic
    def post(self, request):
        datas = request.POST
        files = request.FILES

        datas = {
            'post_title': datas['post-title'],
            'post_content': datas['post-content'],
            'member': Member.objects.get(id=request.session['member']['id'])
        }

        post = Post.objects.create(**datas)

        for key in files:
            PostFile.objects.create(post=post, path=files[key], preview=key == 'upload1')

        return redirect(post.get_absolute_url())


class PostDetailView(View):
    def get(self, request):
        post = Post.objects.get(id=request.GET['id'])
        post.post_read_count += 1
        post.updated_date = timezone.now()
        post.save(update_fields=['post_read_count', 'updated_date'])
        return render(request, 'post/detail.html', {'post': post})


class PostListView(View):
    def get(self, request):
        order = request.GET.get('order', 'recent')
        page = int(request.GET.get('page', 1))

        row_count = 5
        offset = (page - 1) * row_count
        limit = page * row_count
        total = Post.enabled_objects.all().count()
        page_count = 5
        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'page': page,
            'real_end': real_end,
            'page_count': page_count,
        }
        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        context['posts'] = list(Post.enabled_objects.all().order_by(ordering))[offset:limit]

        return render(request, 'post/list.html', context)


class PostDeleteView(View):
    @transaction.atomic
    def get(self, request):
        post = Post.objects.get(id=request.GET['id'])
        post.status = False
        post.updated_date = timezone.now()
        post.save(update_fields=['status', 'updated_date'])

        print(post.postfile_set.all())
        for post_file in PostFile.objects.filter(post_id=post.id):
            post_file.delete()

        return redirect('post:list')


class PostUpdateView(View):
    def get(self, request):
        post = Post.objects.get(id=request.GET['id'])
        context = {
            'post': post,
            'post_files': list(post.postfile_set.values('path'))
        }
        return render(request, 'post/update.html', context)

    @transaction.atomic
    def post(self, request):
        id = request.GET['id']
        datas = request.POST
        deleted_files = request.POST.getlist('deleted')
        files = request.FILES

        datas = {
            'post_title': datas['post-title'],
            'post_content': datas['post-content'],
        }

        post = Post.objects.get(id=id)
        post.post_title = datas['post_title']
        post.post_content = datas['post_content']
        post.updated_date = timezone.now()
        post.save(update_fields=['post_title', 'post_content', 'updated_date'])

        for key in files:
            PostFile.objects.create(post=post, path=files[key], preview=key == 'upload1')

        for path in deleted_files:
            PostFile.objects.get(path=path).delete()

        return redirect(post.get_absolute_url())




















