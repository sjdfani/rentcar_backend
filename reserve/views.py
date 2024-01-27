from rest_framework.views import APIView
from rest_framework .response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import (
    CreateReserveSerializer,
)


class CreateReserve(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = CreateReserveSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
