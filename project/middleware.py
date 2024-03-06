from django.shortcuts import redirect


def pre_handle_request(get_response):
    def middleware(request):
        uri = request.get_full_path()
        print(uri)

        # 미들웨어에 작성한 코드가 반영되면 안되는 URI가 있고,
        # 이 URI가 아니라면,
        if 'admin' not in uri and 'accounts' not in uri and 'oauth' not in uri and 'api' not in uri:
            # 요청한 서비스가 로그인을 필요로 한다면,
            if 'join' not in uri and 'login' not in uri:
                if request.session.get('member') is None:
                    # 요청한 경로를 session에 담은 뒤
                    request.session['previous_uri'] = uri
                    # 로그인 페이지로 이동시킨다.
                    return redirect('/member/login')
            if request.user_agent.is_mobile:
                if 'mobile' not in uri:
                    uri = f'/mobile{uri}'
                    return redirect(uri)

            # 모바일이 아니라면,
            else:
                if 'mobile' in uri:
                    uri = uri.replace('/mobile', '')
                    return redirect(uri)

        # 응답 전처리
        response = get_response(request)

        # 응답 후처리
        return response

    return middleware
