from django.urls import path

from post.views import PostWriteView, PostDetailView, PostListView, PostDeleteView, PostUpdateView

app_name = 'post'

urlpatterns = [
    path('write/', PostWriteView.as_view(), name='write'),
    path('detail/', PostDetailView.as_view(), name='detail'),
    path('list/', PostListView.as_view(), name='list'),
    path('delete/', PostDeleteView.as_view(), name='delete'),
    path('update/', PostUpdateView.as_view(), name='update')
]