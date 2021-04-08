from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from AuthenticationAndVerification.models import *
from .models import *
import re

@csrf_exempt
def webhook(request):
    response = MessagingResponse()
    if request.method == "POST":
        number = request.POST.get("WaId")
        message = request.POST.get("Body")

        if not check_user_exist(number):
            msg = temp_register_user(number, message)
            response.message(msg)
            return HttpResponse(response.to_xml(), content_type='text/xml')

        
        message = request.POST.get("Body")
        check_message(message)

        media = request.POST.get("MediaUrl0")
        print(request.POST)
        response.message('just checking from where the reply is coming you said: ' + message)
    return HttpResponse(response.to_xml(), content_type='text/xml')

# support functions

def check_user_exist(number):
    user = User.objects.filter(contact_no = number)
    if not user:
        return False
    
    return True

def temp_register_user(number, msg):
    tmp_user = TempUserMessage.objects.filter(number=number).first()
    if not tmp_user:
        tmp_user = TempUserMessage.objects.create(number=number)
        tmp_user.last_outgoing = "registration"
        tmp_user.save()
        msg = """*Hey There! \n Welcome To Bloggingpool*\n Do you want to start registration procedure? \n Registration is required to use our service.\n answer with yes/no"""

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
            fullname = msg.lower()
            name = fullname.split()
            user_clone = UserClone.objects.create(contact_no= number, first_name=name[0], last_name=name[-1])
            user_clone.save()
            msg = "Enter your email address"
            tmp_user.last_outgoing = "email"
            tmp_user.save()

        elif tmp_user.last_outgoing == "email":
            email = msg
            reg = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
            if re.search(reg, email):
                if User.objects.filter(email=email):
                    msg = "This email already exists, Please enter another email address"
                else:
                    user_clone = UserClone.objects.filter(contact_no =number).first()
                    user_clone.email = email
                    user_clone.save()
                    msg = "enter a password "
                    tmp_user.last_outgoing = "password"
                    tmp_user.save()
            else:
                msg = "This is an invalid email address, please enter an valid email address"
        
        elif tmp_user.last_outgoing == "password":
            password = msg
            reg = ""
            if len(password) >= 8:
                user_clone = UserClone.objects.filter(contact_no =number).first()
                user_clone.password = password
                user_clone.save()
                msg = f"""These are your details:\n\n\n First Name: {user_clone.first_name}\n Last Name: {user_clone.last_name}\n Email: {user_clone.email}\n Password: {user_clone.password}\n Do you want to save these details answers in yes or no"""
                tmp_user.last_outgoing = "details_sent"
                tmp_user.save()
            else:
                msg = "Password must contain Minimum eight characters, at least one letter, one number and one special character, please enter another password"

        elif tmp_user.last_outgoing == "details_sent":
            if msg.lower() == "yes":
                user_clone = UserClone.objects.filter(contact_no =number).first()
                user = User.objects.create(contact_no=number,email=user_clone.email, username=user_clone.email ,password=user_clone.password, first_name=user_clone.first_name, last_name=user_clone.last_name)
                user.save()
                msg = f"Welcome {user_clone.first_name}, Your data is saved successfully! \n Now you can use our services"
                tmp_user.last_outgoing = "registered"
                tmp_user.save()

            elif msg.lower() == "no":
                msg = "Do you want to start the procedure again"
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
                user = User.objects.create(contact_no=number,email=user_clone.email, username=user_clone.email ,password=user_clone.password, first_name=user_clone.first_name, last_name=user_clone.last_name)
                user.save()
                msg = f"Welcome {user_clone.first_name}, Your data is saved successfully! \n Now you can use our services"
                tmp_user.last_outgoing = "registered"
                tmp_user.save()

            else:
                msg = "Invalid response try yes or no"

    return msg

def check_message(msg):
    pass





