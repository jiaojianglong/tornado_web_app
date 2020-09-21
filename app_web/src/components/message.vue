<template>
    <div class="box">
        <div class="box-header">
            <h3 class="box-title">
                消息列表
            </h3>
        </div>
        <div class="box-body">
            <div
                v-if="messages.length == 0"
                class="panel-body">
                暂无消息
            </div>
            <div
                v-for="(message, index) in messages"
                :key="index"
                class="panel-body"
                style="border-bottom:1px solid #ddd;">
                <i
                    class="fa fa-check-circle text-green pull-right"
                    title="已读"
                    @click="clean(index)" />
                {{ message.text }}
            </div>
        </div>
    </div>
</template>

<script>

 export default {
     data () {
         return {
             messages: this.$store.state.messages
         }
     },
     methods: {
         clean: function(index) {
             this.messages.splice(index, 1);
         }
     }
 }
</script>
