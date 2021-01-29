<template>
  <el-container>
    <el-header>
      <div>
        <img src="../assets/gsl.png" alt="" width="45px" height="45px">
        <span>电商管理平台</span>
      </div>
      <div>
        <el-button type="info" @click="logout">退出</el-button>
      </div>
    </el-header>
    <el-container>
      <!--      // 侧边栏-->
      <el-aside :width="isCollapse? '64px':'200px'">
          <div class="toggle-button" @click="toggleCollapse" >|||</div>
          <!--          // 侧边栏菜单区域-->
          <el-menu
            :default-active="activePath"
            :router="true"
            :collapse-transition="false"
            :collapse="isCollapse"
            :unique-opened="true"
            background-color="#333744"
            text-color="#fff"
            active-text-color="#409BFF">
            <!--            一级菜单  index 后面只接受字符串 不接受数字 -->
            <el-submenu :index="item.id+''" v-for="item in menulist" :key="item.id">
              <!-- 一级菜单模版区 -->
              <template slot="title">
                <!-- 图标 -->
                <i :class="iconsObj[ item.id ]"></i>
                <!-- 文本 -->
                <span>{{ item.authName }}</span>
              </template>
              <!-- 二级菜单 -->
              <el-menu-item @click="saveNavState('/' + subItem.path)" :index="'/' + subItem.path + ''" v-for="subItem in item.children" :key="subItem.id">
                <i class="el-icon-menu"></i>
                <span>{{ subItem.authName }}</span>
              </el-menu-item>
            </el-submenu>
          </el-menu>
      </el-aside>
      <el-main>
        <!--        路由占位符-->
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>
<script>
export default {
  data () {
    return {
      // 左侧菜单数据
      menulist: [],
      iconsObj: {
        1: 'iconfont icon-kehu',
        2: 'iconfont icon--shangpinguanli1',
        3: 'iconfont icon-daizi-',
        4: 'iconfont icon-wodedingdan',
        5: 'iconfont icon-ico_bb_zj_zzt'
      },
      isCollapse: false,
      // 被激活的链接
      activePath: ''
    }
  },
  created () {
    this.getMenuList()
    this.activePath = window.sessionStorage.getItem('activePath')
  },
  methods: {
    logout () {
      window.sessionStorage.clear()
      this.$router.push('/login')
    },
    // 获取所有菜单
    async getMenuList () {
      const { data: res } = await this.$http.get('menus')
      // console.log(res.meta)
      if (res.meta.state !== 200) return this.$message.error(res.meta.msg)
      this.menulist = res.data
      // console.log(res)
    },
    // 点击按钮切换菜单的折叠与展开
    toggleCollapse () {
      // console.log(this.isCollapse)
      this.isCollapse = !this.isCollapse
    },
    // 点击高亮
    saveNavState (activePath) {
      window.sessionStorage.setItem('activePath', activePath)
      this.activePath = activePath
    }
  }
}
</script>
<style lang="less" scoped>
  .el-container {
    height: 100%;
  }
  .el-header {
    background-color: #373d41;
    display: flex;
    justify-content: space-between;
    padding-left: 20px;
    font-size: 20px;
    color:white;
    div {
      display: flex;
      align-items: center;
      span {
        margin-left: 15px;
      }
    }
    img {
      border-radius: 50%;
    }
  }
  .el-aside {
    background-color: #333744;
    .el-submenu span {
      font-size: 15px;
    }
    .el-menu-item span {
      font-size: 10px;
    }
  }
  .el-main {
    background-color: #eaedf1;
  }

  .iconfont {
    margin-right:10px;
  }

  .el-menu {
    border-right:1px;
  }
  .toggle-button {
    background-color: #4A5064;
    font-size: 10px;
    line-height: 10px;
    color:#fff;
    text-align: center;
    letter-spacing: 0.2em;
    cursor:pointer;
  }
</style>
