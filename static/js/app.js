$(document).ready(function(){

   $("input").focus(function(){
        $(this).css("background-color", "#cccccc");
    });
    $("input").blur(function(){
        $(this).css("background-color", "#ffffff");
    });

	$("input").change(function(){
        $("#message").html("<label> You entered:"+$(this).val()+"</label>");
    });

});
$(document).ready(function () {
    $("#error-message").hide();
    // CSRF code
                function getCookie(name) {
                    var cookieValue = null;
                    var i = 0;
                    if (document.cookie && document.cookie !== '') {
                        var cookies = document.cookie.split(';');
                        for (i; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
    
                var csrftoken = getCookie('csrftoken');
    
                function csrfSafeMethod(method) {
                    // these HTTP methods do not require CSRF protection
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                }
    
                $.ajaxSetup({
                    crossDomain: false, // obviates need for sameOrigin test
                    beforeSend: function (xhr, settings) {
                        if (!csrfSafeMethod(settings.type)) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });
    
$("#id_username").change(function (e) {
    e.preventDefault();
    var username = $(this).val();
    var form = $(this).closest("form").attr("id");
    //var UrlEndpoint = "{% url 'account:validate_username' %}";
    var UrlEndpoint ="/account/validate_username";
    $.ajax({
        url:UrlEndpoint,
        data: {'username':username },
        dataType:'json',
        content_type:'application/json',
        success:function(data){
            if(form==='loginForm'){
                if(!data.username_is_taken){
                    $("#error-message").show().html("<label>please enter correct username</label>").fadeOut(3000);
                }
                else{
                    $("#error-message").hide();
                }
                
            }
            else{
                if(data.username_is_taken){
                    
                    $("#error-message").show().html("<label>"+data.error_message+"</label>").fadeOut(3000);
                }
                else{
                    
                    $("#error-message").show().html("<label>username available</label>").fadeOut(3000);
                }
                
            }
        },
        error:function(xhr, textStatus, errorThrown){
           console.log(xhr);
        },
    });

  });
// for email validations
function ValidateEmail(email) {
    var expr = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
    return expr.test(email);
};
  $("#id_email").change(function (e) {
    e.preventDefault();
    var email = $(this).val();

    //var UrlEndpoint = "{% url 'account:validate_username' %}";
    var UrlEndpoint ="/account/validate_username";
    $.ajax({
        url:UrlEndpoint,
        data: {'email':email },
        dataType:'json',
        content_type:'application/json',
        success:function(data){
                if(data.email_is_taken){
                    
                    $("#error-message").show().html("<label>"+data.error_message_email+"</label>").fadeOut(3000);
                }
                else{
                    if (!ValidateEmail(email)) {
                        $("#error-message").show().html("<label>Invalid email address.</label>").fadeOut(3000);
                    }
                    else{
                        $("#error-message").show().html("<label>email id available</label>").fadeOut(3000);
                    }
                    
                }              
        },
        error:function(xhr, textStatus, errorThrown){
           console.log(xhr);
        },
    });

  });

  $("#id_password2").change(function (e) {
    e.preventDefault();
    var password1 = $("#id_password1").val();
    var password2 = $("#id_password2").val();
    if(password1!==password2)
    {
        $("#error-message").show().html("<label>password doesn't matches</label>").fadeOut(3000);
    }

  });

  $("#id_password").change(function (e) {
    e.preventDefault();
    var password = $("#id_password").val();
     //var UrlEndpoint = "{% url 'account:validate_username' %}";
     var UrlEndpoint ="/account/validate_username";
     $.ajax({
         url:UrlEndpoint,
         data: {'password':password },
         dataType:'json',
         content_type:'application/json',
         success:function(data){
                console.log(data.user_login);
                //  if(data.valid_login){
                     
                //      //$("#error-message").show().html("<label>"+data.error_message_email+"</label>").fadeOut(3000);
                //  }
                //  else{ 
                     
                //  }              
         },
         error:function(xhr, textStatus, errorThrown){
            console.log(xhr);
         },
     });

  });
  
});

console.log("app.js loaded");

