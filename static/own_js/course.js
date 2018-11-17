function Course() {

}
Course.prototype.listenAddCommentEvent = function(){
    var addcommentBtn = $('#js-pl-submit');
    addcommentBtn.click(function (event) {
        var self = this;
        event.preventDefault();
        var course_id = addcommentBtn.parent().attr('data-id');
        var comments = $('#js-pl-textarea').val();
        console.log(comments);
        console.log(course_id);
        xfzajax.post({
            'url':'/course/addcomment/',
            'data':{
                'course_id':course_id,
                'comments':comments
            },
            'success':function (result) {
                if(result['code'] === 200){
                    messageBox.showSuccess("发表评论成功!")
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


Course.prototype.run = function () {
    this.listenAddCommentEvent();
};

$(function () {
    var course = new Course();
    course.run();
});