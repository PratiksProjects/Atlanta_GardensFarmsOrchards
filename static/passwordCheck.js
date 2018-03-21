$(document).ready(function(){
    $('#myForm').on('submit', function(e){
      if($(this).find('input[name="password"]').val() != $(this).find('input[name="confirmPassword"]').val()){
          alert("The two password field inputs do not match.");
          return false;
      }
    });
});
