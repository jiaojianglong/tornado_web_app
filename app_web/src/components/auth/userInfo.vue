<template>
    <div>
        <el-row style="float: right; width:50px; display: inline-block" @click="$router.push('/')">
            <el-col>
                <el-popover
                    placement="bottom"
                    width="200"
                    trigger="hover">
                    <el-form label-position="right">
                        <el-form-item label="用户名">
                            <p>{{$store.state.user_info.username}}</p>
                        </el-form-item>
                        <el-form-item label="邮箱">
                            <p>{{$store.state.user_info.email}}</p>
                        </el-form-item>
                    </el-form>
                    <el-button @click="logout" style="float:right" type="danger">退出登录</el-button>
                    <el-avatar :src="user_logo" slot="reference" style="margin-top: 5px"></el-avatar>
                </el-popover>

            </el-col>
        </el-row>
    </div>
</template>

<script>
    import user_logo from '@/assets/user_logo.png'
    import {mixin} from "@/mixin"
    import {API} from '@/service';
    import ElFormItem from "../../../node_modules/element-ui/packages/form/src/form-item.vue";

    export default {
        components: {ElFormItem},
        mixins: [mixin],
        data: function () {
            return {
                user_logo: user_logo,
            }
        },
        methods: {
            logout: function(){
                API(this, "auth.user").default.logout().then(res =>{
                    this.$store.commit("LOGIN_STATUS", false);
                })
            }
        }
    }
</script>
