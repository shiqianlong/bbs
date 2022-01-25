var RegisterHandle = function () {

};

RegisterHandle.prototype.listenSendCaptchaEvent = function () {
    var callback = function (event) {
        $("#email-captcha-btn").on('click', function (event) {
            var $this = $(this);
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
                    $this.off('click');
                    $this.attr('disabled', 'disabled');
                    var countdown = 6;
                    var interval = setInterval(function () {
                        if (countdown > 0) {
                            $this.text(countdown + 's后重新发送')
                        } else {
                            $this.text('发送验证码');
                            $this.attr('disabled', false);
                            $this.on('click', callback);

                            clearInterval(interval);
                        }
                        countdown--;
                    }, 1000)
                }
            })
        })
    };
    $("#email-captcha-btn").on("click", callback())
};

RegisterHandle.prototype.run = function () {
    this.listenSendCaptchaEvent()
};

$(function () {
    var handle = new RegisterHandle();
    handle.run()
});