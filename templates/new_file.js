$(document).ready(function(){
  $("#serch").click(function(){var date=$('#date').val();var auction=$('#auction').val();
  var action=$('action').val();
  var data={date:date,auction:auction,action:action};
  var url='/test';
  console.log(action);
  $('#serchresult').get(url,data);
};}