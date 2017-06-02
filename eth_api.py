from py4j.java_gateway import JavaGateway


class ethAPI:

    def __init__(self):
        print('ethAPI init')
        gateway = JavaGateway()

        # init instance of api java class
        self.eth_api = gateway.entry_point

    def connect(self):
        self.eth_api.connect()

    def createSuitabilityProfile(self, addr, data):
        self.eth_api.createSuitabilityProfile(addr, data)

    def addToWhitelist(self, addr):
        self.eth_api.addToWhitelist(addr)

    def deleteFromWhitelist(self, addr):
        self.eth_api.deleteFromWhitelist(addr)

    def retrieval(self, retriever_addr):
        # need to connect to get new account
        self.connect()
        return self.eth_api.retrieval(retriever_addr)


