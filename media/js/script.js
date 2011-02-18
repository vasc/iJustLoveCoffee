function splitandspan(){
    //find all text in divs, wrap in spans
    $('#dedication>div').contents().filter(function(){return this.nodeType==3}).wrap('<span />');

    //flatten all spans and split them
    var re = new RegExp(String.fromCharCode(160), "g");

    $('#dedication>div>span').each(function(){
        $(this).text($(this).text());
        var parent = $(this);
        var values = parent.text().split(' ');
        if(values.length == 0) return;
        var hasclass = parent.hasClass('emph');
        for(var val in values){
            if(values[val] == '') continue;
            values[val] = values[val].replace(re, " ");

            var new_node = $('<span>' + values[val] + '</span>');
            if(hasclass){ new_node.addClass('emph'); }

            parent.before(new_node);
            new_node.after(' ');
        }
        parent.remove();
    });

/*    var parent = $(this).parent().filter('span');
    var divtext = $(this).wrap('<span />').parent();
    var values = divtext.text().split(' ');
    var hasclass = parent.hasClass('emph');
    for(var val in values){
        if(values[val] == '') continue;

        var new_node = $('<span>' + values[val] + ' </span>');
        if(hasclass) new_node.addClass('emph');

        if(parent.length > 0){
            parent.before(new_node);
        }
        else{
            divtext.before(new_node);
        }
    }
    //$(divtext).parent().parent().filter('span').remove();

    $(divtext).remove();*/
}


$(document).ready(function(){

   //$('#toolbar').buttonset();
   //$('#radio1').button({'icons':  {primary: "ui-icon-pencil"}});
   //$('#radio2').button({'icons':  {primary: "ui-icon-wrench"}});
   		$( ".color-button" ).draggable({revert: "invalid"});
   		$( "#dedication .span").dropable();
   splitandspan();


   //Likes preloading
   $('<img/>')[0].src = '/media/images/heart_lighter.png';

   //edit dedication
   $('#radio1').click(function(){
      $('#dedication').attr('contenteditable', 'true');
      $('#dedication').removeClass('formatting');
      $('#dedication').addClass('editing');
      $('#dedication').focus();
   });
   $('#radio2').click(function(){
      $('#dedication').removeAttr('contenteditable');
      $('#dedication').addClass('formatting');
      $('#dedication').removeClass('editing');


      splitandspan();
   });

   /*$('#dedication.editing').live('keyup', function(e){
       console.log(e.keyCode);
       if (e.keyCode == '13') {
           splitandspan();
       }
   });*/


   //format dedication
   $('#dedication.formatting div').live('click', function(){
       splitandspan();
       $(this).toggleClass('heading');
       return false;
   });
   $('#dedication.formatting span').live('keyup', function(){
      splitandspan();
   });

   $('#dedication.formatting span').live('click', function(){
      $(this).toggleClass('emph');
      return false;
   });



   //Comment validator
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

