import {API} from '@/service';
import {lazyload} from '@/utils';
import {datetimeTrim} from '@/utils';


export var mixin = {
        components: {
            'delete-modal': lazyload('delete'),
            'paginate': lazyload('paginate'),
            'loading': lazyload('loading'),
            'noresult': lazyload('noresult')
        },
        data: function () {
            var page_size = 10;
            var height = $(window).height();
            if (height > 1024) {
                page_size = 30;
            }else if (height > 720) {
                page_size = 20;
            }
            return {
                pageinfo: {
                    page: 1,
                    total: 60,
                    page_size: page_size
                },
                items: [],
                form: {},
                is_loading: true,
                reload_: true,
                create_dialog: false,
                filter: {},
                deletedialogVisible: false,
                is_update: false,
                item_data:{}
            };
        },
        created: function () {
            this.pre();
        },

        methods: {

            pre: function () {
                if (this.role) {
                    this.select();
                }
            },
            select: function () {
                var params = {};
                params.page_size = this.pageinfo.page_size;
                params.page = this.pageinfo.page;
                if (this.filter) {
                    Object.keys(this.filter).forEach(key => {
                        params[key] = this.filter[key];
                    })
                }
                return API(this, this.role).get(params);

            },
            add: function () {
                this.form = {};
                this.is_update = false;
                this.create_dialog = true;
            },
            reload: function () {
                this.reload_ = false;
                this.$nextTick(() => {this.reload_ = true
            })
            },
            create: function () {
                return API(this, this.role).create(this.form).then((self, response) => {
                    self.form = {};
                self.create_dialog = false;
                self.select();
                self.reload();
            })
            },
            update: function () {
                return API(this, this.role).update(this.form).then((self, response) => {
                    self.form = {};
                self.create_dialog = false;
                self.select();
            })
                ;
            },
            edit: function (index, row) {
                this.form = row;
                this.is_update = true;
                this.create_dialog = true
            },
            remove: function (index, id) {
                this.$store.commit("DELETE", {
                    id: id,
                    index: index
                });
                this.$refs.deletemodal.deletedialogVisible = true;
            },
            delete: function () {
                return API(this, this.role).delete().then((self, response) => {
                    self.$refs.deletemodal.deletedialogVisible = false;
                self.$store.commit("RESET");
                self.select();
            })
            },

            getitem: function (id) {
                return API(this, this.role).getitem(id).then(
                    (self, response)=>{
                        self.item_data = response.data.data;
                        self.select();
                    })
            },
            pageChange: function(page){
                this.pageinfo.page = page;
                this.select();
            },
            sizeChange: function (page_size) {
                console.log("123", page_size);
                this.pageinfo.page_size = page_size;
                this.select();
            },

            format_time: function(shijianchuo) {
                //shijianchuo是整数，否则要parseInt转换
                function add0(m){return m<10?'0'+m:m }
                var time = new Date(shijianchuo*1000);
                var y = time.getFullYear();
                var m = time.getMonth() + 1;
                var d = time.getDate();
                var h = time.getHours();
                var mm = time.getMinutes();
                var s = time.getSeconds();
                return y + '-' + add0(m) + '-' + add0(d) + ' ' + add0(h) + ':' + add0(mm) + ':' + add0(s);
            }
        },
        provide: function () {
            return {
                father_delete: this.delete,
                pageinfo: this.pageinfo,
                select: this.select
            }
        }
        ,
    }
;
