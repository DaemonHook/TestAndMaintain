import pandas as pd

BM_df = pd.read_excel("BM&VM.xlsx", sheet_name=0)
VM_df = pd.read_excel("BM&VM.xlsx", sheet_name=1)
# print(BM_df)
# print(VM_df)


def create_BM(name: str, storage: int, cpu_num: int, memory: int) -> dict:
    return {
        'type': 'BM',
        'name': name,
        'storage': storage,
        'storage_rem': storage,
        'cpu_num': cpu_num,
        'cpu_num_rem': cpu_num,
        'memory': memory,
        'memory_rem': memory,
        'vm_list': [],
    }


def create_VM(name: str, storage: int, cpu_num: int, memory: int) -> dict:
    return {
        'type': 'VM',
        'name': name,
        'storage': storage,
        'cpu_num': cpu_num,
        'memory': memory,
    }


def add_VM(BM: dict, VM: dict) -> bool:
    if BM['storage_rem'] >= VM['storage'] and BM['cpu_num_rem'] >= VM['cpu_num']\
            and BM['memory_rem'] >= VM['memory']:
        BM['vm_list'].append(VM)
        BM['cpu_num_rem'] -= VM['cpu_num']
        BM['memory_rem'] -= VM['memory']
        BM['storage_rem'] -= VM['storage']
        return True
    else:
        return False


BM_list_origin = []
for line in BM_df.values:
    name = line[0]
    storage = line[1]
    cpu_num = line[2]
    memory = line[3] * 1024                 # 内存以MB为单位
    # print(name, storage, cpu_num, memory)
    BM_list_origin.append(create_BM(name, storage, cpu_num, memory))

VM_list_origin = []
for line in VM_df.values:
    name = line[0]
    storage = line[1]
    cpu_num = line[2]
    memory = line[3]
    VM_list_origin.append(create_VM(name, storage, cpu_num, memory))


# print(BM_list)
# print(VM_list)

def depatch_VM(BM_list: list[dict], VM_list: list[dict]) -> bool:
    i = 0
    for VM in VM_list:
        if i >= len(BM_list):
            return False
        if not add_VM(BM_list[i], VM):
            i += 1
    return True


def calculate_score(BM_list: list[dict]) -> float:
    n = len(BM_list)
    score_per_occupied_VM = 3.0 * float(n)

    def score_occupancy(BM):
        return (BM['cpu_num_rem'] / BM['cpu_num']) ** 2 + \
            (BM['memory_rem'] / BM['memory']) ** 2 + \
            (BM['storage_rem'] / BM['storage']) ** 2

    score = 0
    for BM in BM_list:
        if len(BM['vm_list']) != 0:
            score += score_per_occupied_VM
            score -= score_occupancy(BM)

    return score
