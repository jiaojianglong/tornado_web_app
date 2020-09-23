<template>
    <el-dialog
        title="删除提示"
        :visible.sync="deletedialogVisible"
        width="30%">
        <slot name="content">
            <span>{{ message }}</span>
        </slot>

        <span
            slot="footer"
            class="dialog-footer">
            <el-button @click="deletedialogVisible = false">取 消</el-button>
            <el-button
                type="primary"
                @click="father_delete">
                确 定
            </el-button>
        </span>
    </el-dialog>
</template>

<script>

    export default {
        props: {
            name: {
                type: String,
                default: ''
            },
            role: {
                type: String,
                default: ''
            },
            message: {
                // 当使用插槽时，message 将不生效
                type: String,
                default: '确定删除？'
            },
            id: {
                type: String,
                default: 'delete-modal'
            },
        },
        inject: ['father_delete'],
        data() {
            return {
                deletedialogVisible: false
            }
        },
    }
</script>
