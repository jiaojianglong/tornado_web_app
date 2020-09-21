<template>
    <el-pagination
        :current-page="pageinfo.page"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="pageinfo.per_page"
        :total="pageinfo.per_page*pageinfo.pages"
        layout="sizes, prev, pager, next, jumper"
        style="padding:15px"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange" />
</template>


<script>

 export default {
     data: function() {
         return {}
     },
     inject: ['pageinfo','select'],
     methods: {
         handleSizeChange: function(val){
             this.pageinfo.per_page = val;
             this.select()
         },
         handleCurrentChange: function(val){
             this.pageinfo.page = val;
             this.select()
         }
     }
 }
</script>
