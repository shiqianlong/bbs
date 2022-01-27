var SettingHandler = function () {

};

SettingHandler.prototype.listenAvatarUploadEvent = function () {
    $("#avatar-input").on("change", function () {
        var image = this.files[0];
        var formData = new FormData();
        formData.append("image", image);
        zlajax.post({
            url: "/avatar/upload",
            data: formData,
            // 如果使用jQuery上传文件，那么还需要指定以下两个参数
            processData: false,
            contentType: false,
            success: function (result) {
                if (result['code'] == 200) {
                    // result = {"code": 200, "data": {"avatar": "/xxx"}}
                    var avatar = result['data']['avatar'];
                    var avatar_url = "/media/avatars/" + avatar;
                    $("#avatar-img").attr("src", avatar_url);
                }
            }
        })
    });
};


SettingHandler.prototype.run = function () {
    this.listenAvatarUploadEvent();
};

$(function () {
    var handler = new SettingHandler();
    handler.run();
});