from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Member, MemberFile
from member.serializers import MemberSerializer


class MemberCheckIdAPI(APIView):
    def get(self, request):
        member_id = request.GET['member-id']
        is_duplicated = Member.objects.filter(member_id=member_id).exists()
        return Response({'isDup': is_duplicated})


class MemberJoinView(View):
    def get(self, request):
        context = {
            'memberEmail': request.GET.get('member_email'),
            'id': request.GET.get('id')
        }
        return render(request, 'member/join.html', context)

    def post(self, request):
        data = request.POST
        data = {
            'member_name': data['member-name'],
            'member_birth': data['member-birth'],
            'member_phone': data['member-phone'],
            'member_id': data['member-id'],
            'member_password': data['member-password'],
            'member_email': data['member-email'],
        }

        # OAuth 최초 로그인 시 TBL_MEMBER에 INSERT된 회원 ID가 member_id이다.
        member = Member.objects.filter(id=request.POST.get('id'))
        # OAuth 최초 로그인 후 회원가입 시
        if member.exists():
            del data['member_email']
            data['updated_date'] = timezone.now()
            member.update(**data)
            
        else:
            member = Member.objects.create(**data)

        return redirect('member:login')


class MemberLoginWebView(View):
    def get(self, request):
        print("WEB")
        return render(request, 'member/login.html')

    def post(self, request):
        data = request.POST
        data = {
            'member_id': data['member-id'],
            'member_password': data['member-password']
        }

        members = Member.objects.filter(member_id=data['member_id'], member_password=data['member_password'])
        if members.exists():
            request.session['member'] = MemberSerializer(members.first()).data
            member_files = list(members.first().memberfile_set.values('path'))
            if len(member_files) != 0:
                request.session['member_files'] = member_files

            previous_uri = request.session.get('previous_uri')
            path = '/post/list?page=1'

            if previous_uri is not None:
                path = previous_uri
                del request.session['previous_uri']

            return redirect(path)

        return render(request, 'member/login.html', {'check': False})


class MemberLoginAppView(View):
    def get(self, request):
        print("APP")
        return render(request, 'member/login.html')

    def post(self, request):
        data = request.POST
        data = {
            'member_id': data['member-id'],
            'member_password': data['member-password']
        }

        members = Member.objects.filter(member_id=data['member_id'], member_password=data['member_password'])
        if members.exists():
            request.session['member'] = MemberSerializer(members.first()).data
            member_files = list(members.first().memberfile_set.values('path'))
            if len(member_files) != 0:
                request.session['member_files'] = member_files

            previous_uri = request.session.get('previous_uri')
            path = '/post/list?page=1'

            if previous_uri is not None:
                path = previous_uri
                del request.session['previous_uri']

            return redirect(path)

        return render(request, 'member/login.html', {'check': False})


class MemberLogoutView(View):
    def get(self, request):
        request.session.clear()
        return redirect("/member/login")


class MemberMyPageView(View):
    def get(self, request):
        # 수정된 정보가 있을 수 있기 때문에 세션 정보 최신화
        request.session['member'] = MemberSerializer(Member.objects.get(id=request.session['member']['id'])).data
        check = request.GET.get('check')
        context = {'check': check}
        return render(request, 'member/mypage.html', context)

    def post(self, request):
        data = request.POST
        file = request.FILES

        data = {
            'member_name': data['member-name'],
            'member_password': data['member-password'],
        }
        member = Member.objects.get(id=request.session['member']['id'])
        member_file = MemberFile.objects.filter(member_id=member.id)

        if member_file.exists():
            member_file = member_file.first()

        else:
            member_file = MemberFile(member=member)

        for key in file:
            member_file.path = file[key]
            member_file.updated_date = timezone.now()
            member_file.save()

        if data['member_password'] == member.member_password:
            member.member_name = data['member_name']
            member.updated_date = timezone.now()
            member.save(update_fields=['member_name', 'updated_date'])
            member_files = list(member.memberfile_set.values('path'))
            if len(member_files) != 0:
                request.session['member_files'] = member_files

            return redirect("member:mypage")

        return redirect("/member/mypage?check=false")
















