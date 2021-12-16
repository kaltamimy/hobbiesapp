from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import date
import base64
import json
import io
from django.core.files.images import ImageFile
from django.contrib import messages

from .models import Hobby, User, FriendRequest


def hobbies_api(request):
    '''
        API entry point for list of hobbies
        On POST: Create a new hobby
        ON GET: Get a list of all hobbies
    '''

    if request.method == "POST":
        body = json.loads(request.body)
        if body != {}:
            hobby = body['hobby']
            Hobby.objects.create(
                hobby=hobby
                )
            return JsonResponse({
                'hobbies': [
                    hobby.to_dict()
                    for hobby in Hobby.objects.all()
                ]
            })

    if request.method == "GET":
        return JsonResponse({
                'hobbies': [
                    hobby.to_dict()
                    for hobby in Hobby.objects.all()
                ]
        })

def profile_api(request):
    '''
        API entry point for profile
        On PUT: Update a profile
        ON GET: Get a profile
    '''
            
    if request.method == "PUT":
        body = json.loads(request.body)
        user = request.user
        profile = get_object_or_404(User, username=user.username)
        if body['email'] != '':
            profile.email = body['email']
        if body['dob'] != '':
            profile.dob = body['dob']
        if body['image'] != '':
            image = ImageFile(io.BytesIO(base64.b64decode(body['image'].split('data:image/png;base64,')[1])), name=body['imageName'])
            profile.image = image
        if body['city'] != '':
            profile.city = body['city']
        if body['hobbies'] != []:
            profile.hobbies.clear()
            for hobby_name in body['hobbies']:
                hobby = Hobby.objects.get(hobby=hobby_name)
                profile.hobbies.add(hobby)
        profile.save()
        messages.info(request, 'Profile Updated!')
        return JsonResponse({})


    if request.method == "GET":
        user = request.user
        sent_friend_requests = FriendRequest.objects.filter(from_user=user)
        sent_to = []
        for sent in sent_friend_requests:
            sent_to.append(sent.to_user.to_dict())
        received_friend_requests = FriendRequest.objects.filter(to_user=user)
        received_from = []
        for received in received_friend_requests:
            received_from.append(received.from_user.to_dict())
        return JsonResponse({
                'profile': user.to_dict(),
                'sent': sent_to,
                'received': received_from
        })

def users_api(request):
    '''
        API entry point for list of users
        ON POST: Filter the list of users
        ON GET: Get a list of all users
    '''

    if request.method == "POST":
        curr_user = request.user
        users = []
        for user in User.objects.exclude(username=curr_user.username):
            users.append(user.to_dict())
        sorted_users = sorted(users, key=lambda x: len(list(set(curr_user.hobbies.values_list()) & set(x['hobbies']))), reverse=True)
        body = json.loads(request.body)
        print(sorted_users)
        if body != {}:
            city = body['city']
            min_age = body['min_age']
            max_age = body['max_age']
            if min_age == '':
                min_age = 0
            if max_age == '':
                max_age = 150
            today = date.today()
            if city != '':
                users_filtered = [user for user in sorted_users if ((user['city'] == city) and (today.year - user['dob'].year - ((today.month, today.day) < (user['dob'].month, user['dob'].day)) >= min_age) and (today.year - user['dob'].year - ((today.month, today.day) < (user['dob'].month, user['dob'].day)) <= max_age))]
            else:
                users_filtered = [user for user in sorted_users if (today.year - user['dob'].year - ((today.month, today.day) < (user['dob'].month, user['dob'].day)) >= min_age and today.year - user['dob'].year - ((today.month, today.day) < (user['dob'].month, user['dob'].day)) <= max_age)]
            return JsonResponse({
                'users': users_filtered,
            })

    if request.method == "GET":
        curr_user = request.user
        users = []
        for user in User.objects.exclude(username=curr_user.username):
            users.append(user.to_dict())
        sorted_users = sorted(users, key=lambda x: len(list(set(curr_user.hobbies.values_list()) & set(x['hobbies']))), reverse=True)
        sent_friend_requests = FriendRequest.objects.filter(from_user=curr_user)
        sent_to = []
        for sent in sent_friend_requests:
            sent_to.append(sent.to_user.to_dict())
        return JsonResponse({
                'users': sorted_users,
                'sent': sent_to
        })

def sent_friend_request_api(request):
    '''
        API entry point for a friend request
        On POST: Create a new friend request
        ON DELETE: Cancel a friend request
    '''

    if request.method == "POST":
        body = json.loads(request.body)
        curr_user = request.user
        user = get_object_or_404(User, username=body['user']['username'])
        FriendRequest.objects.create(
                from_user=curr_user,
                to_user=user)
        sent_friend_requests = FriendRequest.objects.filter(from_user=curr_user)
        sent_to = []
        for sent in sent_friend_requests:
            sent_to.append(sent.to_user.to_dict())
        return JsonResponse({
            'sent': sent_to
        })

    if request.method == "DELETE":
        body = json.loads(request.body)
        curr_user = request.user
        user = get_object_or_404(User, username=body['user']['username'])
        friend_request = get_object_or_404(FriendRequest, from_user=curr_user,
                to_user=user)
        friend_request.delete()
        sent_friend_requests = FriendRequest.objects.filter(from_user=curr_user)
        sent_to = []
        for sent in sent_friend_requests:
            sent_to.append(sent.to_user.to_dict())
        return JsonResponse({
            'sent': sent_to
        })

def received_friend_request_api(request):
    '''
        API entry point for a friend request
        On POST: Accept a friend request
        ON DELETE: Reject a friend request
    '''

    if request.method == "POST":
        body = json.loads(request.body)
        curr_user = request.user
        user = get_object_or_404(User, username=body['user']['username'])
        curr_user.friends.add(user)
        user.friends.add(curr_user)
        friend_request = get_object_or_404(FriendRequest, from_user=user, to_user=curr_user)
        friend_request.delete()
        received_friend_requests = FriendRequest.objects.filter(to_user=curr_user)
        received_from = []
        for received in received_friend_requests:
            received_from.append(received.from_user.to_dict())
        return JsonResponse({
            'profile': curr_user.to_dict(),
            'received': received_from
        })

    if request.method == "DELETE":
        body = json.loads(request.body)
        curr_user = request.user
        user = get_object_or_404(User, username=body['user']['username'])
        friend_request = get_object_or_404(FriendRequest, from_user=user,
                to_user=curr_user)
        friend_request.delete()
        received_friend_requests = FriendRequest.objects.filter(to_user=curr_user)
        received_from = []
        for received in received_friend_requests:
            received_from.append(received.from_user.to_dict())
        return JsonResponse({
            'received': received_from
        })

def friend_api(request):
    '''
        API entry point for a friend
        ON DELETE: Delete a friend
    '''

    if request.method == "DELETE":
        body = json.loads(request.body)
        curr_user = request.user
        user = get_object_or_404(User, username=body['friend'])
        curr_user.friends.remove(user)
        user.friends.remove(curr_user)
        return JsonResponse({
            'profile': curr_user.to_dict(),
        })