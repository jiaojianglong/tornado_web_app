<template>
    <div id="App">
        <div v-if="$store.state.is_login && get_info_end" style="height:100%; width: 100%">
        <el-container >
            <el-header
                id="main-header"
                height="50px">
                <el-row style="width:200px; display: inline-block">
                    <el-col :span="8">
                        <el-image
                            style="height: 45px;width:45px;display: inline-block; margin-top: 5px"
                            :src="logo"
                            @click="$router.push('/')"
                            fit="contain"></el-image>

                    </el-col>
                    <el-col :span="16">
                        <h3 style="display: inline-block; line-height: 50px">管理后台</h3>
                    </el-col>
                </el-row>
                <userInfo style="float: right; width:50px; display: inline-block"></userInfo>
            </el-header>
            <el-container>
                <el-aside width="200px">
                    <el-menu
                        default-active="1"
                        router
                        class="el-menu-vertical-demo"
                        background-color="#1e282c"
                        text-color="#fff"
                        active-text-color="#ffd04b">
                        <!--<el-menu-item index="/">-->
                        <!--<i class="el-icon-s-home"></i>-->
                        <!--<span slot="title">任务管理</span>-->
                        <!--</el-menu-item>-->
                        <el-submenu index="/rpa">
                            <template slot="title">
                                <i class="el-icon-location"></i>
                                <span>账号管理</span>
                            </template>
                            <el-menu-item index="/auth/user">用户管理</el-menu-item>
                            <el-menu-item index="/auth/group">群组管理</el-menu-item>
                        </el-submenu>
                    </el-menu>
                </el-aside>
                <el-main>
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-container>
            </div>
        <el-container v-else-if="!$store.state.is_login">
            <user-login></user-login>
        </el-container>
    </div>
</template>


<script>
    import logo from '@/assets/logo.png'
    import user_logo from '@/assets/user_logo.png'
    import {lazyload} from '@/utils';
    import {API} from '@/service';

    export default {
        name: 'App',
        components: {
            'userInfo': lazyload('auth/userInfo'),
            'userLogin': lazyload('auth/user_login'),
        },
        data: function () {
            return {
                logo: logo,
                user_logo:user_logo,
                get_info_end:false,
            }
        },
        created(){
            this.getUserInfo()
        },
        watch:{
            "$store.state.is_login": function(new_val){
                this.getUserInfo()
            }
        },
        methods: {
            getUserInfo(){
                API(this, "auth.user").default.getItem("self").then(res => {
                    if(res.status ==200){
                        this.$store.commit("USER_INFO", res.data.data);
                        this.$store.commit("LOGIN_STATUS", true);
                        this.get_info_end = true
                    }
                })
            }

        },
    }
</script>

<style>
    * {
        margin: 0;
        padding: 0;
    }

    #main-header {
        background-color: #409EFF;
        color: white;
    }

    html, body, #App {
        width: 100%;
        height: 100%;
    }

    .el-container {
        height: 100%;
    }

    .el-aside {
        height: 100%;
        background-color: #1e282c;
    }
</style>
