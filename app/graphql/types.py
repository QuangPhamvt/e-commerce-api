import strawberry


@strawberry.type()
class RootQuery:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, world!"


@strawberry.type()
class RootMutation:
    @strawberry.mutation
    def hello(self, name: str) -> str:
        return f"Hello, {name}!"
