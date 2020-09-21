<template>
    <div>
        <el-row style="float: right; width:50px; display: inline-block" @click="$router.push('/')">
            <el-col>
                <el-popover
                    placement="bottom"
                    width="200"
                    trigger="hover">
                    <el-button @click="logout">logout</el-button>
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

    export default {
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
