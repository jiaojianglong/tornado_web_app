import axios, {api} from '@/api';

var user_ = {
    self: function() {
        return axios.get(api.auth.user);
    },
    login: function(params) {
        return axios.post(api.auth.userLogin, params)
    },
    logout: function() {
        return axios.post(api.auth.userLogout)
    }
};
export const  user = Object.assign(
    api.default(api.auth.user),
    user_
);

export var group = {
    get: function(params) {
        return axios.get(api.account.group,{
            params:params
        });
    },
    put: function(pk,params) {
        return axios.put(api.account.group + "/" + pk, params);
    },
    post: function(params) {
        return axios.post(api.account.group, params);
    },
    delete: function(pk) {
        return axios.delete(api.account.group + "/" + pk);
    },
    self: function() {
        return axios.get(api.account.groupself);
    }
};

export var resource = {
    get: function() {
        return axios.get(api.account.resource);
    },
};
