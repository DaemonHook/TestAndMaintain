<template>
  <el-container class="layout-container-demo" style="height: 100%">
    <el-aside width="300px">
      <el-scrollbar>
        <el-menu>
          
          <router-link to="/">
            <el-menu-item index="1">
            <template #title>
              Question One
            </template>
          </el-menu-item>
          </router-link>
          
          <router-link to="/question2">
            <el-menu-item index="2">
            <template #title>
              Question Two
            </template>
          </el-menu-item>
          </router-link>
          
          <router-link to="/question3">
            <el-menu-item index="3">
            <template #title>
              Question Three
            </template>
          </el-menu-item>
          </router-link>

        </el-menu>
      </el-scrollbar>
    </el-aside>

    <el-container>
      <el-header style="text-align: right; font-size: 20px">
        <div class="toolbar">
          <!-- <el-dropdown>
            <el-icon style="margin-right: 8px; margin-top: 1px"><setting/></el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>View</el-dropdown-item>
                <el-dropdown-item>Add</el-dropdown-item>
                <el-dropdown-item>Delete</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown> -->
          <span>1.2 大数据Elasticsearch集群智能运维系统</span>
        </div>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { Menu as IconMenu, Message, Setting } from '@element-plus/icons-vue'

</script>

<style scoped>
.layout-container-demo .el-header {
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
}
.layout-container-demo .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
}
.layout-container-demo .el-menu {
  border-right: none;
}
.layout-container-demo .el-main {
  padding: 0;
}
.layout-container-demo .toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}
</style>