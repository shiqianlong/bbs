var PublicPostHandle = function () {
    var editor = new window.wangEditor('#editor');
    editor.create()
};

PublicPostHandle.prototype.run = function () {

};

$(function () {
    var handle = new PublicPostHandle();
    handle.run()
});