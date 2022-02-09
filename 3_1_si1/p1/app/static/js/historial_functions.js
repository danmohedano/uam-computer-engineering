$(document).ready(function(){
    $(".pedido").click(function(){
        $("#detail".concat($(this).attr("id"))).toggle();
    });
})