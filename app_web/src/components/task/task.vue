<template>
    <div>
        <el-card style="max-height: 300px;" bodyStyle="padding:10px" shadow="never">
            <el-card v-for="template in templates"
                     style="width:250px; display: inline-block; margin-right: 20px;"
                     body-style="background: #EBEEF5;"
                     @click="selectTemplate(template)"
                     shadow="hover">
              <div>{{template.name}}</div>
              <div style="font-size: 12px; margin-top: 5px">描述：{{template.description}}</div>
              <div style="font-size: 12px">操作人：{{template.user.username}}</div>
              <div style="font-size: 12px">更新时间：{{template.updatetime}}</div>
            </el-card>
        </el-card>
        <el-card style="height:680px; margin-top: 20px" shadow="never">
            <el-timeline>
                <el-timeline-item v-for="action in template.actions" timestamp="" placement="top">
                  <el-card>
                    <h4>{{action.name}}</h4>
                    <p>{{action.params}}</p>
                  </el-card>
                </el-timeline-item>
            </el-timeline>
        </el-card>
    </div>
</template>

<script>
    import {API} from '@/service'
    import {HTTP} from '@/utils';
    import {api} from "@/api";
    import {mixin} from "@/mixin";
    import {lazyload} from '@/utils';
    import ElCard from "../../../node_modules/element-ui/packages/card/src/main.vue";

    export default {
        components: {
            ElCard,
            'parameter_operate': lazyload('task/params'),
        },
        mixins: [mixin],
        data() {
            return {
                role: "task.task",
                templates:[],
                template:{}
            }
        },
        created() {
            this.getTemplates()
        },

        methods: {
            getTemplates(){
                API(this, "task.template").default.get({page_size:-1}).then(res => {
                    this.templates = res.data.data
                })
            },
            selectTemplate(template){
                this.template = template;
            }
        },
    }
</script>
