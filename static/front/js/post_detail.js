$(function () {
    hljs.highlightAll();

    $('#comment-btn').on('click', function (event) {
        var $this = $(this)
        event.preventDefault();
        var content = $('textarea[name="comment"]').val();
        var post_id = $this.attr('data-post-id');
        var user_id = $this.attr('data-user-id');
        if (!user_id) {
            alert('请先登录再发布评论！')
        }
        zlajax.post({
            'url': '/comment',
            'data': {
                content,
                post_id
            },
            success: function (result) {
                if (result['code'] == 200) {
                    window.location.reload()
                } else {
                    alert(result['message'])
                }
            }
        })
    })
});