var RegisterHandle = function () {

};

RegisterHandle.prototype.listenSendCaptchaEvent = function () {
    $("#email-captcha-btn").on('click', function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;
        if (!email || !reg.test(email)) {
            alert('请输入正确格式的邮箱！');
            return;
        }
        zlajax.get({
            url: '/email/captcha?email=' + email,
            success: function (data) {
                console.log(data)
            }
        })
    })
};

RegisterHandle.prototype.run = function () {
    this.listenSendCaptchaEvent()
};

$(function () {
    var handle = new RegisterHandle();
    handle.run()
});