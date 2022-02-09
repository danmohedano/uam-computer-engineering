$(document).ready(function(){
    $("#register-password").focus(function(){
        $(".hidden").show();
    });

    $("#register-password").blur(function(){
        $(".hidden").hide();
    });

    $("#register-password").keyup(function(){
        var strength = 0;
        var password = $("#register-password").val();

        if (password.match(/[a-z]/)){
            strength++;
        }

        if (password.match(/[A-Z]/)){
            strength++;
        }

        if (password.match(/\d+/)){
            strength++;
        }

        if (password.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]/)){
            strength++;
        }

        $("#meter").attr("value", strength);
    });
})