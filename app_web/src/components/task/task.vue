<template>
    <div>
        <el-card style="max-height: 300px;" bodyStyle="padding:10px" shadow="never">
            <el-card v-for="template in templates"
                     style="width:250px; display: inline-block; margin-right: 20px;"
                     body-style="background: #EBEEF5;"
                     shadow="hover">
                <div @click="selectTemplate(template)">
                    <div>{{template.name}}</div>
                    <div style="font-size: 12px; margin-top: 5px">描述：{{template.description}}</div>
                    <div style="font-size: 12px">操作人：{{template.user.username}}</div>
                    <div style="font-size: 12px">更新时间：{{template.updatetime}}</div>
                </div>
            </el-card>
        </el-card>
        <el-card style="height:680px; margin-top: 20px;" shadow="never">
            <el-row style="margin-bottom: 20px">
                <el-col :span="3"><h3>模板: {{template.name}}</h3></el-col>
                <el-col :span="3"><h3>操作人：{{template.user.username}}</h3></el-col>
                <el-col :span="17"><h3>描述：{{template.description}}</h3></el-col>
                <el-col :span="1">
                    <el-button type="primary" @click="execute">执行</el-button>
                </el-col>
            </el-row>
            <el-tabs v-model="activeName" style="height:590px">
                <el-tab-pane label="执行配置" name="params" style="height:550px;">
                    <el-row style="width:100%;height:100%;" :gutter="50">
                        <el-col :span="12" style="height:100%; overflow-y: auto">
                            <el-table
                                :data="items"
                                @row-click="editParams"
                                style="width: 100%">
                                <el-table-column
                                    prop="name"
                                    label="name"
                                    width="180">
                                </el-table-column>
                                <el-table-column
                                    prop="createtime"
                                    label="创建时间">
                                </el-table-column>
                                <el-table-column
                                    prop="updatetime"
                                    label="更新时间">
                                </el-table-column>
                                <el-table-column
                                    align="right">
                                    <template slot="header" slot-scope="scope">
                                        <el-button type="primary" @click="newParams">新建</el-button>
                                    </template>
                                    <template slot-scope="scope">
                                        <el-button
                                            size="mini"
                                            type="danger"
                                            @click="remove(scope.$index, scope.row.id)">删除
                                        </el-button>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-col>
                        <el-col :span="12" style="height:100%; overflow-y: auto">
                            <el-row style="width:90%">
                                <el-col :span="23">
                                    <div class="demo-input-suffix">
                                        配置名：
                                        <el-input style="width:60%" :disabled="!paramsEdit" v-model="form.name"
                                                  placeholder="请输入内容"></el-input>
                                    </div>
                                </el-col>
                                <el-col :span="1">
                                    <el-button v-if="!paramsEdit" @click="paramsEdit=true" type="primary">编辑</el-button>
                                    <el-button v-else @click="paramsEdit=false" type="primary">取消编辑</el-button>
                                </el-col>
                            </el-row>
                            <el-timeline style="margin-top: 20px">
                                <el-timeline-item v-for="action in form.actions" timestamp=""
                                                  placement="top">
                                    <h4>{{action.name}}</h4>
                                    <parameter_operate v-model="action.params" :disabled="!paramsEdit"
                                                       mode="params_show"></parameter_operate>
                                </el-timeline-item>
                            </el-timeline>
                            <el-button type="primary" v-if="is_update" @click="update">保存</el-button>
                            <el-button type="primary" v-else @click="create">保存</el-button>
                        </el-col>
                    </el-row>

                </el-tab-pane>
                <el-tab-pane label="执行记录" name="tasklist">

                </el-tab-pane>
            </el-tabs>

        </el-card>
        <delete-modal
                ref="deletemodal"
                :name="'项目'"
                :role="role" />
    </div>
</template>

<script>
    import {API} from '@/service'
    import {HTTP} from '@/utils';
    import {api} from "@/api";
    import {mixin} from "@/mixin";
    import {lazyload} from '@/utils';

    export default {
        components: {
            'parameter_operate': lazyload('task/params'),
        },
        mixins: [mixin],
        data() {
            return {
                role:"task.params",
                templates: [],
                template: {},
                paramsList: [],
                activeName: "params",
                paramsEdit: false
            }
        },
        created() {
            this.getTemplates()
        },

        methods: {
            getTemplates() {
                API(this, "task.template").default.get({page_size: -1}).then(res => {
                    this.templates = res.data.data;
                    this.selectTemplate(this.templates[0])
                })
            },
            selectTemplate(template) {
                this.template = template;
                this.filter.template_id = this.template.id;
                this.select();
                this.newParams();
            },
            createParams() {
                API(this, "task.params").default.post(this.template).then(res => {
                    if (res.code === 200) {
                        HTTP.OK(res.data.message)
                    } else {
                        HTTP.ERROR(res.data.message)
                    }
                })
            },
            newParams() {
                this.form.actions = this.template.actions;
                this.form.template_id = this.template.id;
                this.form.name = "";
                this.paramsEdit = true;
                this.is_update=false;
            },
            editParams(row, column, event) {
                this.form = {};
                this.form = row;
                this.is_update=true;
                this.paramsEdit =false;
            },
            execute(){}
        },
    }
</script>
