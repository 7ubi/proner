showNote = function (e){
        $.ajax({
            url: '/getNote/',
            data: {
                'name': e.id,
            },
            success: function (data){
                $("#NoteName").text(data[0].fields["name"]);
                $("#NoteText").html(data[0].fields["text"].replace(/(?:\r\n|\r|\n)/g, '<br />'));
            }
        })
    }