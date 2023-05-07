<template>
    <div class="cluster">
        <h3>cluster</h3>
        <el-row>
            <el-col :span="8" v-for="(node,index) in nodes" :key="index">
                <div class="node">
                    <p>{{ node.name }}</p>
                    <el-row>
                        <el-col :span="8" v-for="(shard,index) in shards" :key="index">
                            <div v-if="shard.flag">
                                <div class="shardp">
                                    <p>{{ shard.prirep+shard.number }}</p>
                                </div>
                            </div>
                            <div v-else>
                                <div class="shardr">
                                    <p>{{ shard.prirep+shard.number }}</p>
                                </div>
                            </div>
                        </el-col>
                    </el-row>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default{
    data(){
        return{
            nodes:[
                {
                    name:"data-node-01"
                },
                {
                    name:"data-node-02"
                },
                {
                    name:"data-node-03"
                },
                {
                    name:"data-node-04"
                },
                {
                    name:"data-node-05"
                },
                {
                    name:"data-node-06"
                }
            ],
            shards:[
                {
                    number:"0",
                    prirep:"P",
                    flag:1
                },
                {
                    number:"1",
                    prirep:"R",
                    flag:0
                },
                {
                    number:"2",
                    prirep:"R",
                    flag:0
                }
            ]
        }
    }
}
</script>

<style scoped>
.cluster{
    border: 1px solid var(--el-border-color);
    border-radius: 8px;
    width: 90%;
    margin: auto;
    margin-top: 10px;
    box-shadow: var(--el-box-shadow-lighter);
    text-align: center;
}
.node{
    border: 2px solid var(--el-border-color);
    border-radius: 4px;
    width: 90%;
    margin: auto;
    margin-bottom: 8px;
    background-color: #c6e2ff;
}
.shardp{
    border: 2px dashed var(--el-border-color);
    border-radius: 4px;
    width: 90%;
    margin: auto;
    background-color: #d9ecff;
}
.shardr{
    border: 2px dashed var(--el-border-color);
    border-radius: 4px;
    width: 90%;
    margin: auto;
    background-color: #e1f3d8;
}
</style>