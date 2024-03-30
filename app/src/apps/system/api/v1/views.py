from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    Health Check endpoint.
    """

    @swagger_auto_schema(
        operation_summary="Health Check",
        operation_description="Returns the health status of the API",
        responses={
            200: openapi.Response(
                "API is up and running",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            )
        },
    )
    def get(self, request):
        return Response({"status": "UP", "message": "API is running smoothly."}, status=status.HTTP_200_OK)
