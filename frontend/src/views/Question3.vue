<template>
    <div class="chart-border">
        <div class="chart" ref="chart" style="height: 400px;"></div>
    </div>
    <div style="display: flex; flex-direction: row; width: 100%;">
        <div style="width: 40%; height: 300px; display: flex; flex-direction: column; justify-content: flex-start;">
            <el-text class="mx-1" size="large" style="margin-top: 10px;">物理机&nbsp;{{ BM_name }}&nbsp;被分配的虚拟机</el-text>
            <el-table :data="curBMData" style="width: 100%; margin-top: 10px;">
                <el-table-column prop="name" label="名称">
                </el-table-column>
                <el-table-column prop="storage" label="存储">
                </el-table-column>
                <el-table-column prop="cpu_num" label="CPU大小">
                </el-table-column>
                <el-table-column prop="memory" label="内存大小(M)">
                </el-table-column>
            </el-table>
        </div>
        <div style="width: 60%; height: 300px; display: flex; flex-direction: column;">
            <el-text class="mx-1" size="large" style="margin-top: 10px; margin-bottom: 10px;">物理机状态</el-text>
            <el-row style="display: flex; flex-direction: row;">
                <!-- <el-col> -->
                <el-statistic title="存储 (G)" :value="BM_storage" />
                <!-- </el-col> -->
                <!-- <el-col> -->
                <el-statistic title="CPU大小 (个)" :value="BM_cpu_num">
                </el-statistic>
                <!-- </el-col> -->
                <!-- <el-col> -->
                <el-statistic title="内存大小 (G)" :value="BM_memory" />
                <!-- </el-col> -->
            </el-row>
            <div style="display: flex; flex-direction: row; margin-top: 20px;">
                <Panel :rate="100 - 100 * BM_storage_rem / BM_storage" panel-name="存储占用率"
                    :numerator="BM_storage - BM_storage_rem" :denominator="BM_storage" style="flex: 1"></Panel>
                <Panel :rate="100 - 100 * BM_cpu_num_rem / BM_cpu_num" panel-name="CPU占用率"
                    :numerator="BM_cpu_num - BM_cpu_num_rem" :denominator="BM_cpu_num" style="flex: 1"></Panel>
                <Panel :rate="100 - 100 * BM_memory_rem / BM_memory" panel-name="内存占用率"
                    :numerator="BM_memory - BM_memory_rem" :denominator="BM_memory" style="flex: 1"></Panel>
            </div>
        </div>
    </div>
</template>

<script>

import * as echarts from 'echarts'
import Panel from './Panel.vue'

const BMSymbolGap = 150
const VMSymbolRadius = 50
const BMSymbolSize = 50
const VMSymbolSize = 15
const BMSymbolLineLength = 8

const CreateBMSymbolData = (x, y, BM, onclick) => {
    return {
        type: 'BM',
        name: BM.name,
        x,
        y,
        symbol: 'circle',
        symbolSize: BMSymbolSize,
        onclick,
        itemStyle: {
            color: '#4e72b8d0',
            borderColor: '#ffffff40',
            borderWidth: 6
        },
        label: {
            show: true,
            color: '#fff'
        }
    }
}

const CreateVMSymbolData = (x, y, VM) => {
    return {
        type: 'VM',
        name: VM.name,
        x,
        y,
        symbol: 'circle',
        symbolSize: VMSymbolSize,
        itemStyle: {
            color: '#d7134590',
            borderColor: '#ffffff40',
            borderWidth: 3
        },
    }
}

export default {
    data() {
        return {
            best_schedule: [],
            BM_name: "",
            BM_storage: 1,
            BM_storage_rem: 1,
            BM_cpu_num: 1,
            BM_cpu_num_rem: 1,
            BM_memory: 1,
            BM_memory_rem: 1,
            curBMData: []
        };
    },
    mounted() {
        this.api.get("./schedule").then(res => {
            console.log("res", res);
            if (res.length === 0) {
                alert("规划失败，正在重新规划分配，请刷新。如果此问题重复出现，请检查数据是否合法。");
                this.api.get("./reschedule");
            }
            else {
                this.best_schedule = res;
                this.BM_dict = new Map();
                this.VM_dict = new Map();
                this.best_schedule.forEach(BM => {
                    this.BM_dict.set(BM.name, BM);
                    BM.vm_list.forEach(VM => {
                        this.VM_dict.set(VM.name, VM);
                    });
                });
                console.log("BM_dict: ", this.BM_dict);
                console.log("VM_dict: ", this.VM_dict);
                // this.best_schedule.forEach()
                this.InitChart();
            }
        });
    },
    methods: {
        GetNodes() {
            let nodes = [];
            let i = 0, j = 0;
            this.BM_dict.forEach(BM => {
                nodes.push(CreateBMSymbolData(i * BMSymbolGap, j * BMSymbolGap, BM,
                    () => { this.RefreshData(BM); }));
                let angle = 0;
                let angleInc = 0;
                if (BM.vm_list.length > 0) {
                    angleInc = 2 * Math.PI / BM.vm_list.length;
                }
                BM.vm_list.forEach(VM => {
                    nodes.push(CreateVMSymbolData(i * BMSymbolGap + VMSymbolRadius * Math.cos(angle),
                        j * BMSymbolGap + VMSymbolRadius * Math.sin(angle), VM))
                    angle += angleInc;
                });
                i++;
                if (i == BMSymbolLineLength) {
                    i = 0;
                    j++;
                }
            });
            return nodes;
        },
        GetLinks() {
            let links = []
            this.BM_dict.forEach(BM => {
                BM.vm_list.forEach(VM => {
                    links.push({
                        source: VM.name,
                        target: BM.name,
                        lineStyle: { width: 2 }
                    })
                })
            })
            return links
        },
        InitChart() {
            this.chart = echarts.init(this.$refs.chart);
            let option = {
                title: { text: "虚拟机分配" },
                // tooltip: {},
                series: {
                    type: "graph",
                    layout: "none",
                    roam: true,
                    edgeSymbol: ['circle', 'circle'],
                    edgeSymbolSize: 1,
                    data: this.GetNodes(),
                    links: this.GetLinks(),
                }
            };
            option && this.chart.setOption(option);
            this.chart.on("click", function (params) {
                // console.log('onclick: ', params)
                let data = params.data;
                if (data.onclick !== undefined) {
                    data.onclick();
                }
            });
        },
        RefreshData(BM) {
            this.BM_name = BM.name
            this.BM_cpu_num = BM.cpu_num
            this.BM_cpu_num_rem = BM.cpu_num_rem
            this.BM_memory = BM.memory
            this.BM_memory_rem = BM.memory_rem
            this.BM_storage = BM.storage
            this.BM_storage_rem = BM.storage_rem
            this.curBMData = []
            BM.vm_list.forEach(VM => {
                this.curBMData.push({
                    name: VM.name,
                    storage: VM.storage,
                    cpu_num: VM.cpu_num,
                    memory: VM.memory
                })
            })
        }
    },
    components: { Panel }
}
</script>

<style scoped>
.el-col {
    text-align: center;
}

.el-statistic {
    flex: 1;
    text-align: center;
}
</style>