<template>
    <el-container>
        <el-header>
            <h4>
                模板列表
            </h4>
        </el-header>
        <el-main>
            <el-row
                type="flex"
                justify="end">
                <el-button type="primary" @click="add">新建模板</el-button>
            </el-row>
            <el-table
                :data="items"
                row-key="name"
                style="width: 100%"
                >
                <el-table-column
                    prop="name"
                    label="模板名" />
                <el-table-column
                        prop="description"
                    label="模板描述" />
                <el-table-column label="创建者">
                    <template slot-scope="scope">
                        <span v-if="scope.row.user">{{scope.row.user.username}}</span>
                    </template>
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
                    label="操作"
                    style="float:right;"
                    width="150px">
                    <template slot-scope="scope">
                        <el-button
                            @click="edit(scope.$index, scope.row)">
                            编辑
                        </el-button>
                        <el-button
                            type="danger"
                            @click="remove(scope.$index, scope.row.id)">
                            删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-dialog
                :title="is_update?'编辑模板':'创建模板'"
                :visible.sync="create_dialog"
                :close-on-click-modal="false">
                <el-form
                    :model="form"
                    label-position="right"
                    label-width="100px">
                    <el-form-item label="模板名">
                        <el-input v-model="form.name" />
                    </el-form-item>
                    <el-form-item label="模板描述">
                        <el-input v-model="form.description" />
                    </el-form-item>
                    <el-form-item label="模板动作">
                        <el-select
                            filterable
                            placeholder="请选择动作"
                            @change="choiceAction">
                            <el-option
                                v-for="item in actions_all"
                                :key="item.name"
                                :label="item.name"
                                :value="item.id" />
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <div
                            style="display: inline-block; width:100%;height:400px;border: 1px solid #DCDFE6;overflow-y: auto">
                            <div style="padding: 10px;">
                                    <el-card
                                        v-for="action in actions"
                                        :key="action.value"
                                        shadow="hover"
                                        body-style="padding:5px 15px"
                                        style="margin:5px 0">
                                        <div>
                                            <span
                                                style="cursor:pointer;color:#409EFF;font-size: 18px;">
                                                {{ action.name }}-{{action.action_code}}
                                            </span>
                                            <i
                                            class="el-icon-circle-close"
                                            style="color:#F56C6C;float:right;font-size: 18px;"
                                            @click="deleteAction(action)" />
                                        </div>
                                        <div>
                                            <span>
                                                {{action.description}}
                                            </span>
                                        </div>
                                    </el-card>
                            </div>
                        </div>
                    </el-form-item>
                </el-form>
                <div
                    slot="footer"
                    class="dialog-footer">
                    <el-button @click="create_dialog = false">
                        取 消
                    </el-button>
                    <el-button
                        type="primary"
                        v-if="!is_update"
                        @click="create">
                        确 定
                    </el-button>
                    <el-button
                        v-else
                        type="primary"
                        @click="update">
                        确 定
                    </el-button>
                </div>
            </el-dialog>
            <delete-modal
                ref="deletemodal"
                :name="'项目'"
                :role="role" />
        </el-main>
        <el-footer>
            <el-row
                type="flex"
                justify="end">
                <paginate :pageinfo="pageinfo" @page-change="pageChange" @size-change="sizeChange" />
            </el-row>
        </el-footer>
    </el-container>
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
                role: "task.template",
                actions: [],
                actions_all: [],
                current_action_params:[]
            }
        },

        created() {
            this.getActions()
        },

        methods: {
            getActions(){
                API(this, "task.action").default.get({page_size:-1}).then(res => {
                    this.actions_all = res.data.data
                })
            },
            choiceAction: function (val) {
                this.select_action = "";
                let select_action = {};
                this.actions_all.forEach(item => {
                    if (val == item.id) {
                        select_action = JSON.parse(JSON.stringify(item))
                    }
                });
                this.actions.push(select_action)
            },
            deleteAction: function(action){
                this.actions.splice(this.actions.indexOf(action), 1)
            },
            create: function () {
                this.form.actions = this.actions;
                return API(this, this.role).create(this.form).then((self, response) => {
                    self.form = {};
                self.create_dialog = false;
                self.select();
                self.reload();
            })},
            edit: function (index, row) {
                this.form = JSON.parse(JSON.stringify(row));
                this.actions = this.form.actions;
                this.is_update = true;
                this.create_dialog = true
            },
        },
    }
</script>
