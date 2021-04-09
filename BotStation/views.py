from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from AuthenticationAndVerification.models import *
from .models import *

from blogthat import firebase
import re

@csrf_exempt
def webhook(request):
    response = MessagingResponse()
    if request.method == "POST":
        number = request.POST.get("WaId")
        message = request.POST.get("Body")

        if not check_user_exist(number):
            msg = temp_register_user(request.POST)
            response.message(msg)
            return HttpResponse(response.to_xml(), content_type='text/xml')

        else:
            pass

        media = request.POST.get("MediaUrl0")
        print(request.POST)
        response.message('Next procedure and user controls are under development,\nyou said: ' + message)
    return HttpResponse(response.to_xml(), content_type='text/xml')

# support functions

def check_user_exist(number):
    user = User.objects.filter(contact_no = number)
    if not user:
        return False
    
    return True

def temp_register_user(data):
    number = data.get("WaId")
    msg = data.get("Body")

    tmp_user = TempUserMessage.objects.filter(number=number).first()
    if not tmp_user:
        tmp_user = TempUserMessage.objects.create(number=number)
        tmp_user.last_outgoing = "registration"
        tmp_user.save()
        msg = """Hey There! \n*Welcome To Bloggingpool*\nYou can visit us here: https://blogpool.herokuapp.com/\n\n\nDo you want to start registration procedure?\nRegistration is required to use our service.\nanswer with yes/no"""

    else:
        if msg.lower() == "abort":
            user_clone = UserClone.objects.filter(contact_no=number).first()
            if user_clone:
                user_clone.delete()
            tmp_user.last_outgoing = "registration"
            tmp_user.save()
            msg = "*All the temporary data is deleted* \n\n\n\n*Welcome To Bloggingpool*\nYou can visit us here: https://blogpool.herokuapp.com/\n\n\nDo you want to start registration procedure?\nRegistration is required to use our service.\nanswer with yes/no"
        else:
            if tmp_user.last_outgoing == "registration":
                if msg.lower() == "yes":
                    tmp_user.last_outgoing = "fullname"
                    tmp_user.save()
                    msg = "Enter your full name"

                elif msg.lower() == "no":
                    msg = "Ok fine! If you change your mind than come back here."
                    tmp_user.delete()

                else:
                    msg = "Invalid response try yes or no"

            elif tmp_user.last_outgoing == "fullname":
                fullname = msg
                name = fullname.split()
                user_clone = UserClone.objects.create(contact_no= number, first_name=name[0], last_name=name[-1])
                user_clone.save()
                msg = "Enter your email address"
                tmp_user.last_outgoing = "email"
                tmp_user.save()

            elif tmp_user.last_outgoing == "email":
                email = msg
                reg = "^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)*$"
                if re.search(reg, email):
                    if User.objects.filter(email=email):
                        msg = "This email already exists, Please enter another email address"
                    else:
                        user_clone = UserClone.objects.filter(contact_no =number).first()
                        user_clone.email = email
                        user_clone.save()
                        msg = "enter a username"
                        tmp_user.last_outgoing = "username"
                        tmp_user.save()
                else:
                    msg = "This is an invalid email address, please enter an valid email address"
            
            elif tmp_user.last_outgoing == "username":
                username = msg
                reg = "^(?=.{8,20}$)(?![_])(?!.*[_]{2})[a-z0-9_]+(?<![_])$"
                if re.search(reg, username):
                    if User.objects.filter(username=username):
                        msg = "This username already exists, Please enter another username"
                    else:
                        user_clone = UserClone.objects.filter(contact_no =number).first()
                        user_clone.username = username
                        user_clone.save()
                        msg = "enter a password "
                        tmp_user.last_outgoing = "password"
                        tmp_user.save()
                else:
                    msg = "This is invalid username, it can only contain lowercase letters, numbers and underscore(_) with length of 8 to 20"

            elif tmp_user.last_outgoing == "password":
                password = msg
                if len(password) >= 8:
                    user_clone = UserClone.objects.filter(contact_no =number).first()
                    user_clone.password = password
                    user_clone.save()
                    msg = "Do you want to upload a profile image, answer in yes or no"
                    tmp_user.last_outgoing = "asked_profile_image"
                    tmp_user.save()
                else:
                    msg = "Password must contain Minimum eight characters, at least one letter, one number and one special character, please enter another password"

            elif tmp_user.last_outgoing == "asked_profile_image":
                if msg.lower() == "yes":
                    msg = "Ok fine!\nPlease send an image with jpg or png format to upload to you profile"
                    tmp_user.last_outgoing = "image_uploading"
                    tmp_user.save()

                elif msg.lower() == "no":
                    msg = f"""ok fine,\n\nThese are your details:\n\n\nFirst Name: {user_clone.first_name}\nLast Name: {user_clone.last_name}\nEmail: {user_clone.email}\nUsername: {user_clone.username}\nPassword: {user_clone.password}\nProfile picture not uploaded\nDo you want to save these details answers in yes or no"""
                    tmp_user.last_outgoing = "details_sent"
                    tmp_user.save()
                else:
                    msg = "Invalid response try yes or no"

            elif tmp_user.last_outgoing == "image_uploading":
                image_url = None
                if data.get("NumMedia")[0] == '1':
                    image_url = data.get("MediaUrl0")
                if image_url:
                    if download_and_save_image(data):
                        user_clone = UserClone.objects.filter(contact_no =number).first()
                        msg = f"""These are your details:\n\n\nFirst Name: {user_clone.first_name}\nLast Name: {user_clone.last_name}\nEmail: {user_clone.email}\nUsername: {user_clone.username}\nPassword: {user_clone.password}\nProfile Picute Uploaded\nDo you want to save these details answers in yes or no"""
                        tmp_user.last_outgoing = "details_sent"
                        tmp_user.save()
                    else:
                        msg = "invalid media type or something is wrong here, please try another image"
                else:
                    msg = "not found any type of media in your msg"

            elif tmp_user.last_outgoing == "details_sent":
                if msg.lower() == "yes":
                    user_clone = UserClone.objects.filter(contact_no =number).first()
                    user_clone_to_real_user(user_clone)
                    msg = f"Welcome {user_clone.first_name}, Your data is saved successfully! \n Now you can use our services"
                    tmp_user.last_outgoing = "registered"
                    tmp_user.save()

                elif msg.lower() == "no":
                    msg = "Do you want to start the procedure again say yes or no"
                    tmp_user.last_outgoing = "edit_details"
                    tmp_user.save()

                else:
                    msg = "Invalid response try yes or no"

            elif tmp_user.last_outgoing == "edit_details":
                if msg.lower() == "yes":
                    tmp_user.last_outgoing = "registration"
                    tmp_user.save()
                    msg = "Please enter yes to start process"

                elif msg.lower() == "no":
                    user_clone = UserClone.objects.filter(contact_no =number).first()
                    user_clone_to_real_user(user_clone)
                    msg = f"Welcome {user_clone.first_name}, Your data is saved successfully!\nNow you can use our services"
                    tmp_user.last_outgoing = "registered"
                    tmp_user.save()

                else:
                    msg = "Invalid response try yes or no"

    return msg

def user_clone_to_real_user(user_clone):
    user = User.objects.create(username=user_clone.username, email=user_clone.email, password=user_clone.password, contact_no=user_clone.contact_no, first_name=user_clone.first_name, last_name=user_clone.last_name)
    user.save()
    if user_clone.profile_image_path:
        path = user_clone.profile_image_path
        link = firebase.upload_to_firebase(path)
        user.profile_image = link
        user.save()
        import os
        os.remove(path)

def download_and_save_image(data):
    import requests
    media = data.get('MediaContentType0', '')
    if media.startswith('image/'):
        image_url = data.get("MediaUrl0")
        number = data.get("WaId")
        DOWNLOAD_DIRECTORY = "static/firebase/user_profile"
        user_clone = UserClone.objects.filter(contact_no=number).first()
        filename = user_clone.username + "_" + user_clone.contact_no + ".png"
        path = '{}/{}'.format(DOWNLOAD_DIRECTORY, filename)

        user_clone.profile_image_path = path
        user_clone.save()

        with open(path, 'wb') as f:
            f.write(requests.get(image_url).content)
        return True
        
    else:
        return False



def blog_clone_to_real():
    pass


def blog_writing(number, msg):
    pass






