var PublicPostHandle = function () {
    var csrf_token = $('meta[name="csrf-token"]').attr('content');

    var editor = new window.wangEditor('#editor');
    editor.config.uploadImgServer = '/post/image/upload';
    editor.config.uploadFileName = "image";
    editor.config.uploadImgMaxSize = 1024 * 1024 * 3;
    editor.config.uploadImgHeaders = {
        'X-CSRFToken': csrf_token
    };

    editor.create();
    this.editor = editor
};

PublicPostHandle.prototype.listenSubmitEvent = function () {
    var that = this;
    $('#submit-btn').on('click', function (event) {
        event.preventDefault();
        var title = $('input[name="title"]').val();
        var board_id = $('select[name="board_id"]').val()
        var content = that.editor.txt.html();
        zlajax.post({
            'url': '/post/public',
            'data': {
                title,
                content,
                board_id
            },
            success: function (result) {
                if (result['code'] == 200) {
                    let post_id = result['data']['id'];
                    window.location = '/post/detail/' + post_id
                } else {
                    alert(result['message'])
                }
            }
        })
    })
}

PublicPostHandle.prototype.run = function () {
    this.listenSubmitEvent();
};

$(function () {
    var handle = new PublicPostHandle();
    handle.run()
});