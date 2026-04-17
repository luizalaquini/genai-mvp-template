import sys
sys.path.append("..")
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

client = Anthropic()
response = run_chain(
    user_input="Qual a capital do Brasil?",
    model_client=client,
    variables={"domain": "geografia"}
)
print(response)