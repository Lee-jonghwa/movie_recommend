
# from django.contrib.auth import login as auth_login
# from django.contrib.auth import logout as auth_logout
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
# from django.contrib.auth.decorators import login_required
# from .forms import CustomUserCreationForm, CustomUserChangeForm


# # Create your views here.
# def login(request):
#     if request.user.is_authenticated:
#         return redirect('movies:movie_list')

#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             auth_login(request, form.get_user())
#             return redirect('movies:movie_list')
#     else:
#         form = AuthenticationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/login.html', context)


# @login_required
# def logout(request):
#     auth_logout(request)
#     return redirect('movies:movie_list')


# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('movies:movie_list')

#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('movies:movie_list')
#     else:
#         form = CustomUserCreationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/signup.html', context)


# @login_required
# def delete(request):
#     request.user.delete()
#     return redirect('movies:movie_list')


# @login_required
# def update(request):
#     if request.method == 'POST':
#         form = CustomUserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('movies:movie_list')
#     else:
#         form = CustomUserChangeForm(instance=request.user)
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/update.html', context)


# @login_required
# def change_password(request, user_pk):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             return redirect('movies:movie_list')
#     else:
#         form = PasswordChangeForm(request.user)
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/change_password.html', context)

# from django.contrib.auth import get_user_model

# def profile(request, username):
#     # 어떤 유저의 프로필을 보여줄건지 유저를 조회 (username을 사용해서 조회)
#     User = get_user_model()
#     person = User.objects.get(username=username)
#     context = {
#         'person': person,
#     }
#     return render(request, 'accounts/profile.html', context)


# def follow(request, user_pk):
#     User = get_user_model()
#     # 팔로우 요청을 보내는 대상
#     you = User.objects.get(pk=user_pk)
#     # 나 (팔로우 요청하는 사람)
#     me = request.user

#     # 나와 팔로우 대상자가 같지 않을 경우만 진행 (다른 사람과만 팔로우 할 수 있음)
#     if me != you:
#     # 만약 내가 상대방의 팔로워 목록에 이미 있다면 팔로우 취소
#         if me in you.followers.all():
#             you.followers.remove(me)
#             # me.followings.remove(you)
#         else:
#             you.followers.add(me)
#             # me.followings.add(you)
#     return redirect('accounts:profile', you.username)

import json
import random
import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers.accounts import *
from movies.serializers import *
from rest_framework import status
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers.accounts import ProfileSerializer

User = get_user_model()

# 회원가입
# 인증 필요 없이 접근 가능한 영역 : 추후 인증 필요
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = AccountSignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 프로필 정보 조회 및 수정
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def profile_update(request, username):
    Users = get_object_or_404(User, username=username)
    if request.user == User:
        serializer = ProfileSerializer(instance=Users, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            serializer = ProfileSerializer(Users)
            return Response(serializer.data)

# 회원탈퇴
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_delete(request):
    request.user.delete()
    data = {
            'content': f'{request.user}님의 탈퇴처리가 완료되었습니다.',
        }
    return Response(data, status=status.HTTP_204_NO_CONTENT)


# 사용자가 좋아요/위시리스트/평점을 준 영화 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_movie_list(request, user_pk):
    Users = get_object_or_404(User, pk=user_pk)
    serializer = UserMovieListSerializer(Users)
    user_list = {
        'id' : serializer.data.get('id'),
        'user_rated_movie_count' : Users.user_rated_movie.count(),
        'user_rated_movie' : serializer.data.get('user_rated_movie'),
        'like_movies_count' : Users.like_movies.count(),
        'like_movies' : serializer.data.get('like_movies'),
        'wish_moives_count' : Users.wish_moives.count(),
        'wish_moives' : serializer.data.get('wish_moives'),
    }
    return JsonResponse(user_list)


# 팔로우 등록 및 해제 : 팔로우 수까지
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def follow(request, user_pk):
    # user_pk : 팔로우 하려는 사람의 pk
    follow_user = get_object_or_404(User, pk=user_pk)
    user = request.user
    if follow_user != user:
        if follow_user.followings.filter(pk=user.pk).exists():
            follow_user.followings.remove(user)
            follow = '팔로우' # 현재 버튼을 누르면 발생하는 동작
        else:
            follow_user.followings.add(user)
            follow = '언팔로우' # 현재 버튼을 누르면 발생하는 동작

        serializer = FollowSerializer(follow_user)

        follow_status = {
            'follow' : follow,
            'count' : follow_user.followings.count(), 
            # 팔로워(from_user_id가 팔로우 당한사람 : user_pk)(followings가 팔로우를 한 사람) 목록
            'follow_list' : serializer.data.get('followings'),
            # 팔로잉 수
            'following_count' : follow_user.followers.count(),
        }
    return JsonResponse(follow_status)


# 팔로우 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def follow_list(request, user_pk):
    # user_pk : 나의 pk
    follow_user = get_object_or_404(User, pk=user_pk)
    # user = request.user
    # if follow_user.followings.filter(pk=user.pk).exists():
    #     follow_user.followings.remove(user)
    #     follow = '팔로우' # 현재 버튼을 누르면 발생하는 동작
    # else:
    #     follow_user.followings.add(user)
    #     follow = '언팔로우' # 현재 버튼을 누르면 발생하는 동작

    serializer = FollowSerializer(follow_user)

    follow_status = {
        # 팔로워
        'follower_count' : follow_user.followings.count(), 
        # 팔로워(from_user_id가 팔로우 당한사람 : user_pk)(followings가 팔로우를 한 사람) 목록
        'follow_list' : serializer.data.get('followings'),
        # 팔로잉 수
        'following_count' : follow_user.followers.count(),
    }
    return JsonResponse(follow_status)


# 상대방 프로필 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)