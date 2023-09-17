from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world!")

@api_view(['GET', 'POST'])
def booksAPI(request):
    if request.method == 'GET':
        books = Book.objects.all()  # Book 모델로부터 전체 데이터 가져오기
        serializer = BookSerializer(books, many=True) # many=Ture => 여러 데이터에 대한 처리
        # 시리얼라이저에 전체 데이터를 한번에 집어넣기(직렬화, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        # POST 요청으로 들어온 데이터를 시리얼라이저에 집어넣기
        if serializer.is_valid():
            serializer.save()
            # 시리얼라이저의 역직렬화를 통해 save(), 모델시리얼라이저의 기본 create() 함수가 동작
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            #2 201 메세지를 보내며 성공!
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def bookAPI(request, bid):  # /book/bid/
    book = get_object_or_404(Book, bid=bid) #bid = id 인 데이터를 Book에서 가져오고, 업으면 404 에러
    serializer = BookSerializer(book)   # 시리얼라이저에 데이터를 집어넣기(직렬화)
    return Response(serializer.data, status=status.HTTP_200_OK)
