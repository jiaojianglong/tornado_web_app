<template>
    <el-container>
        <el-header>
            <h4>
                Group 列表
            </h4>
        </el-header>
        <el-main>
            <el-row
                type="flex"
                justify="end">
                <el-button type="primary" @click="add">新建群组</el-button>
            </el-row>
            <el-table
                :data="items"
                row-key="username"
                style="width: 100%"
            >
                <el-table-column
                    prop="groupname"
                    label="群组名"/>
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
                :title="is_update?'编辑群组':'创建群组'"
                :visible.sync="create_dialog"
                :close-on-click-modal="false">
                <el-form
                    :model="form"
                    label-position="right"
                    label-width="100px">
                    <el-form-item label="群组名">
                        <el-input v-model="form.groupname"/>
                    </el-form-item>
                    <el-form-item label="资源">
                        <el-card shadow="never"
                                 bodyStyle="padding:5px; max-height: 300px; overflow:auto">
                            <el-table
                                :data="sourceShow"
                                :show-header="false"
                                style="width: 100%">
                                <el-table-column
                                    prop="uri">
                                </el-table-column>
                                <el-table-column>
                                    <template slot-scope="scope">
                                        <el-checkbox-group v-model="scope.row.methods"
                                                           style="display: inline-block">
                                            <el-checkbox-button label="GET" key="GET">GET
                                            </el-checkbox-button>
                                            <el-checkbox-button label="POST" key="POST">POST
                                            </el-checkbox-button>
                                            <el-checkbox-button label="PUT" key="PUT">PUT
                                            </el-checkbox-button>
                                            <el-checkbox-button label="DELETE" key="DELETE">DELETE
                                            </el-checkbox-button>
                                        </el-checkbox-group>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </el-card>
                    </el-form-item>
                    <el-form-item label="用户">
                        <el-card shadow="never">
                            <el-checkbox-group v-model="form.users">

                                <el-checkbox
                                     v-for="item in users"
                                     :key="item.username"
                                     :label="item.username" border></el-checkbox>
                            </el-checkbox-group>
                        </el-card>
                        <!--<el-select v-model="form.users" multiple placeholder="请选择">-->
                            <!--<el-option-->
                                <!--v-for="item in users"-->
                                <!--:key="item.username"-->
                                <!--:label="item.username"-->
                                <!--:value="item.id">-->
                            <!--</el-option>-->
                        <!--</el-select>-->
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
                :role="role"/>
        </el-main>
        <el-footer>
            <el-row
                type="flex"
                justify="end">
                <paginate :pageinfo="pageinfo" @page-change="pageChange" @size-change="sizeChange"/>
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
                role: "auth.group",
                sources: [],
                users: [],
                method: ["GET", "POST", "DELETE", "PUT"],
                sourceShow: []
            }
        },
        watch: {
            "form.sources": function (new_val) {
                var sources = [];
                this.sources.forEach(item => {
                    var source_has = false;
                    if (new_val) {
                        for (var i = 0; i < new_val.length; i++) {
                            if (item === new_val[i].uri) {
                                source_has = true;
                                sources.push(new_val[i]);
                                break
                            }
                        }
                    }
                    if (!source_has) {
                        sources.push({
                            uri: item,
                            methods: []
                        })
                    }
                });
                this.sourceShow = sources
            },
            "sources": function (new_val) {
                var sources = [];
                new_val.forEach(item => {
                    var source_has = false;
                    if (this.form.sources) {
                        for (var i = 0; i < this.form.sources.length; i++) {
                            if (item === this.form.sources[i].uri) {
                                source_has = true;
                                sources.push(this.form.sources[i]);
                                break
                            }
                        }
                    }
                    if (!source_has) {
                        sources.push({
                            uri: item,
                            methods: []
                        })
                    }
                });
                this.sourceShow = sources
            }
        },
        created() {
            this.getSource();
            this.getUsers()
        },

        methods: {
            getSource() {
                API(this, "auth.source").default.get().then(res => {
                    this.sources = res.data.data
                })
            },
            addSelect() {
                this.form.sources = this.form.source ? this.form.source : [];
                this.form.sources.push(this.sourceSelect);
                this.sourceSelect = {}
            },
            getUsers() {
                API(this, "auth.user").default.get({page_size: -1}).then(res => {
                    this.users = res.data.data
                })
            },
            create: function () {
                var sources = []
                this.sourceShow.forEach(item => {

                        if (item.methods.length) {
                            sources.push(item)
                        }
                    }
                );
                this.form.sources = sources;
                return API(this, this.role).create(this.form).then((self, response) => {
                    self.create_dialog = false;
                    self.select();
                    self.reload();
                })
            },
            update: function () {
                var sources = []
                this.sourceShow.forEach(item => {

                        if (item.methods.length) {
                            sources.push(item)
                        }
                    }
                );
                this.form.sources = sources;
                return API(this, this.role).update(this.form).then((self, response) => {
                    self.create_dialog = false;
                    self.select();
                });
            },
            edit: function (index, row) {
                var users = [];
                row.users.forEach(item => {
                    users.push(item.username)
                })
                this.form = JSON.parse(JSON.stringify(row));
                this.form.users = users
                this.is_update = true;
                this.create_dialog = true
            },
            add: function () {
                this.form = {users:[]};
                this.is_update = false;
                this.create_dialog = true;
            },
        }
    }
</script>
