from rest_framework.response import Response
from api.models import Invitation, Purchasepackage, User, Zone, Notification, Activity, Score, Package
from .serializers import AcceptrejectSerializer, ActivitySerializer, EmailSerializer, InvitationSerializer, PurchaseackageSerializer, ScoreSerializer, SecondRegisterSerializer, ShowinfoSerializer, UserSerializer, LoginSerializer, ZoneSerializer, NotificationSerializer, ShowNotificationSerializer, PackageSerializer, InvitationSerializer
from rest_framework.views import APIView
from rest_framework import status


# for jwt token
import datetime
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from RestDemo import settings


# for Authentication
from rest_framework.permissions import IsAuthenticated, AllowAny


# for login
from django.contrib.auth import authenticate
import json

# for E-mail
from django.core.mail import send_mail


class UserSerializerAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        print("........................... Register post..............................")
        serializer = UserSerializer(data=request.data)
        print("=========================>>>>>>>>>>serializer", serializer)
        serializer.is_valid()

        print('****************', serializer)
        serializer.save()
        return Response({"mes": "Register Successfully"}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        print("=================")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            print('--------->', email, password)
            user = User.objects.filter(email=email).first()
            print(user)
            print("*************login*************")
            user_serializer = ShowinfoSerializer(user)
            # for token
            token = RefreshToken.for_user(user)
            data = {
                'refresh': str(token),
                "access": str(token.access_token),
                'user_serializer': user_serializer.data
            }
        return Response(data)

# for jwt custome token


def Generate_access_token(user):

    access_token_payload = {
        'user_id': user,
        'exp': datetime.datetime.utcnow()+datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

    return access_token


def Generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user,
        'exp': datetime.datetime.utcnow()+datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')

    return refresh_token


class ZoneAPIView(APIView):
    serializer_class = ZoneSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ZoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShowzoneAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        zone = Zone.objects.exclude(user=request.user)
        serializer = ZoneSerializer(zone, many=True)
        return Response(serializer.data)


class NotificationAPIView(APIView):
    serializer_class = NotificationSerializer

    def post(self, request, zone_id):
        zone = Zone.objects.filter(id=zone_id).first()
        # zone owner name
        print("🚀 ~ file: views.py ~ line 114 ~ zone", zone.user)
        # to_user= request.user
        # print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀",to_user)

        # from_user = Zone.objects.filter(user=zone.user)

        # print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀",from_user
        data = {
            "name": "invitation",
            "description": f"you got a invitation from {request.user}"
        }
        print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀", data)
        serializer = NotificationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(to_user=request.user, from_user=zone.user, zone=zone)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShowNotificatoinAPIView(APIView):
    serializer_class = ShowNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notification = Notification.objects.filter(
            from_user=request.user).order_by('-id')
        print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀 ~ file: views.py ~ line 140 ~ notification", notification)

        serializer = ShowNotificationSerializer(notification, many=True)
        # data={
        #     "name":notification.name,
        #     "description":notification.description,
        #     "to_user":notification.from_user.email,
        #     "from_user":notification.to_user.email
        # }
        return Response(serializer.data)


class AcceptRejectAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AcceptrejectSerializer
    serializer_class = ZoneSerializer

    def post(self, request, notification_id):
        print("*******************-----------------**************>>>>", request.user)
        # zone = Zone.objects.filter(zone__user = request.user)
        zone = Zone.objects.filter(user=request.user).first()
        print("******************************************>>>>>>>>>>>>>>>>>>>>>> ZOne USER *************>>>>>>>>>>>>>>>>>>", zone)
        if zone is not None:
            notification = Notification.objects.filter(
                id=notification_id).first()
            print("******************************** to_user:",
                  notification.to_user)
            data = {
                "name": request.data['name'],
                "description": f"your invitation in {request.data['name']} from { request.user}"
            }
            print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀", data)
            to_user = request.user
            serializer = AcceptrejectSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(to_user=request.user,
                            from_user=notification.to_user)
            data = {
                "name": serializer.data['name'],
                "description": serializer.data['description'],
                "to_user": serializer.data['to_user']['email'],
                "from_user": serializer.data['from_user']['email']
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "you cant Authenticate user "})



class ShowrequestAPIView(APIView):
    serializer_class = AcceptrejectSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print("*************", request.user)
        notification = Notification.objects.filter(
            from_user=request.user).first()
        print("****************************************************", notification)
        # print("🚀 ~ file: views.py ~ line 179 ~ notificatoin🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀", notification.to_user.email)
        serializer = AcceptrejectSerializer(notification)
        print(
            "🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀 ~ file: views.py ~ line 181 ~ serializer", serializer)

        data = {
            "name": notification.name,
            "description": notification.description,
            "to_user": notification.from_user.email,
            "from_user": notification.to_user.email
        }
        return Response(data)


class SendEmailAPIVIew(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def post(self, request):
        user = request.user
        data = request.data['email']

        subject = 'welcome to GFG world to login system'
        message = f'Hi {data}, thank you.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = data
        send_mail(subject, message, email_from, [recipient_list])

        return Response({"mess": "send email succefully"})


class ActivityAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer

    def post(self, request):
        package = Purchasepackage.objects.filter(
            user=request.user).first().package.activity
        if package is not None:
            if Activity.objects.filter(user=request.user).count() < package:
                serializer = ActivitySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"mess": "sorry your activity is full "})
        else:
            return Response({"mess": "pls purche packge"})


class ShowActivityAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer

    def get(sefl, request):
        activity = Activity.objects.all()
        serializer = ActivitySerializer(activity, many=True)
        return Response(serializer.data)


class ScoreAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer

    def post(self, request, id):
        activity = Activity.objects.filter(id=id).first()
        serializer = ScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, activity=activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShowScoreAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer

    def get(self, request, id):
        user = request.user
        score = Score.objects.all()
        activity = Activity.objects.filter(id=id).first()
        score = Score.objects.filter(activity=activity).order_by('-score')
        serializer = ScoreSerializer(score, many=True)
        return Response(serializer.data)


class PackageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PackageSerializer
    
    def post(self,request):
        if request.user.is_superuser:
            serializer = PackageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"mess":"sorryyyy you cant create package "})

class GetPackageView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PackageSerializer

    def get(self, request):
        package = Package.objects.all()
        serializer = self.serializer_class(package, many=True)
        return Response(serializer.data)

class PurchasepackageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseackageSerializer

    def get(self, request):
        purchasepackage = Purchasepackage.objects.filter(user=request.user)
        serializer = self.serializer_class(purchasepackage, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        print("********************************POST************************")
        user = request.user
        print("*********************USER***********", user)
        queryset = Package.objects.filter(id=id).first()
        print("****************ID********************", queryset.id)
        data = {
            "data": queryset.id
        }
        serializer = PurchaseackageSerializer(data=data)
        print("************************SERIALIZER DATA ****************", serializer)
        serializer.is_valid(raise_exception=True)
        print("****************************************")
        serializer.save(user=request.user, package=queryset)
        return Response(serializer.data)


class InvitationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationSerializer

    def post(self, request):
        user = request.user
        print("................USER...................", user.id)
        send_email = request.data['email']
        print("******************data*********************", send_email)
        subject = 'Register now this link'
        message = "hello user, pls click the this link and register now offer till valid for 10 minitus "f'http://127.0.0.1:8000/register/{user.id}/' ""
        print("***********Message *************", message)
        email_from = settings.EMAIL_HOST_USER
        print(  
            "********************Email from  jo send kar rahahe *************", email_from)
        recipient_list = send_email
        print("****************** to_user**************** jise karna he ", recipient_list)
        data = {
            "email": send_email
        }
        serializer = InvitationSerializer(data=data)
        package_account = Purchasepackage.objects.filter(user=request.user).first()
        if  package_account:
            # package_account = Purchasepackage.objects.filter(
            #     user=request.user).first().package.account
            print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀 ~ file: views.py ~ line 393 ~ package",
                package_account)
            total_account = Invitation.objects.filter(from_to=request.user).count()
            print("🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀 ~ file: views.py ~ line 395 ~ total_account", total_account)
            if Invitation.objects.filter(from_to=request.user).count() < package_account.package.account:
                if serializer.is_valid():
                    serializer.save(from_to=request.user)
                    # send_mail(subject, message, email_from, [recipient_list])
                    return Response({"mess": "send email succefully"})
                else:
                    return Response({"mess": "The email is allready send"})
            else:
                return Response({"mess": "sorry your limit is over"})
        else:
            return Response({"mess":"pls purches package"})


class AdditionalAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_classes = SecondRegisterSerializer

    def post(self, request, id):
        user = User.objects.filter(id=id).first()
        serializer = SecondRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(primary_user=user)
        return Response({"mes": "Register Successfully"}, status=status.HTTP_201_CREATED)
