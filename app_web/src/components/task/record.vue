<template>
    <div id="taskList">
        <el-row :gutter="50">
            <el-col :span="12">
                <el-table
                    :data="items"
                    style="width: 100%; height:480px">
                    <el-table-column label="模板">
                        <template slot-scope="scope">
                            <p>{{scope.row.template.name}}</p>
                        </template>
                    </el-table-column>
                    <el-table-column label="配置">
                        <template slot-scope="scope">
                            <p>{{scope.row.params.name}}</p>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作人">
                        <template slot-scope="scope">
                            <p>{{scope.row.user.username}}</p>
                        </template>
                    </el-table-column>
                    <el-table-column
                        prop="createtime"
                        label="创建时间">
                    </el-table-column>
                    <el-table-column label="状态">
                        <template slot-scope="scope">
                            <el-tag effect="dark" :type="status_type[scope.row.status]">
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>

                </el-table>
                <paginate :pageinfo="pageinfo" @page-change="pageChange" @size-change="sizeChange"/>
            </el-col>
            <el-col :span="12">123</el-col>
        </el-row>
    </div>
</template>

<script>
    import {API} from '@/service'
    import {HTTP} from '@/utils';
    import {api} from "@/api";
    import {mixin} from "@/mixin";
    import {lazyload} from '@/utils';

    export default {
        mixins: [mixin],
        props: {
            templateId: {
                type: Number,
                default: 3
            },
        },
        data() {
            return {
                role: "task.task",
                status_type: {
                    success: "success",
                    failed: "danger",
                    executing: "primary",
                    unexecute: "info",
                    waiting: "info",
                    cancel: "info",
                },
            }
        },
        watch: {
            templateId: function (val) {
                this.filter.template_id = val;
                this.items = [];
                this.select()
            }
        },
        methods: {
            tableRowClassName({row, rowIndex}) {
                if (row.status === 'unexecute') {
                    return 'info-row'
                } else if (row.status === 'success') {
                    return 'success-row'
                }
            }
        }
    }
</script>
