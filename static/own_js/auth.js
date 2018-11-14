function Auth() {

}

Auth.prototype.listenLogindBtn = function(){
    var regBtn = $('#login-btn');
    var usernameInput = $("input[name='username']");
    var passwordInput = $("input[name='password']");
    regBtn.click(function (event) {
        event.preventDefault();
        var username = usernameInput.val();
        var password = passwordInput.val();
        xfzajax.post({
            'url':'/user/login/',
            'data':{
                'username':username,
                'password':password
            },
            'success':function (result) {
                if(result['code'] === 200){
                    window.location.href = '/';
                    // messageBox.showSuccess("登录成功!")
                }else {
                    messageBox.showError(result['message'])
                }
            },
            'fail':function (err) {
                xfzalert.alertInfoToast(err)
            }
        })
    })
};

// Auth.prototype.listenRegistBtn = function(){
//     var regBtn = $('#regist-btn');
//     var emailInput = $("input[name='email']");
//     var passwordInput = $("input[name='password']");
//     regBtn.click(function (event) {
//         event.preventDefault();
//         var email = emailInput.val();
//         var password = passwordInput.val();
//         xfzajax.post({
//             'url':'/user/regist/',
//             'data':{
//                 'email':email,
//                 'password':password
//             },
//             'success':function (result) {
//                 if(result['code'] === 200){
//                     messageBox.showSuccess('注册成功,请前往注册邮箱激活!')
//                 }else {
//                     messageBox.showInfo(result['message'])
//                 }
//                 },
//              'fail':function (err) {
//                  messageBox.showError(err)
//              }
//         })
//     })
// };
// 初始化验证码


Auth.prototype.run = function () {
    this.listenLogindBtn();
    this.listenLogindBtn();
    // this.listenRegistBtn();
};

$(function () {
    var auth = new Auth();
    auth.run();
});