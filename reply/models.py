from django.db import models

from member.models import Member
from post.models import Post
from project.period import Period


class Reply(Period):
    post = models.ForeignKey(Post, null=False, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, null=False, on_delete=models.PROTECT)
    reply_content = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'tbl_reply'
        ordering = ['-id']
