from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.dependencies import get_context
from app.graphql.schema import schema


origin = [
    "http://localhost:3000",
    "http://localhost:8000",
]

graphql_app = GraphQLRouter(schema, context_getter=get_context)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")
