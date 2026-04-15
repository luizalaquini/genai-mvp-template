import sys
sys.path.append("..")
from src.core.chains.base_chain import SimpleChain

chain = SimpleChain()
chain.run("Qual a capital do Brasil?")