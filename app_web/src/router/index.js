import Vue from 'vue'
import Router from 'vue-router'


Vue.use(Router);


function lazyload(name) {
    return function(resolve) {
        require(['@/components/' + name + '.vue'], resolve);
    };
}

var auth = ["user","group"].map(i => {
    return {
        path: '/auth/' + i,
        name:  'auth.' + i,
        component: lazyload("auth/" + i)
    };
});

var task = ["action","template", "task"].map(i => {
    return {
        path: '/task/' + i,
        name:  'task.' + i,
        component: lazyload("task/" + i)
    };
});

var routers = [
    {
        path: '/',
        name: 'index',
        component: lazyload("index")
    },
    {
        path: '/message',
        name: 'message',
        component: lazyload("message")
    }
];


routers.push(...auth);
routers.push(...task);

export default new Router({routes:routers})
