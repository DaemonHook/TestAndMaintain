<template>
  <div class="common-layout">
    <el-container style="min-height: 1080px; ">
      <el-aside width="200px" style="background-color: #E6E8EB;">
        <el-menu router :default-active="this.$route.path">
          <el-menu-item index="/q1" class="aside-menu-item">第一题</el-menu-item>
          <el-menu-item index="/q2" class="aside-menu-item">第二题</el-menu-item>
          <el-menu-item index="/q3" class="aside-menu-item">第三题</el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <RouterView></RouterView>
      </el-main>
    </el-container>
  </div>
</template>

<style>
.el-menu {
  align-items: center;
  justify-content: center;
}
</style>

<script scoped>
export default {
  methods: {
    handleSelect(key, keyPath) {
      console.log(`key: ${key}, keyPath: ${keyPath}`)
    }
  }
}
</script>
