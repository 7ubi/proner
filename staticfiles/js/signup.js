$(document).ready(function ($){
    //https://docs.djangoproject.com/en/3.1/ref/csrf
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $("#username").on("change keyup paste", function(){
        $.ajax({
            url:'/signup/check_username',
            type:'POST',
            headers:{'X-CSRFToken': csrftoken},
            data:{
                'username': $('#username').val(),
            },
            success: function (data){
                $('#username').removeClass('exists');
                $('#username').removeClass('notexists');

                if(data['exists']){
                    $('#username').addClass('exists');
                }else{
                    $('#username').addClass('notexists');
                }
            }
        })
    })

    $('form').submit(function (e){
        e.preventDefault();
        if($('#username').val() === ""
            || $('#email').val() === ""
            || $('#password1').val() === ""
            || $('#password2').val() === ""
        ){
            Swal.fire({
                icon: 'error',
                title: 'ERROR',
                text: 'Not everything required was filled in!',
                confirmButtonText: 'Try again',
            })
            return;
        }

        if($('#username').hasClass('exists')){
            Swal.fire({
                icon: 'error',
                title: 'ERROR',
                text: 'User with this username already exsits!',
                confirmButtonText: 'Try again',
            })
            return;
        }

        $.ajax({
            url:'',
            type:'POST',
            headers:{'X-CSRFToken': csrftoken},
            data:{
                'username': $('#username').val(),
                'email': $('#email').val(),
                'password1': $('#password1').val(),
                'password2': $('#password2').val(),
            },
            success: function (data){
                if(data['success']){
                    Swal.fire({
                        icon: 'success',
                        title: 'Your account was created!',
                        confirmButtonText: 'Continue',
                    })
                }else{
                    Swal.fire({
                        icon: 'error',
                        title: 'ERROR',
                        text: data['error'],
                        confirmButtonText: 'Try again',
                    })
                }
            }
        })
    })
})