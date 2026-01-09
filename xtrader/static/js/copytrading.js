
$(document).ready(function () {
  createProTraderTable();
  accountStatus();
});

function createProTraderTable() {
  document.getElementById('tableContainer').innerHTML = '<br><table id="tradersTable" class="strip" style="width:99%;"></table>';
  $('#tradersTable').DataTable({
    ajax: '/social/pro-traders',
    columns: [
      {
        data: 'name',
        title: 'تریدر',
        render: function (data, type, row, meta) {
          let result = '<a href="/social/trader/' + row.id + '"><h1>' + row.name + '</h1></a>';
          return result
        }
      },
      {
        data: 'subscription',
        title: 'اشتراک ماهانه',
        render: $.fn.dataTable.render.number(',', '.', 2, '$')
      },
      {
        title: 'عملکرد',
        data: 'link',
        render: function (data, type, row, meta) {
          let result = '';
          if (type === 'display') {
            result = '<a href="/social/trader/' + row.id + '"><button class="positive small ui button">مشاهده</button></a>';
            //              if (row.protrader_id === 0){
            //                result = '<button class="positive small ui button" onclick="copytrade(1,'+row.id+')">دنبال کردن</button>';
            //              }else if (row.protrader_id === row.id){
            //                result = '<button class="negative small ui button" onclick="copytrade(0,'+row.id+')">دنبال نکردن</button>';
            //              }else{
            //                result = 'شما تریدر دارید';
            //              }
          }
          return result
        }
      }
    ],
  });
  document.getElementById('tradersTable_length').style.display = 'none';
  document.getElementById('tradersTable_info').style.display = 'none';
  document.getElementById('tradersTable_paginate').style.display = 'none';
  let label = document.querySelector('#tradersTable_filter > label');
  label.style.color = 'white';
  let input = label.children[0];
  label.innerHTML = 'جستجو: ';
  input.placeholder = 'نام تریدر';
  input.style.color = 'white';
  input.style.fontFamily = 'IranSans';
  label.appendChild(input);

}

function copytrade(action, protrader_id) {
  console.log(action, protrader_id);
  $.ajax({
    'url': '/social/copy-trade/follow-toggle',
    'method': 'POST',
    'data': JSON.stringify({
      action: action,
      protrader_id: protrader_id,
    }),
    success: function (result) {
      console.log(result);
      if (result.c === 200) {
        createProTraderTable();
      } else {
        alert(result.msg);
      }
    },
    error: function () {

    }
  })
}

function accountStatus() {
  $.ajax({
    url: '/accounts/status',
    success: function (result) {
      console.log(result);
      if (result.following) {

      }
    },
  });
}
