<template>
  <div>
    <!-- 面包屑导航 -->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>商品管理</el-breadcrumb-item>
      <el-breadcrumb-item>商品分类</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片视图区 -->
    <el-card>
      <el-row>
        <el-col>
          <el-button type="primary" @click="showAddCateDialog">添加分类</el-button>
        </el-col>
      </el-row>
      <!-- 表格 -->
      <tree-table class="treeTable" :show-row-hover="false" border index-text='#'
                  :columns="columns" :selection-type="false" :expand-type="false"
                  :show-index="true"
                  :data="catelist.slice((queryInfo.pagenum-1)*queryInfo.pagesize,queryInfo.pagenum*queryInfo.pagesize)">
        <!-- 是否有效 -->
        <template slot="isok" slot-scope="scope">
          <i  v-if="scope.row.cate_delete===false" class="el-icon-success"
          style="color: lightgreen;"></i>
          <i v-else class="el-icon-error" style="color: lightgreen;"></i>
        </template>
        <!-- 排序 -->
        <template slot="order" slot-scope="scope">
          <el-tag size="mini" v-if="scope.row.cate_level === 0">一级</el-tag>
          <el-tag type="success" v-else-if="scope.row.cate_level === 1">二级</el-tag>
          <el-tag type="warning" v-else>三级</el-tag>
        </template>
        <!-- 操作 -->
        <template slot="opt">
          <el-button type="primary" icon="el-icon-edit" size="mini">编辑</el-button>
          <el-button type="danger" icon="el-icon-delete" size="mini">删除</el-button>
        </template>
      </tree-table>
      <!-- 分页区 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.pagenum"
        :page-sizes="[2, 3, 10, 15]"
        :page-size="queryInfo.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>
    </el-card>
    <!-- 添加分类的对话框 -->
    <el-dialog
      title="添加分类"
      :visible.sync="addCateDialogVisible"
      width="70%" @close="addCateDialogClosed">
      <!-- 添加分类的表单 -->
      <el-form :model="addCateForm" :rules="addCateFormRules" ref="addCateFormRef" label-width="100px">
        <el-form-item label="分类名称:" prop="cate_name">
          <el-input v-model="addCateForm.cate_name"></el-input>
        </el-form-item>
        <el-form-item label="父级分类:" >
          <!-- options 用来指定数据源 -->
          <!-- props 用来指定配置对象 -->
          <el-cascader
            change-on-select
            :checkStrictly = "true"
            :clearable="true"
            expand-trigger="hover"
            v-model="selectedKeys"
            :options="parentCateList"
            :props="cascaderProps"
            @change="parentCateChanged"></el-cascader>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="addCateDialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="addCate">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>
<script>
export default {
  data () {
    return {
      // 查询条件
      queryInfo: {
        type: 3,
        pagenum: 1,
        pagesize: 2
      },
      // 商品分类的数据列表，默认为空
      catelist: [],
      // 总数据条数
      total: 0,
      // 为table指定列的定义
      columns: [
        {
          label: '分类名称',
          prop: 'cate_name'
        },
        {
          label: '是否有效',
          // 表示，将当前列定义为模版
          type: 'template',
          // 表示当前这一列使用的模版名称
          template: 'isok'
        },
        {
          label: '排序',
          type: 'template',
          template: 'order'
        },
        {
          label: '操作',
          type: 'template',
          template: 'opt'
        }
      ],
      // 控制添加分类对话框的显示与隐藏
      addCateDialogVisible: false,
      // 添加分类的表单数据对象
      addCateForm: {
        // 将要添加的分类的名称
        cate_name: '',
        // 父级分类ID
        cate_pid: 0,
        // 分类的等级，默认要添加的是1级分类
        cate_level: 0
      },
      // 添加分类表单的验证规则对象
      addCateFormRules: {
        cate_name: [
          { required: true, message: '请输入分类名称', trigger: 'blur' }
        ]
      },
      // 父级分类的列表
      parentCateList: [],
      // 指定级联选择器的配置对象
      cascaderProps: {
        value: 'cate_id',
        label: 'cate_name',
        children: 'children'
      },
      // 选中的父级分类的ID数组
      selectedKeys: []
    }
  },
  created () {
    this.getCateList()
  },
  methods: {
    // 获取商品分类数据
    async getCateList () {
      const { data: res } = await this.$http.get('categories', { params: this.queryInfo })
      if (res.meta.status !== 200) {
        return this.$message.error('获取商品分类失败')
      }
      // console.log(res)
      // 把数据列表赋值给catelist
      this.catelist = res.data.result
      console.log(this.catelist)
      // 为总数据条数赋值
      this.total = res.data.total
    },
    // 监听pagesize的页码
    handleSizeChange (newSize) {
      this.queryInfo.pagesize = newSize
      this.getCateList()
      console.log(this.queryInfo.pagesize)
    },
    // 监听最新的page页码值
    handleCurrentChange (newPage) {
      this.queryInfo.pagenum = newPage
      this.getCateList()
      console.log(this.queryInfo.pagenum)
    },
    // 点击按钮，展示添加分类的对话框
    showAddCateDialog () {
      // 先获取父级分类的数据列表
      this.getParentCateList()
      // 再展示出对话框
      this.addCateDialogVisible = true
    },
    // 获取父级分类的数据列表
    async getParentCateList () {
      const { data: res } = await this.$http.get('categories', {
        params: { type: 2 }
      })
      if (res.meta.status !== 200) {
        return this.$message.error('获取父级分类数据失败')
      }
      // console.log(res.data)
      this.parentCateList = res.data
    },
    // 选择项发生变化触发这个函数
    parentCateChanged () {
      console.log(this.selectedKeys)
      // 如果selectedKeys 数组中的 length 大于0，证明选中的父级分类
      // 反之，就说明没有选中任何父级分类
      if (this.selectedKeys.length > 0) {
        // 父级分类的ID
        this.addCateForm.cate_pid = this.selectedKeys[this.selectedKeys.length - 1]
        // 为当前的分类的等级赋值
        this.addCateForm.cate_level = this.selectedKeys.length
        // return;
      } else {
        // 父级分类的ID
        this.addCateForm.cate_pid = 0
        // 为当前的分类的等级赋值
        this.addCateForm.cate_level = 0
      }
    },
    // 点击按钮，添加新的分类
    addCate () {
      console.log(this.addCateForm)
      this.$refs.addCateFormRef.validate(
        async valid => {
          if (!valid) return
          const { data: res } = await this.$http.post('categories', this.addCateForm)
          if (res.meta.status !== 201) {
            return this.$message.error('添加分类失败!')
          }
          this.$message.success('添加分类成功!')
          this.getCateList()
          this.addCateDialogVisible = false
        }
      )
    },
    // 监听对话框的关闭事件，重置表单数据
    addCateDialogClosed () {
      this.$refs.addCateFormRef.resetFields()
      // 清空父级分类的ID
      this.addCateForm.cate_pid = 0
      // 清空当前的分类的等级赋值
      this.addCateForm.cate_level = 0
      // 清空父级关联的数组
      this.selectedKeys = []
      // console.log(1111)
    }
  }
}
</script>
<style lang="less" scoped>
  .treeTable {
    margin-top: 15px;
  }
  .el-cascader {
    width: 100%
  }
</style>
