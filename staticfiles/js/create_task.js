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
    $('form').submit(function (e){
        e.preventDefault();
        if($('#name').val() === ""){
            Swal.fire({
                icon: 'error',
                title: 'ERROR',
                text: 'Task must have a name!',
                confirmButtonText: 'Try again',
            })
            return;
        }
        console.log($('#label').val())
        $.ajax({
            url: $(location).attr('pathname') + '/create_task',
            type:'POST',
            headers:{'X-CSRFToken': csrftoken},
            data:{
                'name': $('#name').val(),
                'label': $('#label').val(),
            },
            success: function (data){
                if(data['success']) {
                    $('#name').val('')
                    Swal.fire({
                        icon: 'success',
                        title: 'Task has been saved',
                        confirmButtonText: 'Continue',
                    }).then(function (e){
                        $('#create_task').modal('hide');
                    })
                }
            }
        })
    })
})