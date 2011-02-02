$(document).ready(function(){
   $('<img/>')[0].src = '/media/images/heart_lighter.png';
   validator = function(){
      var chars = 360 - $('#form textarea').val().length;
      $('#chars').text(chars);
      if(chars < 0){
          $('#form :button[type=submit]').attr('disabled', 'disabled');
      }
      else{
          $('#form :button[type=submit]').attr('disabled', '');
      }
   };
   validator();
   $('#form textarea').bind('focus change click dblclick keyup mouseout', validator);

   $('#form form').submit(function(){
      r = true;

      textarea = $('#form textarea');
      from_name = $('#form [name=from_name]');
      to_name = $('#form [name=to_name]');

      $('#form .alert').remove()
      textarea.css('border-color', '');
      from_name.css('border-color', '');
      to_name.css('border-color', '');


      if(from_name.val().length == 0){
          from_name.after($('<span class="alert">*required</span>'));
          from_name.css('border-color', '#A00');
          r = false;
      }
      to_name = $('#form [name=to_name]');
      if(to_name.val().length == 0){
          to_name.after($('<span class="alert">*required</span>'));
          to_name.css('border-color', '#A00');
          r = false;
      }

      textarea = $('#form textarea');
      if(textarea.val().length < 15 || textarea.val().length > 360){
          textarea.after($('<span class="alert">*must be longer than 15 characters</span>'));
          textarea.css('border-color', '#A00');
          r = false;
      }

      return r;
   });
});

