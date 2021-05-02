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
    $('#create_project').submit(function (e){
        e.preventDefault();
        if($('#name').val() === ""){
            Swal.fire({
                icon: 'error',
                title: 'ERROR',
                text: 'Project must have a name!',
                confirmButtonText: 'Try again',
            })
            return;
        }

        $.ajax({
            url:'/create-project/',
            type:'POST',
            headers:{'X-CSRFToken': csrftoken},
            data:{
                'name': $('#name').val(),
            },
            success: function (data){
                if(data['success']){
                    Swal.fire({
                        icon: 'success',
                        title: 'Project has been saved',
                        confirmButtonText: 'Continue',
                    }).then(function (){
                        console.log(data['slug'])
                        $("#projectList").html(`${$("#projectList").html()}<a href='/projects/${data['slug']}' id='navbg' class='nav-link'>${$('#name').val()}</a>`);
                        $('#name').val('');
                        $('#create_project').modal('hide');
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