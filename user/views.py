import requests
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RegisterDraft, CustomUser
from .serializers import CustomUserSerializer
from .utils import generate_code, SmsService

# class CustomUserCreate(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user:
#                 json = serializer.data
#                 return Response(json, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


TIME_STAMP = 120  # seconds
TEMPLATE_SMS_TEXT = "مدیکپ: کد ثبت نام شما {} میباشد"


@api_view(['POST'])
def generate_registration_code(request):
    user_serializer = CustomUserSerializer(data=request.data)
    if user_serializer.is_valid() is False:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    phone_number = request.data['phone_number']
    user_registered_by_number = CustomUser.objects.filter(phone_number=phone_number)
    if len(user_registered_by_number):
        return Response({
            'error': 'this number was registered please logging in',
            'code': 3333,
        }, status=status.HTTP_404_NOT_FOUND
        )
    form = request.data
    code = generate_code()

    draft, created = RegisterDraft.objects.get_or_create(
        phone_number=phone_number,
    )
    draft.code = code
    draft.form = form
    draft.registered = False
    draft.save()

    sms_service = SmsService(settings.MP_USERNAME, settings.MP_PASSWORD)
    sms_text = TEMPLATE_SMS_TEXT.format(code)
    try:
        sms_service.send(phone_number, sms_text)
    except requests.ConnectionError:
        return Response({'error': 'sms service has a problem', 'code': 3242})

    expired_at = draft.started_at + timezone.timedelta(seconds=TIME_STAMP)

    return Response(
        {'data': {'start_at': draft.started_at, 'form': form, 'timestamp': TIME_STAMP,
                  'expired_at': expired_at}},
        status=status.HTTP_200_OK)


@api_view(['GET'])
def get_register_code_time(request, phone_number):
    try:
        draft = RegisterDraft.objects.get(phone_number=str(phone_number))
        expired_at = draft.started_at + timezone.timedelta(seconds=TIME_STAMP)
        return Response({'started_at': draft.started_at, 'timestamp': TIME_STAMP, 'expired_at': expired_at})
    except RegisterDraft.DoesNotExist:
        return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def verify_code_and_register(request):
    try:
        draft = RegisterDraft.objects.get(phone_number=request.data['phone_number'])
        expired_at = draft.started_at + timezone.timedelta(seconds=TIME_STAMP)

        if request.data['code'] == draft.code and timezone.now() < expired_at and draft.registered is False:
            user_serializer = CustomUserSerializer(data=draft.form)
            if user_serializer.is_valid():
                user_serializer.save()
                draft.registered = True
                draft.save()
                return Response({'message': 'created was successful'}, status=status.HTTP_201_CREATED)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'code does not valid or expired'}, status=status.HTTP_400_BAD_REQUEST)
    except RegisterDraft.DoesNotExist:
        return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
