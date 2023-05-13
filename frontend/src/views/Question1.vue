<template>
    <div class="chart-border">
        <div class="chart" ref="chart"></div>
    </div>
    <div class="table-container">
        <el-table :data="tableData" style="width: 100%; padding:20px 20px">
            <el-table-column prop="index" label="索引">
            </el-table-column>
            <el-table-column prop="shard" label="分片" width="60">
            </el-table-column>
            <el-table-column prop="prirep" label="主副情况" width="80">
            </el-table-column>
            <el-table-column prop="state" label="状态" width="90">
            </el-table-column>
            <el-table-column prop="docs" label="文档数量" width="120">
            </el-table-column>
            <el-table-column prop="store" label="分片大小" width="120">
            </el-table-column>
            <el-table-column prop="ip" label="服务器ip">
            </el-table-column>
            <el-table-column prop="node" label="集群节点">
            </el-table-column>
        </el-table>
    </div>
</template>

<script>

import * as echarts from 'echarts'
import randomColor from 'randomcolor'

// x和y坐标的最大值
const maxX = 1000

const nodeSymbolSize = 50
const partitionSymbolSize = 40
const indexSymbolSize = 60
const nodeSymbolY = 50
const partitionSymbolY = 120
const indexSymbolY = 250

// node图形数据的工厂函数
const GetNodeSymbolData = (x, y, name, label, onclick) => {
    return {
        type: 'nodeSymbol',
        name,
        x,
        y,
        label: {
            show: true,
            position: 'top',
            formatter() {
                return label
            }
        },
        symbol: 'circle',
        symbolSize: nodeSymbolSize,
        itemStyle: {
            color: 'rgba(240,248,255,255)',
            borderColor: 'rgb(135,206,250)',
            borderWidth: 2
        },
        onclick,

    }
}

// 分片图形数据的工厂函数
const GetPartitionSymbolData = (x, y, name, label, onclick) => {
    return {
        type: 'partitionSymbol',
        name,
        x,
        y,
        label: {
            show: true,
            formatter() {
                return label
            },
            color: '#000'
        },
        symbol: 'roundRect',
        symbolSize: partitionSymbolSize,
        itemStyle: {
            color: label[0] == 'R' ? '#98FB9860' : '#87CEFA60',
            borderColor: '#ffffff40',
            // borderColor: label[0] == 'R' ? '#98FB98' : '#87CEFA',
            borderWidth: 6
        },
        onclick,
    }
}

// index图形数据的工厂函数
const GetIndexSymbolData = (x, y, name, label, color, onclick) => {
    return {
        type: 'indexSymbol',
        name,
        x,
        y,
        label: {
            show: true,
            formatter() {
                return label
            },
        },
        symbol: 'circle',
        symbolSize: indexSymbolSize,
        itemStyle: {
            color: color,
            borderColor: '#EE82EE30',
            borderWidth: 5
        },
        onclick,
    }
}


/*
NodeInfo: {
    node: {masterName, ip}
    partitions: [节点上所有分片]
}
*/
function NodeInfo(node) {
    this.node = node
    this.partitions = []
}

/*
IndexInfo: {
    name: 索引名称
    partitions: [节点上所有分片]
}
*/
function IndexInfo(indexName) {
    this.name = indexName
    this.partitions = []
    this.color = '#000000'
}

// 获取node内部名称，用于连线
function GetNodeInnerName(node) {
    return node.ip + node.masterName
}

// 获取partition内部名称，用于连线
function GetPartitionInnerName(partition) {
    return partition.index + partition.shard + partition.prirep
}



export default {
    data() {
        return {
            tableData: [],
            nodes: [],
            partitions: [],
            nodeInfoDict: new Map(),    // key: masterName, value: nodeInfo
            indexInfoDict: new Map()    // key: indexName, value: indexInfo
        }
    },
    mounted() {
        // TODO: 这里应该请求后端
        this.axios.get('./data.json').then(res => {
            console.log(res.data)
            this.nodes = res.data.nodes
            this.partitions = res.data.partitions
            console.log('nodes', this.nodes)
            console.log('partitions', this.partitions)
            this.BuildMap()
            this.InitChart()
        })
    },
    methods: {
        // 构造partition和node之间的映射关系
        BuildMap() {
            this.nodes.forEach((node) => {
                this.nodeInfoDict.set(node.masterName, new NodeInfo(node, []))
            })
            this.partitions.forEach((partition) => {
                let nodeInfo = this.nodeInfoDict.get(partition.node)
                if (nodeInfo === undefined) {
                    console.error('buildMap: Invalid Node name:', partition.node)
                }
                nodeInfo.partitions.push(partition)
                if (!this.indexInfoDict.has(partition.index)) {
                    this.indexInfoDict.set(partition.index, new IndexInfo(partition.index))
                }
                this.indexInfoDict.get(partition.index).partitions.push(partition)
            })
            console.log('nodeInfoDict:', this.nodeInfoDict)
            console.log('indexInfoDict', this.indexInfoDict)
        },
        // 生成echarts绘图中的data
        GetDataList() {
            let dataList = []
            let partitionSet = new Set()    // 按照顺序插入partition，确保图形的美观
            let indexSet = new Set()
            // 设定图形间距
            let nodeSymbolGap = maxX / (this.nodeInfoDict.size + 1)
            // 插入node图形
            let curX = nodeSymbolGap
            let i = 0
            this.nodeInfoDict.forEach((nodeInfo) => {
                let node = nodeInfo.node
                dataList.push(GetNodeSymbolData(curX, nodeSymbolY, GetNodeInnerName(nodeInfo.node),
                    'ES Node' + i, () => { this.OnNodeClick(node) }))
                nodeInfo.partitions.forEach((partition) => {
                    partitionSet.add(partition)
                })
                curX += nodeSymbolGap
                i++
            })

            // 插入partition图形
            let partitionSymbolGap = maxX / (partitionSet.size + 1)
            curX = partitionSymbolGap
            partitionSet.forEach((partition) => {
                dataList.push(GetPartitionSymbolData(curX, partitionSymbolY, GetPartitionInnerName(partition),
                    partition.prirep.toUpperCase() + partition.shard, () => { this.OnPartitionClick(partition) }
                ))

                indexSet.add(partition.index)
                curX += partitionSymbolGap
            })

            // 插入index图形
            let indexSymbolGap = maxX / (indexSet.size + 1)
            curX = indexSymbolGap
            i = 0
            indexSet.forEach((indexName) => {
                this.indexInfoDict.get(indexName).color = randomColor()
                dataList.push(GetIndexSymbolData(curX, indexSymbolY, indexName, 'index ' + i,
                    this.indexInfoDict.get(indexName).color,
                    () => { this.OnIndexClick(indexName) }))
                i++
                curX += indexSymbolGap
            })
            return dataList
        },
        // 生成箭头
        GetLinkList() {
            let linkList = []

            // 添加partition到node的箭头
            this.nodeInfoDict.forEach((nodeInfo) => {
                let nodeInnerName = GetNodeInnerName(nodeInfo.node)
                nodeInfo.partitions.forEach((partition) => {
                    let partitionInnerName = GetPartitionInnerName(partition)
                    linkList.push({
                        source: partitionInnerName,
                        target: nodeInnerName,
                        lineStyle: { width: 2, opacity: 1 }
                    })
                })
            })

            this.indexInfoDict.forEach((indexInfo) => {
                let indexInnerName = indexInfo.name
                indexInfo.partitions.forEach((partition) => {
                    let partitionInnerName = GetPartitionInnerName(partition)
                    linkList.push({
                        source: partitionInnerName,
                        target: indexInnerName,
                        lineStyle: { width: 2, color: indexInfo.color, opacity: 0.7 }
                    })
                })
            })

            return linkList
        },
        InitChart() {
            this.chart = echarts.init(this.$refs.chart)
            let dataList = this.GetDataList()
            let linkList = this.GetLinkList()
            console.log('dataList:', dataList)
            let option = {
                title: { text: '分片统计' },
                series: {
                    type: 'graph',
                    layout: 'none',
                    coordinatesystem: 'cartesian2d',
                    roam: true,
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [5, 5],
                    // itemStyle: { join: 'miter', miterLimit: 20 },
                    // lineStyle: { join: 'miter', miterLimit: 20 },
                    label: {
                        show: true
                    },
                    data: dataList,
                    links: linkList
                }
            }
            option && this.chart.setOption(option)
            this.chart.on('click', function (params) {
                // console.log('onclick: ', params)
                let data = params.data
                if (data.onclick !== undefined) {
                    data.onclick()
                }
            })
        },
        OnNodeClick(node) {
            this.tableData = []
            console.log('OnNodeClick:', node);
            let partitions = this.nodeInfoDict.get(node.masterName).partitions
            console.log('partitions:', partitions)
            partitions.forEach(partition => {
                this.tableData.push(partition)
            })
        },
        OnPartitionClick(partition) {
            this.tableData = [partition]
            console.log('OnPartitionClick:', partition)
        },
        OnIndexClick(indexName) {
            this.tableData = []
            console.log('OnIndexClick:', indexName)
            let partitions = this.indexInfoDict.get(indexName).partitions
            partitions.forEach(partition => {
                this.tableData.push(partition)
            })
        }
    },


}
</script>