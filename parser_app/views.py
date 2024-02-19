from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sqlite3

class ArticleListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Подключение к базе данных
            connection = sqlite3.connect('parser_app/parser.db')
            cursor = connection.cursor()

            # Выполнение SQL-запроса
            cursor.execute('SELECT * FROM articles;')
            data = cursor.fetchall()

            # Закрытие соединения с базой данных
            connection.close()

            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


