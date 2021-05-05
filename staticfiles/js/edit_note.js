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

    let note;

    showNote = function (e){
        note = e.id;
        $.ajax({
            url: '/getNote/',
            data: {
                'id': e.id,
            },
            success: function (data){
                $("#NoteNameShow").html(data[0].fields["name"]);
                $("#NoteText").html(data[0].fields["text"].replace(/(?:\r\n|\r|\n)/g, '<br />'));
                $("#NodeNameEdit").val(data[0].fields["name"]);
                $("#text_edit").val(data[0].fields["text"]);
            }
        })
    }

    $("#deleteNote").click(function () {
        Swal.fire({
            icon: 'question',
            title: 'Do you really want to delete this Note?',
            confirmButtonText: 'Continue',
            showCancelButton: true,
        }).then( isConfirm => {
            if(isConfirm.isConfirmed) {
                $.ajax({
                    url: '/delete-note',
                    type: 'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    data: {
                        'note': note,
                    },
                    success: function (data) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Note has been deleted!',
                            confirmButtonText: 'Continue',
                        }).then(function () {
                            $("#show_note").modal('hide');
                            $("#edit_note").modal('hide');
                            $("#" + data['id']).remove();
                        })
                    }
                })
            }
        })
    })

    $('#edit_note_form').submit(function (e){
        e.preventDefault();
        if($('#NodeNameEdit').val() === "" || $('#text_edit').val() === ""){
            Swal.fire({
                icon: 'error',
                title: 'Note must have a name!',
                confirmButtonText: 'Continue',
            })
            return;
        }

        Swal.fire({
            icon: 'question',
            title: 'Do you really want to change this project?',
            confirmButtonText: 'Continue',
            showCancelButton: true,
        }).then( isConfirm => {
            if (isConfirm.isConfirmed) {
                $.ajax({
                    url: '/edit-note',
                    type: 'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    data: {
                        'note': note,
                        'name': $('#NodeNameEdit').val(),
                        'text': $('#text_edit').val(),
                    },
                    success: function (data){
                        Swal.fire({
                            icon: 'success',
                            title: 'Note has been changed!',
                            confirmButtonText: 'Continue',
                        }).then(function () {
                            $("#NoteNameShow").html($('#NodeNameEdit').val());
                            $("#NoteText").html($('#text_edit').val().replace(/(?:\r\n|\r|\n)/g, '<br />'));
                            $("#" + note).children("#NoteNameDisplay").html($('#NodeNameEdit').val());
                            $("#" + note).children("#NoteTextDisplay").html($('#text_edit').val());
                            $("#edit_note").modal('hide');
                        })
                    }
                })
            }
        })
    })
})
