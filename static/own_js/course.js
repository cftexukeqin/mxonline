function Course() {

}
Course.prototype.listenAddCommentEvent = function(){
    var addcommentBtn = $('#js-pl-submit');
    var textarea = $("textarea[name='comment']");
    addcommentBtn.click(function (event) {
        var self = this;
        event.preventDefault();
        var course_id = addcommentBtn.parent().attr('data-id');
        var comments = $('#comments-area').val();
        // console.log(comments);
        // console.log(course_id);
        xfzajax.post({
            'url':'/course/addcomment/',
            'data':{
                'course_id':course_id,
                'comments':comments
            },
            'success':function (result) {
                if(result['code'] === 200){
                    // console.log(result['data'])
                    var comment = result['data'];
                    var tpl = template('comment-item',{'comment':comment});
                    var commentsGroup = $('.mod-post');
                    commentsGroup.prepend(tpl);
                    textarea.val("");
                    console.log("成功!");
                    messageBox.showSuccess("评论发表成功!")
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