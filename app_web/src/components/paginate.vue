<template>
    <el-pagination
        :current-page="pageinfo.page"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="pageinfo.page_size"
        :total="pageinfo.total"
        layout="sizes, prev, pager, next, jumper"
        style="padding:15px"
        @size-change="$emit('size-change', $event)"
        @current-change="$emit('page-change', $event)" />
</template>


<script>

 export default {
     data: function() {
         return {}
     },
     props: ["pageinfo"],
 }
</script>
