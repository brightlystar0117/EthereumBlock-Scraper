import re
from farm.helpers.classContainer import Contract

def load_contracts(contracts=[], start=True):
    if start:
	    print("Loading new contracts ...\n")
    cont=[]
    for contract in contracts:
        cont.append(contract.addr)

    cont = "".join(cont)
    with open("contracts/contracts.csv") as c:
        for contract in [x.strip() for x in c]:
            if contract.split(",")[0] == "remove":
                for i in contracts:
                    if contract.split(",")[1] == i.name:
                        print("\n ---Contract of `{}` REMOVED---\n".format(i.name))
                        del contracts[contracts.index(i)]

            elif contract.split(",")[0] in cont:
                continue
            else:
                contracts.append(Contract(*tuple(re.split("\,(?=.*\()|\,(?!.*\))", contract))))
                if start:
                    print("Contract loaded @  {}".format(contracts[-1].addr))
                    print("  |--- Name        {}".format(contracts[-1].name))
                    print("  |--- Method      {}".format(contracts[-1].method.canonicalExpression))
                    print("  |--- Method ID   {}".format(contracts[-1].method.id))
                    print("  |--- StartBlock  {:,}".format(int(contracts[-1].startBlock)))
                    print("  |--- Chunksize   {:,}\n".format(contracts[-1].chunksize))

                try:
                    with open('{}.txt'.format("contracts/.lastSafedBlock/"+contracts[-1].name), 'r') as loadBlock:
                        contracts[-1].fromBlock = int(loadBlock.read())+1
                        print("`Startblock` overwritten for {} to Block {:,}\n\n".format(contracts[-1].name,
                                                                                         contracts[-1].fromBlock))
                except:
                    pass
    return contracts
