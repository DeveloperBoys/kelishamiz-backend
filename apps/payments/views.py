from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from payme.methods.generate_link import GeneratePayLink

from .serializers import CustomOrderSerializer


class OrderCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CustomOrderSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            order_id = instance.id
            amount = instance.amount

            pay_link = GeneratePayLink(
                order_id=order_id, amount=int(amount)).generate_link()

            return Response({"pay_link": pay_link}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
