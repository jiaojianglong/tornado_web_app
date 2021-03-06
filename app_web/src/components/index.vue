<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="4" v-for="app in apps">

                <el-link :href="getPath(app)" target="_blank"
                         style="display: block; width:100%">
                    <el-card shadow="never" bodyStyle="padding:5px">
                        <el-row type="flex" justify="space-between">
                            <el-col :span="12">
                                <el-image
                                    style="height:40px; display: inline-block; margin: 5px"
                                    :src="getLogo(app)"
                                    fit="contain"></el-image>
                            </el-col>
                            <el-col :span="8">
                                <h3 style="line-height: 50px; align-content: center; margin: auto">
                                    {{app}}</h3>
                            </el-col>
                        </el-row>
                    </el-card>
                </el-link>

            </el-col>
        </el-row>
    </div>
</template>

<script>
    import {mixin} from "@/mixin"
    import {API} from '@/service';
    import myadminLogo from '@/assets/myadmin.png'
    import portainerLogo from '@/assets/portainer.png'
    import seafileLogo from '@/assets/seafile.png'
    import swaggerLogo from '@/assets/swagger.svg'

    export default {
        mixins: [mixin],
        data: function () {
            return {
                is_local: window.location.host.indexOf("aixiaochu") == -1,
                host: window.location.host.indexOf("aixiaochu") == -1 ? "http://127.0.0.1" : window.location.host,
                path: {
                    myadmin: {local: '8080', online: "myadmin", logo: myadminLogo},
                    portainer: {local: '9000', online: "portainer", logo: portainerLogo},
                    seafile: {local: '8899', online: "seafile", logo: seafileLogo},
                    swagger: {local: '8081', online: "swagger", logo: swaggerLogo},
                },
                apps: [
                    "myadmin",
                    "portainer",
                    "seafile",
                    "swagger"
                ]
            }
        },
        methods: {
            getPath(name) {
                if (this.is_local) {
                    return "http://127.0.0.1:" + this.path[name].local
                } else {
                    return this.path[name].online+".aixiaochu.nat300.top:7441"
                }
            },
            getLogo(name) {
                return this.path[name].logo
            }
        }
    }

</script>
