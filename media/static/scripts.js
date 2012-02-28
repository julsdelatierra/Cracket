$('document').ready(function(){
    $('#imagefake').live('click', function(){
        $('#image').click();
    });
    $('#image').live('change', function(){
        $('#imagefake').val($(this).val());
    });
});