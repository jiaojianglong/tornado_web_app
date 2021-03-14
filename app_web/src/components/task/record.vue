<template>
    <div id="taskList">
        <el-row :gutter="50">
            <el-col :span="12">
                <el-table
                    :data="items"
                    @row-click="selectTask"
                    style="width: 100%; height:505px">
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
            <el-col :span="12" style="height:545px; overflow-y: auto">
                <el-timeline>
                    <el-timeline-item v-for="action in taskLog" timestamp="" placement="top">
                        <h4 style="display: inline-block; margin-right: 10px">
                            {{action.name + "-" + action.action_code}}</h4>
                        <el-tag :type="status_type[action.action_log.status]"
                                style="margin-right: 10px">{{action.action_log.status}}
                        </el-tag>
                        <i class="el-icon-loading" v-if="action.action_log.status=='executing'"
                           style="color:#409EFF"></i>

                        <i class="el-icon-arrow-down" v-if="showLogs.indexOf(action.id) != -1" @click="showLog(action)"></i>
                        <i class="el-icon-arrow-right" v-else @click="showLog(action)"></i>
                        <div v-if="showLogs.indexOf(action.id) != -1">
                            <pre v-for="log in action.action_log.logger">{{log.time + "-" + log.message}}</pre>
                        </div>
                    </el-timeline-item>
                </el-timeline>
                <!--</div>-->
            </el-col>
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
                taskLog: [],
                items: [],
                activeNames: [],
                showLogs: []
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
            },
            selectTask(row, column, event) {
                console.log(row);
                API(this, "task.task_log").default.get({task_id: row.id}).then(res => {
                    this.taskLog = res.data.data;
                })
            },
            showLog(action){
                var index = this.showLogs.indexOf(action.id);
                if (index != -1){
                    this.showLogs.splice(index, 1);
                }else{
                    this.showLogs.push(action.id)
                }

            }
        }
    }
</script>
