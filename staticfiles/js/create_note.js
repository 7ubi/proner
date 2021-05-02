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
    $('#create_task_form').submit(function (e){
        e.preventDefault();
        if($('#NodeName').val() === ""){
            Swal.fire({
                icon: 'error',
                title: 'ERROR',
                text: 'Note must have a name!',
                confirmButtonText: 'Try again',
            })
            return;
        }
        console.log($('#NodeName').val())
        $.ajax({
            url: $(location).attr('pathname') + '/create_task',
            type:'POST',
            headers:{'X-CSRFToken': csrftoken},
            data:{
                'name': $('#NodeName').val(),
                'text': $('#text').val(),
            },
            success: function (data){
                if(data['success']) {

                    Swal.fire({
                        icon: 'success',
                        title: 'Note has been saved',
                        confirmButtonText: 'Continue',
                    }).then(function (e){
                        $('#notestable').html($('#notestable').html()+ "<tr id='" + $('#NodeName').val() + "' data-bs-toggle='modal' data-bs-target='#show_note' onclick='showNote(this)'><td>" + $('#NodeName').val() + "</td><td>" + $('#text').val() + "</td></tr>")
                        $('#create_note').modal('hide');
                        $('#NodeName').val('');
                        $('#text').val('');
                    })
                }else{
                    Swal.fire({
                        icon: 'error',
                        title: 'Note already exists',
                        confirmButtonText: 'Try again',
                    })
                }
            }
        })
    })
})