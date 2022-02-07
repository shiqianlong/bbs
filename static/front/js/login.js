var LoginHandle = function () {

};

LoginHandle.prototype.listenLoginEvent = function () {
    $('#submit-btn').on('click', function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        var password = $("input[name='password']").val();
        var remember = $('input[name="remember"]').prop('checked')

        zlajax.post({
            url: '/login',
            data: {
                email,
                password,
                remember: remember ? 1 : 0
            },
            success: function (result) {
                if (result['code'] == 200) {
                    var token = result['data']['token'];
                    var user = result['data']['user'];
                    localStorage.setItem('JWT_TOKEN_KEY', token);
                    localStorage.setItem('USER_KEY', JSON.stringify(user));
                    window.location = '/'
                } else {
                    alert(result['message'])
                }
            }
        })
    })
};

LoginHandle.prototype.run = function () {
    this.listenLoginEvent();
};

$(function () {
    var handle = new LoginHandle();
    handle.run()
})