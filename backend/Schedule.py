import math
import pandas as pd
import random

SHUFFLE_TIMES = 3
START_TEMPERATURE = 100.0
END_TEMPERATURE = 0.01
COLD_COEF = 0.97

BM_df = pd.read_excel("BM&VM.xlsx", sheet_name=0)
VM_df = pd.read_excel("BM&VM.xlsx", sheet_name=1)

START_TEMPERATURE = 3.0 * len(VM_df)


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


def copy_BM(BM: dict) -> dict:
    cp = BM.copy()
    cp['vm_list'] = BM['vm_list'].copy()
    return cp


def create_VM(name: str, storage: int, cpu_num: int, memory: int) -> dict:
    return {
        'type': 'VM',
        'name': name,
        'storage': storage,
        'cpu_num': cpu_num,
        'memory': memory,
    }


def add_VM(BM: dict, VM: dict) -> bool:
    """
    将VM分配给BM
    return: True 如果分配成功 否则 False
    """
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


def copy_VM_list(VM_list: list[dict]) -> list[dict]:
    return [VM for VM in VM_list]


def copy_BM_list(BM_list: list[dict]) -> list[dict]:
    return [copy_BM(BM) for BM in BM_list]


def depatch_VM(BM_list: list[dict], VM_list: list[dict]) -> bool:
    """
    将VM_list顺序地分配给BM_list

    return: True if VM_list are all assigned else False
    """
    if len(BM_list) == 0:
        return False
    for VM in VM_list:
        j = 0
        while add_VM(BM_list[j], VM) == False:
            j += 1
            if j >= len(BM_list):
                return False
    return True


def calculate_fitness(BM_list: list[dict]) -> float:
    """
    评估分配的好坏，分数越小越好
    """
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


def variate(VM_list: list[dict]) -> list[dict]:
    new_list = copy_VM_list(VM_list)
    indexes = [i for i in range(len(VM_list))]
    l = random.choices(indexes, k=2)
    new_list[l[0]], new_list[l[1]] = new_list[l[1]], new_list[l[0]]
    return new_list


def simulation_annealing(VM_list: list[dict]) -> tuple[bool, float, list[dict]]:
    """
    以VM_list为添加顺序，进行一次模拟退火算法

    return: 是否成功，评估分数，最优的分配后的BM_list
    """
    BM_list = copy_BM_list(BM_list_origin)
    first_BM_list = copy_BM_list(BM_list)
    # print(f'first_BM_list len: {len(first_BM_list)}, VM_list len: {len(VM_list)}')
    first_depatch = depatch_VM(first_BM_list, VM_list)
    if not first_depatch:
        return False, math.inf, []
    bestScore, bestList = calculate_fitness(
        first_BM_list), copy_BM_list(BM_list)
    adopted_score = bestScore
    adopted_VM_list = VM_list

    temperature = START_TEMPERATURE
    while temperature > END_TEMPERATURE:
        # print(f'tem: {temperature}')
        temperature *= COLD_COEF
        new_VM_list = variate(adopted_VM_list)
        new_BM_list = copy_BM_list(BM_list)
        suc = depatch_VM(new_BM_list, new_VM_list)
        if not suc:
            continue
        new_score = calculate_fitness(new_BM_list)
        if new_score < bestScore or random.random() < math.exp(-(new_score - adopted_score) / temperature):
            adopted_score = new_score
            adopted_VM_list = new_VM_list
            if new_score < bestScore:
                bestScore, bestList = new_score, new_BM_list
    return True, bestScore, bestList


def SA_routine() -> list[dict]:
    VM_lists = []
    VM_lists.append(sorted(copy_VM_list(VM_list_origin),
                    key=lambda vm: vm['cpu_num']))
    VM_lists.append(sorted(copy_VM_list(VM_list_origin),
                    key=lambda vm: vm['storage']))
    VM_lists.append(sorted(copy_VM_list(VM_list_origin),
                    key=lambda vm: vm['memory']))
    VM_lists.append(list(reversed(sorted(copy_VM_list(VM_list_origin),
                    key=lambda vm: vm['cpu_num']))))
    VM_lists.append(list(reversed(sorted(copy_VM_list(VM_list_origin),
                    key=lambda vm: vm['storage']))))
    VM_lists.append(list(reversed(sorted(copy_VM_list(VM_list_origin),
                    key=lambda vm: vm['memory']))))
    for i in range(SHUFFLE_TIMES):

        cur_list = copy_VM_list(VM_list_origin)
        random.shuffle(cur_list)
        VM_lists.append(cur_list)
    result_list = []
    print(f'待选数量：', len(VM_lists))
    for i, VM_list in enumerate(VM_lists):
        print('scheduling:', i)
        suc, score, BM_list = simulation_annealing(VM_list)
        if suc:
            result_list.append((score, BM_list))
    if len(result_list) == 0:
        return []
    best = min(result_list, key=lambda x: x[0])
    # ssize = 0
    # for BM in best[1]:
    #     ssize += len(BM["vm_list"])
    #     print(
    #         f'name: {BM["name"]}, subsize: {len(BM["vm_list"])}, cpu_free: {BM["cpu_num_rem"]}, mem_free: {BM["memory_rem"]}, sto_free: {BM["storage_rem"]}')
    #     print('vm_list: ')
    #     print(BM['vm_list'])
    # print(f'ssize: {ssize}')
    
    return best[1]
