<template>
    <div id="taskList">
        <el-table
            :data="taskList"
            style="width: 100%"
            :row-class-name="tableRowClassName">
            <el-table-column
                prop="date"
                label="模板"
                width="180">
            </el-table-column>
            <el-table-column
                prop="name"
                label="操作人"
                width="180">
            </el-table-column>
            <el-table-column
                prop="address"
                label="配置">
            </el-table-column>
        </el-table>
    </div>
</template>

<script>

    export default {
        model: {
            prop: 'taskList',
        },
        props: {
            taskList: {
                type: Array,
                default: []
            },
        },
        data() {
            return {}
        },
        methods: {
            tableRowClassName({row, rowIndex}) {
                if (row.status==='unexecute') {
                    return 'info-row'
                }else if (row.status==='success') {
                    return 'success-row'
                }
            }
        }
    }
</script>
