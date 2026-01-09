
$(document).ready(function () {
  initPage();
});
function initPage() {
  createInvestorsTable();
  //  accountStatus();
  getFundInfo();
}
function createInvestorsTable() {
  document.getElementById('investorsContainer').innerHTML = '<br><table id="investorsTable" class="strip" style="width:99%;"></table>';
  $('#investorsTable').DataTable({
    ajax: '/asset-management/investors',
    columns: [
      {
        data: 'id',
        title: 'آیدی'
      },
      {
        data: 'name',
        title: 'سرمایه‌گذار'
      },
      {
        data: 'national_code',
        title: 'کد ملی',
      },
      {
        title: 'تعداد واحد',
        data: 'units',
        render: $.fn.dataTable.render.number(',', '.', 1, '')
        // render: $.fn.dataTable.render.number( ',', '.', 0, 'روز' )
      },
      //      {
      //        title: 'ارزش پرتفو',
      //        data: 'nav',
      //        render: $.fn.dataTable.render.number( ',', '.', 0, '$' )
      //      },
      //      {
      //        title: 'بازدهی کل',
      //        data: 'total_performance',
      //        render: $.fn.dataTable.render.number( ',', '.', 2, '%' )
      //      },
      {
        title: 'عملیات',
        data: 'link',
        render: function (data, type, row, meta) {
          let result = '';
          if (type === 'display') {
            result = '<button class="positive small ui button" onclick="issueOrRedeemUnit(1,' + row.id + ')">صدور</button>';
            result += '<button class="negative small ui button" onclick="issueOrRedeemUnit(0,' + row.id + ')">ابطال</button>';
            //                result += '<button class="negative small ui button" onclick="copytrade(0,'+row.id+')">انتقال</button>';

            //              if (row.protrader_id === 0){
            //                result = '<button class="positive small ui button" onclick="copytrade(1,'+row.id+')">صدور</button>';
            //              }else if (row.protrader_id === row.id){
            //                result = '<button class="negative small ui button" onclick="copytrade(0,'+row.id+')">ابطال</button>';
            //              }else{
            //                result = 'شما تریدر دارید';
            //              }
          }
          return result
        }
      }
    ],
  });
  document.getElementById('investorsTable_length').style.display = 'none';
  document.getElementById('investorsTable_info').style.display = 'none';
  document.getElementById('investorsTable_paginate').style.display = 'none';
  let label = document.querySelector('#investorsTable_filter > label');
  //  label.style.color = 'white';
  let input = label.children[0];
  label.innerHTML = 'جستجو: ';
  input.placeholder = 'سرمایه‌گذار';
  //  input.style.color = 'white';
  input.style.fontFamily = 'IranSans';
  label.appendChild(input);

}

function getFundInfo() {
  $.ajax({
    'url': '/asset-management/get-fund',
    success: function (result) {
      //      console.log(result);
      if (result.hasOwnProperty('brand')) {
        Object.keys(result).forEach(function (key) {
          document.getElementById(key).innerHTML = result[key];
        });
      } else {
        alert('صندوق یافت نشد.');
      }
    },
  });
}

function changeMenu(elm) {
  let menus = ['fund', 'history', 'customer', 'performance'];
  menus.forEach(function (menu) {
    document.getElementById(menu).classList.remove('active');
    document.getElementById(menu + 'div').style.display = 'none';
  });
  document.getElementById(elm.id).classList.add('active');
  document.getElementById(elm.id + 'div').style.display = 'block';
  if (elm.id === 'history') {
    getHistory();
  }
  if (elm.id === 'performance') {
    getFundPerformance();
  }
}
function getHistory() {
  document.getElementById('historyContainer').innerHTML = '<br><table id="historyTable" class="strip" style="width:99%;"></table>';
  $('#historyTable').DataTable({
    ajax: '/asset-management/transactions-history',
    columns: [
      {
        data: 'action',
        title: 'عملیات'
      },
      {
        data: 'amount',
        title: 'مقدار',
        render: $.fn.dataTable.render.number(',', '.', 1, '$')
      },
    ],
  });
  document.getElementById('historyTable_length').style.display = 'none';
  document.getElementById('historyTable_info').style.display = 'none';
  document.getElementById('historyTable_paginate').style.display = 'none';
  let label = document.querySelector('#historyTable_filter > label');
  label.style.display = 'none';
  let input = label.children[0];
  label.innerHTML = 'جستجو: ';
  input.placeholder = 'سرمایه‌گذار';
  input.style.display = 'none';
  input.style.fontFamily = 'IranSans';
  label.appendChild(input);
}

function createInvestor() {
  let fields = ['first_name', 'last_name', 'nationalCode', 'phoneNumber'];
  let params = {};
  let bad_fields = [];
  fields.forEach(function (field) {
    let value = document.getElementById('customer-' + field).value;
    if (value === '') {
      bad_fields.push(field);
    } else {
      params[field] = value;
    }
  });
  if (bad_fields.length === 0) {
    $.ajax({
      'url': '/asset-management/add-investor',
      'method': 'POST',
      'data': JSON.stringify(params),
      success: function (result) {
        if (result.c === 200) {
          alert('مشتری ایجاد شد.');
        } else {
          alert(result.msg);
        }
      },
    });
  } else {
    alert(bad_fields[0]);
  }
}


function issueOrRedeemUnit(actionId, investorId) {
  let units = prompt('تعداد واحد جهت صدور:');
  let action = 'issue';
  if (actionId === 0) {
    action = 'redeem';
  }
  if (units !== '' && units !== null) {
    units = parseInt(units);
    $.ajax({
      'url': '/asset-management/issue-or-redeem-unit',
      method: 'POST',
      data: JSON.stringify({ 'action': action, 'investor_id': investorId, 'amount': units }),
      success: function (result) {
        if (result.c === 200) {
          alert('انجام شد.');
          initPage();
        } else {
          alert(result.msg);
        }
      },
    });
  }
}



function getFundPerformance() {
  document.getElementById('performanceContainer').innerHTML = '<br><table id="performanceTable" class="strip" style="width:99%;"></table>';
  $('#performanceTable').DataTable({
    ajax: '/asset-management/fund-performance',
    order: [[0, "desc"]],
    columns: [
      {
        data: 'age',
        title: 'روز'
      },
      {
        data: 'date',
        title: 'تاریخ'
      },
      {
        data: 'nav',
        title: 'قیمت',
        render: $.fn.dataTable.render.number(',', '.', 2, '$')
      },
      {
        data: 'return',
        title: 'بازدهی',
        render: $.fn.dataTable.render.number(',', '.', 2, '%')
      },
      {
        data: 'btc',
        title: 'بیت‌کوین',
        render: $.fn.dataTable.render.number(',', '.', 2, '$')
      },
      {
        data: 'btcReturn',
        title: 'بازدهی بیت‌کوین',
        render: $.fn.dataTable.render.number(',', '.', 2, '%')
      },
    ],
  });
  //  document.getElementById('performanceTable_length').style.display = 'none';
  //  document.getElementById('performanceTable_info').style.display = 'none';
  //  document.getElementById('performanceTable_paginate').style.display = 'none';
  let label = document.querySelector('#performanceTable_filter > label');
  label.style.display = 'none';
  let input = label.children[0];
  label.innerHTML = 'جستجو: ';
  input.placeholder = 'سرمایه‌گذار';
  input.style.display = 'none';
  input.style.fontFamily = 'IranSans';
  label.appendChild(input);
}






var seriesOptions = [],
  seriesCounter = 0,
  names = ['fund', 'btc'];
//    names = ['MSFT', 'AAPL', 'GOOG'];

/**
 * Create the chart when all data is loaded
 * @returns {undefined}
 */
function createChart() {

  Highcharts.stockChart('container', {

    rangeSelector: {
      selected: 4
    },

    yAxis: {
      labels: {
        formatter: function () {
          return (this.value > 0 ? ' + ' : '') + this.value + '%';
        }
      },
      plotLines: [{
        value: 0,
        width: 2,
        color: 'silver'
      }]
    },

    plotOptions: {
      series: {
        compare: 'percent',
        showInNavigator: true
      }
    },

    tooltip: {
      pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
      valueDecimals: 2,
      split: true
    },

    series: seriesOptions
  });
}

function success(data) {
  var name = this.url.split('=')[1];
  //    let names_map = {'FUND': 'صندوق', 'BTC': 'بیت'};
  var i = names.indexOf(name);
  seriesOptions[i] = {
    name: name.toLowerCase(),
    data: data
  };

  // As we're loading the data asynchronously, we don't know what order it
  // will arrive. So we keep a counter and create the chart when all the data is loaded.
  seriesCounter += 1;

  if (seriesCounter === names.length) {
    createChart();
  }
}

Highcharts.getJSON(
  '/asset-management/fund-performance?mode=fund',
  success
);
Highcharts.getJSON(
  '/asset-management/fund-performance?mode=btc',
  success
);
