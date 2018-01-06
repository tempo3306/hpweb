var answer = '0000'
var question = ''


//限制只能输入数字
$(function () {
    $('input').keypress(function (e) {
        if (!String.fromCharCode(e.keyCode).match(/[0-9\.]/)) {
            return false;
        }
    })
});

//判定验证码是否回答正确
function Answer(useranswer) {
    if (useranswer == answer) {
        return true
    } else {
        return false
    }
}


//更新验证码及弹出窗口
var id = Math.floor(Math.random() * 100 + 1);
var path_yanzhengma = "/yanzhengma/" + id;
var path_answer = "/answer/" + id;

//刷新功能
function GetYanzhengma() {
    time1 = new Date().getTime();
    var id = Math.floor(Math.random() * 100 + 1);
    var path_yanzhengma = "/yanzhengma/" + id;
    var path_answer = "/answer/" + id;
    $.get(path_answer, null, function (ret) {
        question = ret.question;
        answer = ret.answer;
        $('#question').text(question);
    });  //获取答案和问题
    $("#yanzhengma").load(path_yanzhengma);//加载验证码
}

function Confirm() {
    time2 = new Date().getTime();
    usetime =time2-time1
    var useranswer = $('input').val();
    var result = Answer(useranswer);
    if (result) {
        GetYanzhengma();  //刷新验证码
        $('input').val("");
        var a = document.getElementsByTagName("input");
        a[0].focus();
        alert("回答正确，用时"+usetime+"毫秒");
    }
    else {
        $('input').val(""); //清空
        // $('input').focus();
        var a = document.getElementsByTagName("input");
        a[0].focus();
        alert("回答错误");

        //          window.setTimeout(function ()
        // {
        //     var a=document.getElementsByTagName("input");
        //         a[0].focus();
        // }, 0);

    }
}

//刷新功能
$(document).ready(function () {
    $('.cancel').click(function () {
        GetYanzhengma();
        var a = document.getElementsByTagName("input");
        $('intput').val("");
        a[0].focus();
    })
})


$(document).ready(function () {
    $('.confirm').click(function () {
        Confirm();
    })
})
//设置  回车确认  与  E确认
$(document).keydown(function (event) {
    if (event.keyCode == 13 && choice == 1) {
        Confirm();
    }
    else if (event.keyCode == 69 && choice == 2) {
        Confirm();
    }
});

//设计  bt1 bt2 bt3功能
function gray(btn){
    btn.css({'background': '#5e5e5e','border-color': '#5e5e5e'})
}
function blue(btn){
    btn.css({'background': '#00aeff','border-color': '#00aeff'})
}
$(document).ready(function(){
    $('#bt1').click(function(){
        blue($('#bt1'));
        gray($('#bt2'));
        gray($('#bt3'));
        mode=0;
    })
})
$(document).ready(function(){
    $('#bt2').click(function(){
        blue($('#bt2'));
        gray($('#bt1'))
        gray($('#bt3'))
        mode=1;
    })
})
$(document).ready(function(){
    $('#bt3').click(function(){
        blue($('#bt3'));
        gray($('#bt1'));
        gray($('#bt2'));
        mode=2;
    })
})


