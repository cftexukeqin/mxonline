function Auth() {

}
// geetest
function Geetest(){

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

// 注册代码
Auth.prototype.listenRegistBtn = function(){
    var regBtn = $('#regist-btn');
    var emailInput = $("input[name='email']");
    var passwordInput = $("input[name='password']");
    regBtn.click(function (event) {
        event.preventDefault();
        var email = emailInput.val();
        var password = passwordInput.val();
        xfzajax.post({
            'url':'/user/regist/',
            'data':{
                'email':email,
                'password':password
            },
            'success':function (result) {
                if(result['code'] === 200){
                    messageBox.showSuccess('注册成功,请前往注册邮箱激活!')
                }else {
                    messageBox.showInfo(result['message'])
                }
                },
             'fail':function (err) {
                 messageBox.showError(err)
             }
        })
    })
};
// 初始化验证码
// Auth.prototype.listenGeetestLogin = function(){
//     var usernameInput = $('#username1');
//     var passwordInput = $('#password1');
//     var handlerPopup = function (captchaObj) {
//         captchaObj.onSuccess(function () {
//             var validate = captchaObj.getValidate();
//             var username = usernameInput.val();
//             var password = passwordInput.val();
//             xfzajax.post({
//                 'url':'/user/login/',
//                 'data':{
//                     'username':username,
//                     'password':password,
//                     'geetest_challenge':validate.geetest_challenge,
//                     'geetest_validate':validate.geetest_validate,
//                     'geetest_second':validate.geetest_second,
//                 },
//                 'success':function (result) {
//                     if (result['code'] === 200){
//                         window.location.href = '/';
//                     } else {
//                         messageBox.showInfo(result['msg'])
//                     }
//                 },
//                 'fail':function (err) {
//                     messageBox.showError(err)
//                 }
//             })
//         });
//         $('#popup-submit').click(function () {
//             captchaObj.show();
//         });
//         captchaObj.appendTo('#popup-captcha');
//     };
//     xfzajax.get({
//         'url':'/user/pc-geetest/login/?t='+(new Date()).getTime(),
//         'data':{},
//         'success':function (result) {
//             initGeetest({
//                 gt:result.gt,
//                 challenge:result.challenge,
//                 product:'popup',
//                 offline:!result.success
//             },handlerPopup);
//         }
//     })
// };
// geetest 初始化
// Geetest.prototype.Init = function(){
//     console.log("success init");
//     xfzajax.get({
//         'url':'/user/pc-geetest/login/?t='+(new Date()).getTime(),
//         'data':{},
//         'success':function (result) {
//             initGeetest({
//                 gt:result.gt,
//                 challenge:result.challenge,
//                 product:'popup',
//                 offline:!result.success
//             },window.hp);
//         }
//     })
// };


Auth.prototype.run = function () {
    // 无极验验证码版本
    // this.listenLogindBtn();
    // this.listenRegistBtn();
    // this.listenGeetestLogin();
};

$(function () {
    var auth = new Auth();
    auth.run();
});