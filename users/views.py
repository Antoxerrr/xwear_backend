from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import RegisterSerializer, UserSerializer


@extend_schema(
    request=RegisterSerializer,
    responses=None
)
@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response()


@extend_schema(request=UserSerializer, responses=UserSerializer)
@api_view(['GET', 'PATCH'])
def user_view(request):
    if request.method == 'GET':
        return Response(UserSerializer(request.user).data)
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
