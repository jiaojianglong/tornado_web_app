<template>
    <el-container>
        <el-header>
            <h4>
                User 列表
            </h4>
        </el-header>
        <el-main>
            <el-row
                type="flex"
                justify="end">
                <el-button type="primary" @click="add">新建用户</el-button>
            </el-row>
            <el-table
                :data="items"
                row-key="username"
                style="width: 100%"
                >
                <el-table-column
                    prop="username"
                    label="用户名" />
                <el-table-column
                    prop="email"
                    label="邮箱" />
                <el-table-column label="群组">
                    <template slot-scope="scope">
                        <el-tag
                            style="margin-right: 5px"
                            v-for="group in scope.row.groups">
                            {{group.groupname}}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="createtime"
                    label="创建时间">
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
                :title="is_update?'编辑用户':'创建用户'"
                :visible.sync="create_dialog"
                :close-on-click-modal="false">
                <el-form
                    :model="form"
                    label-position="right"
                    label-width="100px">
                    <el-form-item label="用户名">
                        <el-input v-model="form.username" />
                    </el-form-item>
                    <el-form-item label="邮箱">
                        <el-input v-model="form.email" />
                    </el-form-item>
                    <el-form-item label="密码" v-if="!is_update">
                        <el-input v-model="form.password" show-password/>
                    </el-form-item>
                    <el-form-item label="群组">
                        <el-card shadow="never">
                            <el-checkbox-group v-model="form.groups">
                                <el-checkbox
                                     v-for="item in groups"
                                     :key="item.groupname"
                                     :label="item.groupname" border></el-checkbox>
                            </el-checkbox-group>
                        </el-card>
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
        mixins: [mixin],
        data() {
            return {
                role: "auth.user",
                groups: []
            }
        },

        created() {
            this.getGroups()
        },

        methods: {
            getGroups(){
                API(this, "auth.group").default.get({page_size:-1}).then(res => {
                    this.groups = res.data.data
                })
            },
            create: function () {
                return API(this, this.role).create(this.form).then((self, response) => {
                    self.create_dialog = false;
                    self.select();
                    self.reload();
                })
            },
            update: function () {
                return API(this, this.role).update(this.form).then((self, response) => {
                    self.create_dialog = false;
                    self.select();
                });
            },
            edit: function (index, row) {
                var groups = [];
                row.groups.forEach(item => {
                    groups.push(item.groupname)
                })
                this.form = JSON.parse(JSON.stringify(row));
                this.form.groups = groups
                this.is_update = true;
                this.create_dialog = true
            },
            add: function () {
                this.form = {groups:[]};
                this.is_update = false;
                this.create_dialog = true;
            },
        },
    }
</script>
