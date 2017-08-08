$(document).ready(function(){

   $("input").focus(function(){
        $(this).css("background-color", "#cccccc");
    });
    $("input").blur(function(){
        $(this).css("background-color", "#ffffff");
    });

    $("p").on({
	    mouseenter: function(){
	        $(this).css("background-color", "lightgray");
	    }, 
	    mouseleave: function(){
	        $(this).css("background-color", "#ffffff");
	    }, 
	    click: function(){
	        $(this).css("background-color", "lightblue");
	    } 
	});
    $("#p1").click(function(){
        $("#p1").css("color", "red").slideUp(2000).slideDown(2000);
    });
	$("input").change(function(){
        $("#message").html("<label> You entered:"+$(this).val()+"</label>");
    });

});
console.log("app.js loaded");

