import * as auth from '@/service/auth';
import {HTTP} from '@/utils';

var _api = {
    auth:auth,
};

export function API(self, key) {
    var apis = key.split(".");
    var api = _api[apis[0]][apis[1]];
    return {
        default: api,
        create: function(params, callback) {
            return new Promise(resolve => {
                api.post(params).then(response => {
                    if (! response) return;
                    if (typeof callback !== "undefined") {
                        callback(self, response);
                    }else {
                        self.items.push(response.data.data);
                        HTTP.OK(self);
                    }
                    return resolve(self, response);
                }).catch(error => {
                    return HTTP.ERROR(self, error);
                });
            });
        },
        update: function(params, callback) {
            return new Promise(resolve => {
                api.put(params.id,params).then(response => {
                    if (! response) return;
                    if (typeof callback !== "undefined") {
                        callback(self, response);
                    }else {
                        // self.items.splice(self.$store.state.delete.index,1,response.data.data);
                        HTTP.OK(self);
                    }
                    return resolve(self, response);
                }).catch(error => {
                    return HTTP.ERROR(self, error);
                });
            });
        },
        delete: function() {
            return new Promise(resolve => {
                if (self.$store.state.delete.id !== 0){
                    api.delete(self.$store.state.delete.id).then(response => {
                        if (! response) return;
                        self.items.splice(self.$store.state.delete.index,1);
                        HTTP.OK(self);
                        return resolve(self, response);
                    }).catch(error => {
                        return HTTP.ERROR(self, error);
                    });
                }
            });
        },
        get: function(params, callback, loading) {
            if ((typeof loading !== "undefined") && !loading) {
                self.is_loading = false;
            }else {
                self.is_loading = true;
            }
            return new Promise(resolve => {
                api.get(params).then(response => {
                    self.is_loading = false;
                    if (! response) return;
                    if (typeof callback !== "undefined") {
                        return callback(self, response);
                    }else {
                        self.items = response.data.data;
                        self.pageinfo = response.data.pageinfo;
                    }
                    return resolve(self, response);
                }).catch(error => {
                    self.is_loading = false;
                    return HTTP.ERROR(self, error);
                });
            });
        },
        getItem: function(pk, params, callback) {
            return new Promise(resolve => {
                api.getItem(pk, params).then(response => {
                    if (! response) return;
                    if (typeof callback !== "undefined") {
                        return callback(self, response);
                    }else {
                        self.item = response.data.data;
                    }
                    return resolve(self, response);
                }).catch(error => {
                    return HTTP.ERROR(self, error);
                });
            });
        },
    };
}
