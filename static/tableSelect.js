function tableSelect(val){
    var id = val.getAttribute('id');
    $("#"+id).addClass('selected').siblings().removeClass('selected');
    var value=$("#"+id).find('td:first').html();
    //alert(value);
}

function hideAnimals(){
  if($("#propertyType_selector option:selected").val() != "Farm"){
    $("#animal_type").hide();
    $("#animal_selector").hide();
  } else {
    $("#animal_type").show();
    $("#animal_selector").show();
  }
}

function checkNumbers(name){
  if(isNaN($("#"+name).val())){
    alert("Only numbers allowed for this field");
  }
}

function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    }
    else
    {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = dc.length;
        }
    }
    return decodeURI(dc.substring(begin + prefix.length, end));
}

function checkAdmin(){
    var myCookie = getCookie("type");

    if(myCookie == "ADMIN"){
      $("#request_crop_approval").hide();
      $("#cropname").hide();
      $("#crop_type_selector").hide();
      $("#submit_crop_request_button").hide();
      $("#request_animal_approval").hide();
      $("#animalname").hide();
      $("#submit_animal_request_button").hide();
    }
}


function hideAnimalsRegister(){
  if($("#propertyType_selector option:selected").val() != "Farm"){
    $("#animal_selector").hide();
  } else {
    $("#animal_selector").show();
  }
}

function findSelected(){
  alert($("#ownerTable tr.selected td:first").html());
}

function rangeCheck(){
  if($("#toSearch option:selected").val() == "Visits" || $("#toSearch option:selected").val() == "Rating"){
    $("#min").show();
    $("#minLabel").show();
    $("#max").show();
    $("#maxLabel").show();
    $("#minmaxbut").show();
  } else {
    $("#min").hide();
    $("#minLabel").hide();
    $("#max").hide();
    $("#maxLabel").hide();
    $("#minmaxbut").hide();
  }
}

function minMax(tableID) {
  var col = $("#toSearch option:selected").attr('id');
  if(col == null){
    alert("Please select a search index.");
  } else {
    var input, filter, table, tr, td, i;
    min = $("#min").val();
    max = $("#max").val();
    console.log(min);
    console.log(max);
    table = document.getElementById(tableID);
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[col];
      if (td) {
        if (parseFloat(td.innerHTML) >= min && parseFloat(td.innerHTML) <= max) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }
}

function search(tableID) {
  var col = $("#toSearch option:selected").attr('id');
  if(col == null){
    alert("Please select a search index.");
  }
  else {
    console.log(col);
    var input, filter, table, tr, td, i;
    input = document.getElementById("Search Term");
    filter = input.value.toUpperCase();
    table = document.getElementById(tableID);
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[col];
      if (td) {
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }
}

function addAnimal(){
  var name = $('#approved_animal_selector option:selected').val();
  $('#animals_table tr:last').after("<tr onclick='tableSelect(this);' id='"+name+"'><td>" + name + '</td></tr>');
}
function addCrop(){
  var name = $('#approved_crop_selector option:selected').val();
  $('#crops_table tr:last').after("<tr onclick='tableSelect(this);' id='"+name+"'><td>" + name + '</td></tr>');
}

function deleteAnimal(){
  $("#animals_table tr.selected").remove();
}
function deleteCrop(){
  $("#crops_table tr.selected").remove();
}

function requestAnimal(){
  var type = 'ANIMAL';
  var nm = $("#animalname").val();
  $.post( "/requestAnimal", { type: type, nm: nm } );
}

function requestCrop(){
  var type = $("#crop_type_selector option:selected").attr('id');
  var nm = $("#cropname").val();

  $.post( "/requestCrop", { type: type, nm: nm } );
}

function deleteVisitor() {
    var v = $("#visitorTable tr.selected").attr('id');
    if(v == null){
      alert("Please select a row");
    } else {
      document.cookie = "VName=" + v;
      alert("The visitor account has been deleted");
      window.location.href ="http://localhost:5000/deleteVacc";
    }
}

function logUnlog(){
  var v = $("#ownerTable tr.selected").attr('id');
  if(v == null){
    alert("Please select a row");
  } else {
    document.cookie = "PID=" + v;
    window.location.href ="http://localhost:5000/logUnlog";
  }
}

function hello(){
  alert("hello");
}

function deleteLog() {
    var v = $("#visitorTable tr.selected").attr('id');
    if(v == null){
      alert("Please select a row");
    } else {
      document.cookie = "VName=" + v;
      alert("The visitor log has been deleted");
      window.location.href ="http://localhost:5000/deleteVlog";
    }
}

function manageProperty(tableName){
  console.log("hello");
  var id = $("#"+tableName+" tr.selected").attr('id');
  if(id == null){
    alert("Please select a row");
  } else {
    document.cookie = "PropertyID=" + id;
    window.location.href ="http://localhost:5000/manageProperty";
  }
}
function saveChanges(){
  var myanimals = [];
  var mycrops = [];

  name = $('#farm_name').val();
  type = $('#type_farm').val();
  street = $('#address_input').val();
  city = $('#city_input').val();
  zip = $('#zip_input').val();
  size = $('#size_address_input').val();
  commercial = $('#is_commercial_selector option:selected').attr('id');
  publicc = $('#is_public option:selected').attr('id');
  $('#animals_table tr').each(function(){
    $(this).find('td').each(function(){
        myanimals.push($(this).html());
    })
  })
  $('#crops_table tr').each(function(){
    $(this).find('td').each(function(){
        mycrops.push($(this).html());
    })
  })
  var r = confirm("Are you sure you want to save the changes?");
  if(r == true){
    alert("Your changes have been saved");
    $.post("/updateInfo", {name: name, type: type, street: street, city: city, zip: zip, size: size, commercial: commercial, publicc: publicc, 'animals[]': myanimals, 'crops': mycrops});
  } else{
    alert("Your changes have not been saved.");
  }
}

function addApprovedAC(){
  var type = $("#newAC option:selected").attr('id');
  var name = $("#enter_name").val();
  document.cookie = "ACName=" + name;
  document.cookie = "Type=" + type;
  alert("Your entry has been added to the database");
  window.location.href ="http://localhost:5000/addAC";
}

function deleteOwner(){
  var name = $("#ownerTable tr.selected").attr('id');
  if(name==null){
    alert("Please select a row");
  } else {
    document.cookie = "OName=" + name;
    alert("The owner account has been deleted");
    window.location.href ="http://localhost:5000/deleteOwner";
  }
}

function approveAC(){
  var name = $("#pendingAC tr.selected").attr('id');
  if(name==null){
    alert("Please select a row");
  } else {
    document.cookie = "ACName=" + name;
    alert("The selection has been approved");
    window.location.href ="http://localhost:5000/approveAC";
  }
}

function deleteAC(tableName){
  var name = $("#"+tableName+" tr.selected").attr('id');
  if(name==null){
    alert("Please select a row");
  } else {
    document.cookie = "ACName=" + name;
    alert("The selection has been deleted");
    window.location.href ="http://localhost:5000/deleteAC";
  }
}

function viewDetails(tableName){
  var name = $("#"+tableName+" tr.selected").attr('id');
  if(name==null){
    alert("Please select a row");
  } else {
    document.cookie = "PID=" + name;
    window.location.href ="http://localhost:5000/farmDetails";
  }
}
//above works
// var visit = 0;
// function sortTable() {
//   var table, rows, switching, i, x, y, shouldSwitch;
//   table = document.getElementById("ownerTable");
//   switching = true;
//   /*Make a loop that will continue until
//   no switching has been done:*/
//   while (switching) {
//     //start by saying: no switching is done:
//     switching = false;
//     rows = table.getElementsByTagName("tr");
//     /*Loop through all table rows (except the
//     first, which contains table headers):*/
//     for (i = 2; i < (rows.length - 1); i++) {
//       //start by saying there should be no switching:
//       shouldSwitch = false;
//       /*Get the two elements you want to compare,
//       one from current row and one from the next:*/
//       x = rows[i].getElementsByTagName("td")[10];
//       y = rows[i + 1].getElementsByTagName("td")[10];
//       //check if the two rows should switch place:
//       console.log(visit);
//       if (visit = 0){
//       if (x.textContent > x.textContent) {
//         //if so, mark as a switch and break the loop:
//         console.log(parseInt(x.textContent));
//         console.log(y.textContent);
//         shouldSwitch= true;
//         break;
//       }
//   }
//   else if (visit = 1)
//   {
//       if (x.textContent < y.textContent) {
//         //if so, mark as a switch and break the loop:
//         shouldSwitch= true;
//         break;
//
//       }
//     }
//     if (shouldSwitch) {
//       /*If a switch has been marked, make the switch
//       and mark that a switch has been done:*/
//       rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
//       switching = true;
//     }
//   }
//   }
// }
