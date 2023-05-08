import json
import libs.FilesizeConverter as fszCvtr

data_json_file = open('./data.json')
origin_data = json.load(data_json_file)
data_json_file.close()


class NodeInfo:
    def __init__(self, ip: str, master_name: str) -> None:
        self.ip = ip
        self.master_name = master_name

    def __str__(self) -> str:
        return f'<ip: {str(self.ip)}, master_name: {str(self.master_name)}>'

    def __repr__(self) -> str:
        return self.__str__()


cluster_infos = [NodeInfo(c['ip'], c['masterName'])
                 for c in origin_data['clusters']]


class IndexData:
    def __init__(self, index: str, shard: int, prirep: str, state: str, docs: int, store: int,
                 ip: str, node: str) -> None:
        self.index = index
        self.shard = shard
        self.prirep = prirep
        self.state = state
        self.docs = docs
        self.store = store          # 此处转换为byte数
        self.ip = ip
        self.node = node

    def __str__(self) -> str:
        return f'<index: {self.index}, shard: {self.shard}, prirep: {self.prirep}, state: {self.state}, docs: {self.docs}, store: {self.store}, ip: {self.ip}, node:{self.node}>'

    def __repr__(self) -> str:
        return self.__str__()


index_datas = [IndexData(i['index'], int(i['shard']), i['prirep'], i['state'],
                         int(i['docs']), fszCvtr.human2bytes(i['store']), i['ip'], i['node'])
               for i in origin_data['partitions']]
