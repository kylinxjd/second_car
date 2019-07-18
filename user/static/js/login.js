$(function () {
    $('#login-window').click(function () {
        $('.login_window').removeAttr('hidden', 'hidden')
    });

    $('#logout').click(function () {
        $.ajax({
            url:'/api/v1.0/logout',
            type:'DELETE',
            cache:false,
            success:function (data) {
                console.log(data);
                msg = data["msg"];
                if (msg){
                    alert(data["msg"]);
                } else {
                    alert(data["err"])
                }
            },
            error:function (res) {
                console.log(res);
            }
        })
    });
    $("#get-msg-code").click(function (e) {
        var phone = $("#phone").val();
        if (phone === '') {
            alert("手机号码为空")
        } else {
            var data = {
                'phone': phone
            };
            var data_json = JSON.stringify(data);
            $.ajax({
                url: '/api/v1.0/smgcode',
                type: 'POST',
                contentType: 'application/json',
                data: data_json,
                cache:false,
                success: function (data) {
                    console.log(data);
                    alert(data['msg'])
                },
                error: function (res) {
                    console.log(res)
                }
            });
        }

    });
    $("#login-btn").click(function (e) {
        var phone = $("#phone").val();
        var msgcode = $("#msgcode").val();
        if (phone === '') {
            alert("手机号码为空")
        }
        if (msgcode === '') {
            alert("请填写验证码")
        } else {
            var data = {
                'phone': phone,
                'msgcode': msgcode
            };
            var data_json = JSON.stringify(data);
            $.ajax({
                url: '/api/v1.0/login',
                type: 'POST',
                contentType: 'application/json',
                data: data_json,
                cache:false,
                success: function (data) {
                    console.log(data);
                    alert(data['msg']);
                    window.location.href='userstore'
                },
                error: function (res) {
                    console.log(res)
                }
            });
        }
    });
});