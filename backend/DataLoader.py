import json
import libs.FilesizeConverter as fszCvtr

data_json_file = open('./data.json')
origin_data = json.load(data_json_file)
data_json_file.close()

cluster_infos = origin_data['clusters']

subshard_infos = origin_data['partitions']

print('cluster_info', cluster_infos)
print('subshard_info', subshard_infos)
