<template>
    <tr v-if="show">
        <td
            :colspan="colspan"
            class="satori-noresult">
            暂无结果
        </td>
    </tr>
</template>

<style>
 .satori-noresult {
     text-align:center;
     color:#999;
     background-color: #fff;
 }
</style>

<script type="text/javascript">
 export default {
     props: {
         show: Boolean,
         colspan: {
           type: Number,
           required: true
         }
     },
 }
</script>
