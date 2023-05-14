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
        return f'<index: {self.index}, shard: {self.shard}>'


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
        return f'<{self.name}>'

    def shardCount(self) -> int:
        return len(self.subshards)


NODE_SHARD_THRESHOLD = 4     # 每个节点上的分片阈值


def AutoSetShardThreshold():
    """
    自动设置分片阈值
    """
    global NODE_SHARD_THRESHOLD
    NODE_SHARD_THRESHOLD = math.ceil(len(shardInfos) / len(nodeInfos))


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
    print('threshold:', NODE_SHARD_THRESHOLD)
    state = copy.deepcopy(state)
    # 转出集合
    outNodeSet = set(filter(lambda node: node.shardCount() >
                 NODE_SHARD_THRESHOLD,  state.nodeDict.values()))
    # 转入集合
    inNodeSet = set(filter(lambda node: node.shardCount() <
                NODE_SHARD_THRESHOLD,  state.nodeDict.values()))

    print('inset:', inNodeSet)
    print('outset:', outNodeSet)

    transferList = []

    while len(outNodeSet) > 0 and len(inNodeSet) > 0:
        outNode = outNodeSet.pop()
        # print('after pop outset: ', outNodeSet)
        # print('outNode:', outNode)
        # print()
        # print()
        inNodeList = list(inNodeSet)
        # print('inNodeList:', inNodeList)
        for inNode in inNodeList:
            # print('inNode:', inNode)
            shard = state.getAvailableTransferShard(outNode, inNode)
            if shard is not None:
                state.transferShard(shard, inNode)
                transferList.append({
                    'from': outNode.data,
                    'to': inNode.data,
                    'shard': shard.data
                })
                # print(f'outNode: {outNode}, size: {outNode.shardCount()}')
                if outNode.shardCount() > NODE_SHARD_THRESHOLD:
                    # print(f'outNode.shardCount(): {outNode.shardCount()}, NODE_SHARD_THRESHOLD: {NODE_SHARD_THRESHOLD}')
                    outNodeSet.add(outNode)
                if inNode.shardCount() >= NODE_SHARD_THRESHOLD:
                    inNodeSet.remove(inNode)
                # print('after transfer:')
                # print('inset:', inNodeSet)
                # print('outset:', outNodeSet)
                break
    return transferList


# print('transferList:', GetTransferList(originState))
