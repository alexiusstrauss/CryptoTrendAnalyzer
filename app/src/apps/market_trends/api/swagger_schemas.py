from drf_yasg import openapi

# Documentação do Swagger
CURRENCY_DATA_SCHEMA = {
    'operation_summary': "Get Moving Averages for Currency Pair",
    'operation_description': "Retrieves moving averages (MMS) for a specified currency pair within a given time range and averaging period ('range').",
    'manual_parameters': [
        openapi.Parameter(
            "from",
            openapi.IN_QUERY,
            description="Start timestamp in Unix format",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
        openapi.Parameter(
            "to",
            openapi.IN_QUERY,
            description="End timestamp in Unix format",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
        openapi.Parameter(
            "range",
            openapi.IN_QUERY,
            description="Range for moving average (20, 50, 200)",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    'responses': {
        200: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "timestamp": openapi.Schema(
                        type=openapi.TYPE_INTEGER, description="Unix Timestamp of the data point"
                    ),
                    "mms": openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format="float",
                        description="Moving Average value based on the specified range",
                    ),
                },
            ),
        ),
        404: openapi.Response(
            description="Not Found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Error message explaining the pair is not found or not supported.",
                    ),
                },
            ),
        ),
    },
}
