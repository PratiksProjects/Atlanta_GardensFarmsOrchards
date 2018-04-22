function tableSelect(val){
    var id = val.getAttribute('id');
    $("#"+id).addClass('selected').siblings().removeClass('selected');
    var value=$("#"+id).find('td:first').html();
    //alert(value);
}

function findSelected(){
  alert($("#ownerTable tr.selected td:first").html());
}

function search(tableID) {
  var col = $("#toSearch option:selected").attr('id');
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

function deleteVisitor() {
    var v = $("#visitorTable tr.selected").attr('id');
    if(v == null){
      alert("Please select a row");
    } else {
      console.log(v);
      //code for delet visitor
    }
}

function manageProperty(){
  console.log("hello");
  var id = $("#ownerTable tr.selected").attr('id');
  if(id == null){
    alert("Please select a row");
  } else {
    document.cookie = "PropertyID=" + id;
    window.location.href ="http://localhost:5000/manageProperty";
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
