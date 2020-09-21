<template>
    <el-row style="width:100%">
        <el-col :span="10">
            <div style="height:600px;"/>
        </el-col>
        <el-col
            :span="4"
            style="margin-top: 200px;min-width: 320px;">
            <h1 style="color:#66b1ff; text-align: center; margin-bottom: 50px">
                运维平台
            </h1>
            <el-form
                ref="form"
                :model="form">
                <el-form-item>
                    <el-input
                        v-model="form.username"
                        placeholder="用户名"/>
                </el-form-item>
                <el-form-item>
                    <el-input
                        v-model="form.password"
                        placeholder="密码"
                        show-password/>
                </el-form-item>
            </el-form>

            <el-button
                type="primary"
                style="width:100%"
                @click="login">
                登录
            </el-button>
        </el-col>
        <el-col :span="9"/>
    </el-row>
</template>
<script>
    import {mixin} from "@/mixin"
    import {API} from '@/service';

    export default {
        mixins: [mixin],
        data: function () {
            return {
            }
        },
        methods: {
            login(){
                API(this, "auth.user").default.login(this.form).then(res => {
                    console.log(res)
                    this.$store.commit("LOGIN_STATUS", true);
                })
            },
        }
    }
</script>

