<template>
    <el-container>
        <el-header>
            <h4>
                动作列表
            </h4>
        </el-header>
        <el-main>
            <el-row
                type="flex"
                justify="end">
                <el-button type="primary" @click="add">新建动作</el-button>
            </el-row>
            <el-table
                :data="items"
                row-key="name"
                style="width: 100%"
                >
                <el-table-column
                    prop="name"
                    label="动作名" />
                <el-table-column
                    prop="action_code"
                    label="动作脚本" />
                <el-table-column
                    prop="description"
                    label="描述" />
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
                :title="is_update?'编辑动作':'创建动作'"
                :visible.sync="create_dialog"
                :close-on-click-modal="false">
                <el-form
                    :model="form"
                    label-position="right"
                    label-width="100px">
                    <el-form-item label="动作名">
                        <el-input v-model="form.name" />
                    </el-form-item>
                    <el-form-item label="描述">
                        <el-input v-model="form.description" />
                    </el-form-item>
                    <el-form-item label="动作脚本">
                        <el-select v-model="form.action_code" placeholder="请选择">
                            <el-option
                              v-for="item in actionCodes"
                              :key="item.action_code"
                              :label="item.action_code"
                              :value="item.action_code">
                            </el-option>
                          </el-select>
                    </el-form-item>
                    <el-form-item label="动作参数">
                        <parameter_operate v-if="!is_update" v-model="current_action_params" mode="params_show"></parameter_operate>
                        <parameter_operate v-else v-model="form.params" mode="params_show"></parameter_operate>
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
                role: "task.action",
                actionCodes: [],
                current_action_params:[]
            }
        },
        watch: {
            "form.action_code": function (val) {
                if (!val){this.current_action_params=[];return}
                this.actionCodes.forEach(item => {
                    if (item.action_code == val){
                        this.current_action_params = item.params
                    }
                })

            }
        },

        created() {
            this.getActionCodes()
        },

        methods: {
            getActionCodes(){
                API(this, "task.action_code").default.get({page_size:-1}).then(res => {
                    this.actionCodes = res.data.data
                })
            },
            create: function () {
                this.form.params = this.current_action_params;
                return API(this, this.role).create(this.form).then((self, response) => {
                    self.form = {};
                self.create_dialog = false;
                self.select();
                self.reload();
            })
            },
        },
    }
</script>
