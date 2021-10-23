from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


def paginate_response(data, page=0, per_page=0):
    return Response({
        'data': data,
        'page': page,
        'per_page': per_page,
    }, status=HTTP_200_OK)


def response_data(data):
    return Response(
        {'data': data},
        status=HTTP_200_OK
    )


def data_mapper(func):
    def wrapper(*args, **kwargs):
        serializer_data = func(*args, **kwargs)
        return Response(
            {'data': serializer_data},
            status=HTTP_200_OK
        )
    return wrapper
