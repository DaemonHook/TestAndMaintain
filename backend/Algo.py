from DataLoader import cluster_infos, subshard_infos


class SubShard:
    """
    分片的副本, 设为一个hashable的类，以方便后续实现
    """

    def __init__(self, shardData: dict) -> None:
        """
        只记录特殊的属性
        param:
            shardData: shard的原始数据
        """
        self.index = shardData['index']
        self.shard = shardData['shard']
        self.prirep = shardData['prirep']
        self.data = shardData

    def __hash__(self) -> int:
        return hash((self.index, self.shard))

    def __eq__(self, __value: object) -> bool:
        return (self.index, self.shard) == (__value.index, __value.shard)

    def __repr__(self) -> str:
        return f'<index: {self.index}, shard: {self.shard}, prirep: {self.prirep}>'

class NodeState:
    def __init__(self, nodeInfo) -> None:
        self.masterName = nodeInfo.masterName
        self.ip = nodeInfo.ip
        self.data = nodeInfo
        self.subshards = set()

class IndexState:
    def __init__(self, indexName) -> None:
        self.name = indexName
        self.subshards = list()
    
    