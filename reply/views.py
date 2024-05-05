from django.db.models import F
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from reply.models import Reply


class ReplyWriteAPI(APIView):
    def post(self, request):
        # 1. FormData객체가 들어오는 가
        # request.POST

        # 2. JSON이 들어오는 가
        data = request.data
        data = {
            'reply_content': data['reply_content'],
            'post_id': data['post_id'],
            'member_id': request.session['member']['id']
        }

        Reply.objects.create(**data)
        return Response('success')


class ReplyListAPI(APIView):
    def get(self, request, post_id, page):
        row_count = 5
        offset = (page - 1) * row_count
        limit = page * row_count

        replies = Reply.objects.filter(post_id=post_id)\
            .annotate(member_name=F('member__member_name'), member_path=F('member__memberfile__path'))\
            .values('reply_content', 'id', 'member_name', 'member_path', 'created_date', 'member_id')

        return Response(replies[offset:limit])


class ReplyAPI(APIView):
    def delete(self, request, reply_id):
        Reply.objects.filter(id=reply_id).delete()
        return Response('success')

    def patch(self, request, reply_id):
        reply_content = request.data['reply_content']
        updated_date = timezone.now()

        reply = Reply.objects.get(id=reply_id)
        reply.reply_content = reply_content
        reply.updated_date = updated_date
        reply.save(update_fields=['reply_content', 'updated_date'])

        return Response('success')












