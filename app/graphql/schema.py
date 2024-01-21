import strawberry
from .types import RootQuery, RootMutation


@strawberry.type
class Query(RootQuery):
    pass


@strawberry.type
class Mutation(RootMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
