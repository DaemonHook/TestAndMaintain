import json
import libs.FilesizeConverter as fszCvtr

data_json_file = open('./data.json')
origin_data = json.load(data_json_file)
data_json_file.close()

nodeInfos = origin_data['nodes']

shardInfos = origin_data['shards']
