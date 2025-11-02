"""JWT authentication example."""

from phoebe_client import PhoebeClient
from phoebe_client.auth.jwt import JWTAuthProvider

with open('public_key.pem', 'r') as f:
    public_key = f.read()

auth = JWTAuthProvider(
    public_key=public_key,
    issuer="https://auth.example.com",
    audience="phoebe-api"
)

client = PhoebeClient(host="localhost", port=8001, auth_provider=auth)
client.authenticate({"token": "your_jwt_token"})

session = client.create_session()
client.set_value(twig='period@binary', value=1.5)
client.close_session()
