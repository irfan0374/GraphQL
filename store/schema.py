from graphene_django import DjangoObjectType
import graphene
from .models import User
from .serializer import UserRegistrationSerializer


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'last_login')



class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=False)
        password = graphene.String(required=True)
        password2 = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, email, first_name, last_name=None, password=None, password2=None):
        input_data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
            'password2': password2
        }

        serializer = UserRegistrationSerializer(data=input_data)
        if serializer.is_valid():
            user = serializer.save()
            return CreateUser(user=user, success=True, errors=None)
        else:
            error_messages = "\n".join(
                [f"{field}: {error}" for field, errors in serializer.errors.items() for error in errors]
            )
            return CreateUser(user=None, success=False, errors=error_messages)



class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()



class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.ID(required=True))


    def resolve_all_users(root, info):
        return User.objects.all()


    def resolve_user_by_id(root, info, id):
        return User.objects.filter(id=id).first()

user_schema = graphene.Schema(query=Query, mutation=Mutation)
