<template>
    <div :id="mode">
        <el-form :inline="true" class="demo-form-inline">
            <el-form-item v-for="parameter in params" :label="parameter.show_name">
                <el-select
                    v-if="parameter.options"
                    v-model="parameter.value"
                    @change="$emit('change', params)"
                    :multiple="parameter.type=='list'?true:false">
                    <el-option
                      v-for="item in parameter.options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
                </el-select>
                <el-input-number v-else-if="parameter.type && parameter.type=='int'"
                                 @change="$emit('change', params)"
                                 v-model="parameter.value"></el-input-number>
                <el-switch v-else-if="parameter.type && parameter.type=='bool'"
                           @change="$emit('change', params)"
                           v-model="parameter.value"></el-switch>
                <el-input v-else v-model="parameter.value"
                          @change="$emit('change', params)"
                          placeholder="请输入内容" ></el-input>

                <el-tooltip v-if="parameter.describe" class="item" effect="dark" :content="parameter.describe" placement="top-start">
                  <i class="el-icon-question" style="margin-left:3px; font-size:16px"></i>
                </el-tooltip>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>

    export default {
        model: {
            prop: 'params',
            event: 'change'
        },
        props: {
            mode: {
                type: String,
                default: "params_show"
            },
            params: {
                type: Array,
                default: []
            },
        },
        data() {
            return {
            }
        },
    }
</script>
