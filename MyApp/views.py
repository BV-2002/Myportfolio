from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
# Create your views here.


from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')



EMAIL_HOST_USER = 'bathalavishnu88@gmail.com'



def send_confirmation_to_client(name, email):
    subject = '🎉 Your request has been received - Vishnu Portfolio'
    plain_message = f'Thank you {name}, we received your request.'

    html_message = f'''
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
          <h2 style="color: #2c3e50;">Hi {name},</h2>
          <p style="font-size: 16px; color: #333;">
            👋 Thank you for getting in touch!<br><br>
            Your request has been successfully received by <strong>Vishnu</strong>.
          </p>
          <p style="font-size: 15px; color: #333;">
            Vishnu will reach out to you within <strong>24 hours</strong> to assist you further.
          </p>
          <hr style="margin: 20px 0;">
          <p style="font-size: 14px; color: #777;">
            Need immediate help? You can reply to this email anytime.
          </p>
          <p style="font-size: 15px; color: #2c3e50;">
            Regards,<br>
            <strong>Vishnu Official</strong><br>
            📧 bathalavishnu88@gmail.com
          </p>
        </div>
      </body>
    </html>
    '''

    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        html_message=html_message
    )


def notify_owner_about_new_request(name, mobile, email, address, message_text):
    subject = f'📥 New Contact Request from {name}'
    plain_message = f'You have a new contact request from {name}.'

    html_message = f'''
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 650px; margin: auto; background: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
          <h2 style="color: #2c3e50;">📨 New Contact Request Received</h2>
          <p style="font-size: 15px; color: #555;">You have received a new request from your portfolio website:</p>

          <table style="width: 100%; font-size: 15px; margin-top: 20px;">
            <tr><td><strong>Name:</strong></td><td>{name}</td></tr>
            <tr><td><strong>Mobile:</strong></td><td>{mobile}</td></tr>
            <tr><td><strong>Email:</strong></td><td>{email}</td></tr>
            <tr><td><strong>Address:</strong></td><td>{address}</td></tr>
            <tr><td><strong>Message:</strong></td><td>{message_text}</td></tr>
          </table>

          <hr style="margin: 20px 0;">
          <p style="color: #888; font-size: 13px;">This message was triggered by your portfolio contact form.</p>
        </div>
      </body>
    </html>
    '''

    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],  # Sends to you (the owner)
        fail_silently=False,
        html_message=html_message
    )



from django.utils.timezone import now
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        address = request.POST.get('address')
        message_text = request.POST.get('message')

        try:
            # Save the data to the Contact model
            Contact.objects.create(
                name=name,
                mobile=mobile,
                email=email,
                address=address,
                message=message_text,
                submitted_at=now()  # saves in IST if TIME_ZONE is set in settings.py
            )

            # Send email to Vishnu
            notify_owner_about_new_request(name, mobile, email, address, message_text)

            # Send confirmation to client
            send_confirmation_to_client(name, email)

            messages.success(request, '✅ Your request has been submitted successfully. You will receive a confirmation email.')
        except Exception as e:
            print("Email sending or DB error:", e)
            messages.error(request, '❌ Something went wrong. Please try again later.')

        return render(request, 'index.html')

    return render(request, 'index.html')
