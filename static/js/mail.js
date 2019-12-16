$("button[name='btn_delete_mail']").click(function() {

    var data = { mail_id : $(this).data('mail_id')}

    $.ajax({
      type: 'POST',
      url: "/delete_mail",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_mail']").click(function() {

    window.location = "edit_mail?mail_id="+$(this).data('mail_id');

});


$("button[name='btn_new_mail']").click(function() {

    window.location = "insert";

});

