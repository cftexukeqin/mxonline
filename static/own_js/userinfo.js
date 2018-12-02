function User() {

}

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

User.prototype.run = function () {
    var self = this;
    this.listenResetPassword();
};

$(function () {
    var user = new User();
    user.run();
});