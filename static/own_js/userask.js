function Organization() {

}

Organization.prototype.listenUserAskEvent = function(){
    var askBtn = $('#ask-btn');
    var nameInput = $("input[name='name']");
    var mobileInput = $("input[name='mobile']");
    var courseInput = $("input[name='course_name']");

    askBtn.click(function (event) {
        event.preventDefault();
        var name = nameInput.val();
        var mobile = mobileInput.val();
        var course_name = courseInput.val();
        if(!name){
            window.messageBox.showError("输入姓名");
            return;
        }
        if(!mobile) {
            window.messageBox.showError("输入手机号");
            return;
        }
        if (!course_name) {
            window.messageBox.showError("输入课程名");
            return;
        }
        if (!(/^1[35789]\d{9}$/.test(mobile))) {
            window.messageBox.showError('请输入正确的手机号！');
            return;
        }
        xfzajax.post({
            'url':'/org/ask/',
            'data':{
                'name':name,
                'mobile':mobile,
                'course_name':course_name
            },
            'success':function (result) {
                if(result['code'] === 200){
                    window.messageBox.showSuccess("提问成功!")
                }else {
                    console.log(result['msg'])
                }
            },
            'fail':function (error) {
                console.log(error)
            }
        })
    })
};

Organization.prototype.run = function () {
    this.listenUserAskEvent();
};

$(function () {
   var org = new Organization();
   org.run();
});