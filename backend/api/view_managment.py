from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404


def method_post_and_delete(queryset, request, pk, model):
    """Метод добавления и удаления подписок, с проверкой дублирования
    при добавлении и проверкой на наличие при удалении"""
    recipe = get_object_or_404(queryset, pk=pk)
    if request.method == 'POST':
        obj, create = model.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if create:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        obj = model.objects.filter(user=request.user, recipe=recipe)
        if obj:
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
