$(document).ready(function () {
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

    let project = "";

    $("#deleteProject").click(function () {
        project = window.location.pathname.split("/")[2];
        Swal.fire({
            icon: 'question',
            title: 'Do you really want to delete this project?',
            confirmButtonText: 'Continue',
            showCancelButton: true,
        }).then( isConfirm => {
            console.log(isConfirm.isConfirmed);
            if(isConfirm.isConfirmed) {
                $.ajax({
                    url: '/deleteProject',
                    type: 'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    data: {
                        'project': project,
                    },
                    success: function () {
                        Swal.fire({
                            icon: 'success',
                            title: 'Project has been deleted!',
                            confirmButtonText: 'Continue',
                        }).then(function (e) {
                            document.location.href = '/';
                        })
                    }
                })
            }
        })
    })
})
