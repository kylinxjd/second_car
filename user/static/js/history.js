function inithistory(){
    $.ajax({
        url:'/user/user_history',
        type:'POST',
        contentType: 'application/json',
        dataType:'json',
        cache:false,
        success:function (ret) {
            console.log(ret);
            if (ret['data'].length === 0){
                $("#no-history").show();
                $("#no-history").css({'text-align':'center', 'margin-top': '150px'});
            }
            else {
                $("#no-history").hide();
            }
            $.each(ret['data'], function (index, value) {
                var li = '<li>\n' +
                    '                <div>\n' +
                    '                    <img src="'+value['index_image_url']+'" width="180" height="220" alt="">\n' +
                    '                    <p>\n' +
                    '                        <span>'+value['brand']+'</span>\n' +
                    '                        <span>'+value['carstyle']+'</span>\n' +
                    '                        <span>'+value['car_style_detail']+'</span>\n' +
                    '                    </p>\n' +
                    '                    <p>\n' +
                    '                        <span>'+value['milage']+'</span>\n' +
                    '                        <span>万公里</span>\n' +
                    '                        <span style="color: red">'+value['price']+'万</span>\n' +
                    '                    </p>\n' +
                    '                    <p>\n' +
                    '                    </p>\n' +
                    '                </div>\n' +
                    '            </li>';
                console.log(value);
                $("#history-cars").append(li);
            })
        },
        error:function (res) {
            console.log("dc");
            console.log(res);
        }
    })
}
$(function () {
    inithistory();
});