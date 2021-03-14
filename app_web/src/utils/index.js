import Vue from 'vue'

if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'? args[number]: match;
        });
    };
}

if(!String.prototype.trim) {
    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g, '');
    };
}

function isInArray(value, array) {
    return array.indexOf(value) > -1;
}

export function MessageRecord(self, options) {
    var icon = "fa-check";
    var color = "green";
    if (options.type == "warn") {
        icon = "fa-warning";
        color= "yellow";
    }else if (options.type == "error") {
        color= "red";
    }
    self.$store.commit("MESSAGE", {
        text: options.message,
        icon: icon,
        color: color
    });
}

export function lazyload(name) {
    return function(resolve) {
        require(['@/components/' + name], resolve);
    };
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


export var HTTP = {
    OK: function(self, msg) {
        var options = {
            type: 'success'
        };
        if (typeof msg === "undefined") {
            options.message = "success";
        }else if (typeof msg.response === "undefined") {
            options.message = msg;
        }else {
            options.message = msg.response.data.message;
        }
        MessageRecord(self, options);
        if (typeof self.$message === "undefined") {
            return Vue.$message(options);
        }
        return self.$message(options);
    },
    ERROR: function(self, msg) {
        var options = {
            type: 'warn'
        };
        if (typeof msg.response === "undefined") {
            options.message = msg;
        }else if ([404,403,500].indexOf(msg.response.status) > -1 ){
            options.type = "error";
            if ("message" in msg.response.data) {
                // satori 的接口
                options.message = msg.response.data.message.slice(0,1000);
            } else if ("error" in msg.response.data) {
                // satori 转发的 eneru 接口
                options.message = msg.response.data.error;
            }
        }else {
            if ("message" in msg.response.data) {
                // satori 的接口
                options.message = msg.response.data.message.slice(0,1000);
            } else if ("error" in msg.response.data) {
                // satori 转发的 eneru 接口
                options.message = msg.response.data.error;
            }
        }
        if ($('#create-modal') && $('#create-modal').hasClass('in') ){
            if( $('#create-modal').children("#satori-notification-hide").length === 0) {
                $('#create-modal').append($("#satori-notification-hide"));
            }
            $("#create-modal > #satori-notification-hide").css("display", "block");
            options.group = "hide";
        }
        MessageRecord(self, options);
        if (typeof self.$message === "undefined") {
            return Vue.$message(options);
        }
        return self.$message(options);
    }
};
import { Message } from 'element-ui';
export function notify(data) {
    var opt = {
        message: data
    }
    if (data == "success") {
        opt.type = "success"
    } else {
        opt.type = "error"
    }
    Message(opt)
}

export function operateConfirm(vm, operateDes, callback) {
    return new Promise( function (resolve) {
        vm.$confirm('确定' + operateDes + '?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
            callback().then( res => {
                if (res.status >= 200 && res.status < 300) {
                    vm.$message({
                        type: 'success',
                        message: operateDes + '成功!'
                    });
                }
                resolve();
            })
        }).catch(() => {
            vm.$message({
                type: 'info',
                message: '取消' + operateDes
            });
        });
    } );
}

export const datetimeTrim = function (datetimeStr) {

    return datetimeStr.replace(/UTC/g, '').replace(/T/g, ' ').
            replace(/Z/g,'').replace(/\+\S+/g, '').replace(/\.\d+/g, '');
};


