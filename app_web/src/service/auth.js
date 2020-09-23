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

export var group = api.default(api.auth.group);

export var source = api.default(api.auth.source);
