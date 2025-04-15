from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        national_id = request.data.get('national_id')
        phone_number = request.data.get('phone_number')
        user = get_user_model().objects.filter(national_id=national_id, phone_number=phone_number).first()

        if user:
            return Response(user.tokens(), status=200)
        return Response({'error': _('اطلاعات وارد شده نامعتبر است')}, status=400)