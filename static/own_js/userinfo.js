function User() {

}

// 修改密码
User.prototype.listenResetPassword = function(){
  var resetBtn = $('#resetpwd-btn');
  var pwd1Input = $("input[name='password1']");
  var pwd2Input = $("input[name='password2']");

  resetBtn.click(function (event) {
      event.preventDefault();
      var pwd1 = pwd1Input.val();
      var pwd2 = pwd2Input.val();

      if (pwd1 != pwd2) {
          messageBox.showInfo("两次密码不一致!");
          return;
      }
      xfzajax.post({
          'url':'/user/pwdreset/',
          'data':{
              'pwd1':pwd1,
              'pwd2':pwd2
          },
          'success':function (reslut) {
              if (reslut['code'] === 200){
                  messageBox.showSuccess("修改成功!");
                  var bgdialog = $('#dialogBg');
                  var resetdialog = $('#jsResetDialog');
                  bgdialog.hide();
                  resetdialog.hide();
              }
          },
          'fail':function (err) {
              messageBox.showError(err)
          }
      })
  })
};

// 修改个人信息
User.prototype.listenModifyInfo = function () {
    var modifyBtn = $('#save-btn');
    var nicknameInput = $("input[name='nick_name']");
    var birthdayInput = $("input[name='birday']");
    var gender = $("input:radio[name='gender']:checked").val();
    var addressInput = $("input[name='address']");
    var telephoneInput = $("input[name='mobile']");
    var emailInput = $("input[name='email']");


    modifyBtn.click(function (event) {
        event.preventDefault();
        var nickname = nicknameInput.val();
        var birday = birthdayInput.val();
        var address = addressInput.val();
        var telephone = telephoneInput.val();
        var email = emailInput.val();
        console.log(birday);
        xfzajax.post({
            'url':'/user/save/info/',
            'data':{
                'nick_name':nickname,
                'birthday':birday,
                'gender':gender,
                'address':address,
                'mobile':telephone,
                'email':email
            },
            'success':function (result) {
                if(result['code'] === 200){
                    messageBox.showSuccess("个人信息修改成功!")
                }else {
                    messageBox.showInfo(result['msg'])
                }
            },
            'fail':function (err) {
                messageBox.showError(err)
            }
        })

    })
};

User.prototype.run = function () {
    var self = this;
    this.listenResetPassword();
    this.listenModifyInfo();
};

$(function () {
    var user = new User();
    user.run();
});