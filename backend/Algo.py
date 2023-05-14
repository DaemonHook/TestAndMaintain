import heapq
import math
import json
from DataLoader import nodeInfos, shardInfos
from libs.FilesizeConverter import human2bytes
import copy


class Shard:
    """
    分片的副本, 设为一个hashable的类，以方便后续实现
    """

    def __init__(self, shardInfo: dict) -> None:
        """
        只记录特殊的属性
        param:
            shardData: shard的原始数据
        """
        self.index = shardInfo['index']
        self.shard = shardInfo['shard']
        self.prirep = shardInfo['prirep']
        self.nodeName = shardInfo['node']
        self.sto = human2bytes(shardInfo['store'])
        self.data = shardInfo

    def __eq__(self, __value: object) -> bool:
        """
        认为主副分片相等
        """
        return (self.index, self.shard) == (__value.index, __value.shard)

    def __lt__(self, other: object) -> bool:
        return self.sto < other.sto

    def __repr__(self) -> str:
        return f'<index: {self.index}, self.shard: {self.shard}, self.prirep: {self.prirep}>'


class Node:
    def __init__(self, nodeInfo: dict) -> None:
        self.name = nodeInfo['masterName']
        self.ip = nodeInfo['ip']
        self.subshards: list[Shard] = []
        self.data = nodeInfo

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def __hash__(self) -> int:
        return hash(self.name)

    def removeShard(self, subshard: Shard) -> None:
        self.subshards.remove(subshard)

    def addShard(self, subshard: Shard) -> None:
        self.subshards.append(subshard)

    def __repr__(self) -> str:
        return f'<masterName: {self.name}, ip: {self.ip} subshards: {str(self.subshards)}>'

    def shardCount(self) -> int:
        return len(self.subshards)


NODE_SHARD_THRESHOLD = 4     # 每个节点上的分片阈值


def AutoSetShardThreshold():
    """
    自动设置分片阈值
    """
    SHARD_THRESHOLD = math.ceil(len(shardInfos) / len(nodeInfos))


class State:
    def __init__(self, nodeInfos, shardInfos) -> None:
        self.nodeDict: dict[str, Node] = dict()
        for nodeInfo in nodeInfos:
            self.nodeDict[nodeInfo['masterName']] = Node(nodeInfo)
        for shardInfo in shardInfos:
            self.nodeDict.get(shardInfo['node']).addShard(
                Shard(shardInfo))

    def __repr__(self) -> str:
        return f'[State: nodeDict: {self.nodeDict}]'

    def originNode(self, shard: Shard) -> Node:
        return self.nodeDict[shard.nodeName]

    # def getCandidates(self, shard: Shard) -> list[Node]:
    #     return filter(lambda node: node.ip != self.OriginNode(shard).ip, list(self.nodeDict.values()))

    def getAvailableTransferShard(self, outNode: Node, inNode: Node) -> Shard:
        outNode.subshards.sort(key=lambda shard: shard.sto)

        # 假定主副分片在同一ip上的情况不可能发生
        if outNode.ip == inNode.ip:
            return outNode.subshards[0] if len(outNode.subshards) > 0 else None

        nodesOfInNodeIP = filter(
            lambda node: node.ip == inNode.ip, self.nodeDict.values())
        shardsOfInNodeIP = [
            shard for node in nodesOfInNodeIP for shard in node.subshards]
        for shard in outNode.subshards:
            # 确保主副分片
            if shard not in shardsOfInNodeIP:
                return shard
        return None

    def transferShard(self, shard: Shard, newNode: Node):
        oldNode = self.originNode(shard)
        oldNode.removeShard(shard)
        newNode.addShard(shard)
        shard.nodeName = newNode.name


originState = State(nodeInfos, shardInfos)


def GetTransferList(state: State) -> list[dict]:
    state = copy.deepcopy(state)
    # 转出集合
    outset = set(filter(lambda node: node.shardCount() >
                 NODE_SHARD_THRESHOLD,  state.nodeDict.values()))
    # 转入集合
    inset = set(filter(lambda node: node.shardCount() <
                NODE_SHARD_THRESHOLD,  state.nodeDict.values()))

    print('inset:', inset)
    print('outset:', outset)

    transferList = []

    while len(outset) > 0 and len(inset) > 0:
        outNode = outset.pop()
        print('outNode:', outNode)
        inNodeList = list(inset)
        # print('inNodeList:', inNodeList)
        for inNode in inNodeList:
            print('inNode:', inNode)
            shard = state.getAvailableTransferShard(outNode, inNode)
            if shard is not None:
                state.transferShard(shard, inNode)
                transferList.append({
                    'from': outNode.data,
                    'to': inNode.data,
                    'shard': shard.data
                })
                if outNode.shardCount() > NODE_SHARD_THRESHOLD:
                    outset.add(outNode)
                if inNode.shardCount() >= NODE_SHARD_THRESHOLD:
                    inset.remove(inNode)

    return transferList


print('transferList:', GetTransferList(originState))
