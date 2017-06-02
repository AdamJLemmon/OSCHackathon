from eth_api import ethAPI

eth = ethAPI()

# call methods
print(eth.connect())
eth.createSuitabilityProfile(
    "b284f31146b21903cf89743268de9e1fe828b7e2",
    "this is the data"
)

# print(eth.connect("481bb4d6bae0734c17d0bfa4e70dad9fd13a6ae8"))
# eth.createSuitabilityProfile(
#     "481bb4d6bae0734c17d0bfa4e70dad9fd13a6ae8",
#     "22222222222222222222222222222222222222"
# )

eth.addToWhitelist("b284f31146b21903cf89743268de9e1fe828b7e2")
# eth.deleteFromWhitelist("06d3ae659a2284a04046d696cd997feea827065f")

print(eth.retrieval("b284f31146b21903cf89743268de9e1fe828b7e2"))

# print(eth.retrieval("481bb4d6bae0734c17d0bfa4e70dad9fd13a6ae8"))



