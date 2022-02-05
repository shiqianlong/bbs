var PublicPostHandle = function () {
    var csrf_token = $('meta[name="csrf-token"]').attr('content');

    var editor = new window.wangEditor('#editor');
    editor.config.uploadImgServer = '/post/image/upload';
    editor.config.uploadFileName = "image";
    editor.config.uploadImgMaxSize = 1024 * 1024 * 3;
    editor.config.uploadImgHeaders = {
        'X-CSRFToken': csrf_token
    };

    editor.create()
};

PublicPostHandle.prototype.run = function () {

};

$(function () {
    var handle = new PublicPostHandle();
    handle.run()
});