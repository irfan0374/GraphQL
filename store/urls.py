from django.urls import path
from graphene_django.views import GraphQLView
# from django.views.decorators.csrf import csrf_exempt
from .schema import user_schema

urlpatterns = [
  path("user", GraphQLView.as_view(graphiql=True,schema=user_schema)),
]
