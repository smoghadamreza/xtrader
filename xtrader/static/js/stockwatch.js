/**
 * Created by hadi on 7/25/17.
 */
var ids = {
    'LastTradePrice': "LastTradePrice", //معامله
    'FirstTradePrice': "FirstTradePrice",  //اولین
    'ClosingPrice': "ClosingPrice", //پایانی
    'PreviousDayPrice': "PreviousDayPrice", //دیروز
    // 'HighestTradePrice': "HighestTradePrice", //بازه روز اول
    // 'LowestTradePrice': "LowestTradePrice", // بازه روز دوم
    // 'UpperPriceThreshold': "UpperPriceThreshold", //قیمت مجاز اول
    // 'LowerPriceThreshold': "LowerPriceThreshold", //قیمت مجاز دوم
    // 'YearHighestTradePrice': "YearHighestTradePrice", //بازه سال اول
    // 'YearLowestTradePrice': "YearLowestTradePrice", // بازه سال دوم
    // 'TotalNumberOfTrades': "TotalNumberOfTrades", // تعداد  معاملات
    'TotalNumberOfSharesTraded': "TotalNumberOfSharesTraded", // حجم معاملات
    'TotalTradeValue': "TotalTradeValue", // ارزش معاملات
    'InstrumentMarketValue': "InstrumentMarketValue", // ارزش بازار
    'NumberOfSharesOrBonds': "NumberOfSharesOrBonds", // تعداد سهام
    'BaseQuantity': "BaseQuantity", // حجم مبنا
    'FreeFloatPercent': "FreeFloatPercent", // سهام شناور
    'MonthAverageVolume': "MonthAverageVolume", // میانگین حجم ماه
    'BuyIndividualVolumePercentage': "BuyIndividualVolumePercentage", // درصد خرید حقیقی
    'BuyIndividualVolume': "BuyIndividualVolume", // خرید حقیقی
    'SellIndividualVolumePercentage': "SellIndividualVolumePercentage", // درصد فروش حقیقی
    'SellIndividualVolume': "SellIndividualVolume", // فروش حقیقی
    'BuyFirmVolumePercentage': "BuyFirmVolumePercentage", // درصد خرید حقوقی
    'BuyFirmVolume': "BuyFirmVolume", // خرید حقوقی
    'SellFirmVolumePercentage': "SellFirmVolumePercentage", // درصد فروش حقوقی
    'SellFirmVolume': "SellFirmVolume", // فروش حقوقی
    'BuyIndividualCount': "BuyIndividualCount", // تعداد خرید حقیقی
    'SellIndividualCount': "SellIndividualCount", // تعداد فروش حقیقی
    'BuyFirmCount': "BuyFirmCount", // تعداد خرید حقوقی
    'SellFirmCount': "SellFirmCount", // تعداد فروش حقوقی
    'LastTradeDate': "LastTradeDate", // آخرین معامله
    'InstrumentStateTitle': "InstrumentStateTitle", // وضعیت
    'Eps': "Eps", //eps
    'PricePerEarning': "PricePerEarning", // p/e
    'PricePerEarningGroup': "PricePerEarningGroup", // p/e group
    'InstrumentName': "InstrumentName",
    'CompanyName': "CompanyName",
    'TotalBuy': "TotalBuy",
    'TotalSell': "TotalSell",
    /**************************************************************/
    'zd1': "zd1",
    'qd1': "qd1",
    'pd1': "pd1",
    'po1': "po1",
    'pd1q': "pd1",
    'po1q': "po1",
    'qo1': "qo1",
    'zo1': "zo1",
    'zd2': "zd2",
    'qd2': "qd2",
    'pd2': "pd2",
    'po2': "po2",
    'qo2': "qo2",
    'zo2': "zo2",
    'zd3': "zd3",
    'qd3': "qd3",
    'pd3': "pd3",
    'po3': "po3",
    'qo3': "qo3",
    'zo3': "zo3",
    /***************************************************************/
    'ClosingPriceVariationPercent': "ClosingPriceVariationPercent",
    'ClosingPriceVariation': "ClosingPriceVariation",
    'ReferencePriceVariationPercent': 'ReferencePriceVariationPercent',
    'ReferencePriceVariation': 'ReferencePriceVariation',
};
var candleIntervals = [];
var userTimeFrame = '4h';
var orderTypes = { 'LIMIT': ['price', 'quantity'], 'MARKET': ['quantity'] };
function makeDepth() {
    let depth_div = document.getElementById('depth');
    let depth = '<div class="divTableRow">\n' +
        '                                        <div class="divTableHead" style="color: #26A65B">حجم</div>\n' +
        '                                        <div class="divTableHead" style="color: #26A65B">خرید</div>\n' +
        '                                        <div class="divTableHead" style="color: #dd4d68">فروش</div>\n' +
        '                                        <div class="divTableHead" style="color: #dd4d68">حجم</div>\n' +
        '        </div>\n';
    let s = 'style="background: #4d5068 "';
    for (let i = 0; i < 10; i++) {
        ids['bp' + i] = 'bp' + i;
        ids['bq' + i] = 'bq' + i;
        ids['aq' + i] = 'aq' + i;
        ids['ap' + i] = 'ap' + i;
        let st = '';
        if (i % 2 === 0) {
            st = s;
        }
        depth += '<div class="divTableRow" ' + st + '>\n' +
            '        <div class="divTableHead" id="bq' + i + '"></div>\n' +
            '        <div class="divTableHead" id="bp' + i + '"></div>\n' +
            '        <div class="divTableHead" id="ap' + i + '"></div>\n' +
            '        <div class="divTableHead" id="aq' + i + '"></div>\n' +
            '</div>\n';

    }
    depth_div.innerHTML = depth;

}

let ordersIDS = {};
$(document).ready(function () {
    makeDepth();
    update_stockwatch();
    portfo();
    //    orders();
    //    setCandleIntervals();
});

function setCandleIntervals() {
    $.ajax({
        url: '/data/intervals',
        success: function (result) {
            let intervalsDiv = '';
            Object.keys(result.intervals).forEach(function (interval) {
                candleIntervals.push(interval);
                intervalsDiv += '<button onclick="changeInterval(this.id)" id="' + interval + '">' + interval + '</button>';
            });
            document.getElementById('intervals').innerHTML = intervalsDiv;
            changeInterval(getSetInterval('get'));
            draw_chart();
        },
    });
}
function changeInterval(newInterval) {
    candleIntervals.forEach(function (interval) {
        document.getElementById(interval).style.backgroundColor = '';
        document.getElementById(interval).style.color = 'black';
    });
    document.getElementById(newInterval).style.backgroundColor = '#1c1f32';
    document.getElementById(newInterval).style.color = 'white';
    if (newInterval !== getSetInterval('get')) {
        getSetInterval('set', newInterval);
        draw_chart();
    }
}
function getSetInterval(action, interval) {
    if (action === 'get') {
        let candleInterval = window.localStorage.candleInterval;
        if (candleInterval) {
            return candleInterval
        } else {
            getSetInterval('set', '4h');
            return getSetInterval('get')
        }
    } else if (action === 'set') {
        if (interval) {
            window.localStorage.candleInterval = interval;
        } else {
            console.log("no interval");
        }
    } else {
        console.log('invalid action');
    }
}

function insert(data) {
    Object.keys(ids).forEach(function (key) {
        if (document.getElementById(key)) {
            var obj = document.getElementById(key);
            if (!former[key]) {
                document.getElementById(key).style.transition = 'background 1s';
                obj.innerHTML = quick_check(data[ids[key]]);
            }
            if (former[key] && !isNaN(former[key])) {
                if (former[key] !== data[ids[key]]) {
                    obj.innerHTML = quick_check(data[ids[key]]);
                }
                if (former[key] < data[ids[key]]) {
                    effect(obj, 'positive');
                }
                if (former[key] > data[ids[key]]) {
                    effect(obj, 'negative');
                }
            }
            former[key] = data[ids[key]]
        }
        // if (['ClosingPriceVariation', 'ClosingPriceVariationPercent', 'ReferencePriceVariationPercent', 'ReferencePriceVariation'].indexOf(key) > -1) {
        // if (['ClosingPriceVariation', 'ClosingPriceVariationPercent', 'ReferencePriceVariationPercent', 'ReferencePriceVariation'].indexOf(key) > -1) {
        //     if (former[key] < 0) {
        //         obj.style.color = '#dd4d68';
        //     } else {
        //         obj.style.color = 'green'
        //     }
        // }
    });
    // ['ClosingPriceVariation', 'ClosingPriceVariationPercent'].forEach(function (k) {
    //     if (['ClosingPriceVariation', 'ClosingPriceVariationPercent'].indexOf(key)>-1){
    //         if (former[key]<0) {obj.style.color='red';} else {obj.style.color = 'green'}
    //     }
    // })
}

function effect(obj, status) {
    var color = { 'positive': '#26A65B', 'negative': '#C3272B' },
        current_color = obj.style.background,
        timer = 1;
    obj.style.background = color[status];
    setTimeout(function () {
        // obj.style.background = '#22263d'
        obj.style.background = current_color;
    }, timer * 1000)
}

if (checkTime()) {
    setInterval(update_stockwatch, 5000);
}
var former = {};

// var data;
function update_stockwatch() {
    console.log('updating');
    $.ajax({
        type: 'GET',
        url: "/data/stock-watch/" + SymbolId,
        success: function (result) {
            result = JSON.parse(result);
            //            result['InstrumentName'] = '(' + result['InstrumentName'] + ')';
            result['InstrumentName'] = result['InstrumentName'];
            let book_depth = result.depth.length;
            for (let i = 0; i < book_depth; i++) {
                result['bp' + i] = result.depth[i].bp;
                result['bq' + i] = result.depth[i].bq;
                result['ap' + i] = result.depth[i].ap;
                result['aq' + i] = result.depth[i].aq;
            }
            // result['TotalBuy'] = result['BuyIndividualCount'] + result['BuyFirmCount'];
            // result['TotalSell'] = result['SellIndividualCount'] + result['SellFirmCount'];
            // var pe = result['PricePerEarning'];
            // pe *= 100;
            // pe = Math.round(pe);
            // pe /= 100;
            // result['PricePerEarning'] = pe;
            insert(result);
        },
    });
}

window.ODate = Date;
window.Date = JDate;

function draw_chart() { }
function draw_chart1() {
    waiting('wait');
    $.ajax({
        url: '/data/get-data/' + SymbolId + '/' + getSetInterval('get'),
        success: function (data) {
            data = JSON.parse(data);
            var close = [],
                //            name = data['per_name'];
                name = SymbolId;
            data = JSON.parse(data['items']);
            var dataLength = data.length;
            for (var i = 0; i < dataLength; i++) {
                close.push([
                    data[i][0], // date
                    data[i][4], // close
                    // Math.ceil(data[i][4]), // close
                ]);
            }
            Highcharts.stockChart('chart', {


                rangeSelector: {
                    enabled: false,
                    inputEnabled: false,
                    // selected: 1
                },
                credits: {
                    enabled: false,
                },
                yAxis: [{
                    gridLineWidth: 0,
                    minorGridLineWidth: 0,
                    opposite: false,
                }],
                scrollbar: {
                    enabled: false
                },
                navigator: {
                    enabled: false
                },
                series: [{
                    color: {
                        linearGradient: { x1: 0, x2: 0, y1: 0, y2: 1 },
                        stops: [
                            [0, '#f3f774'],
                            [0.25, '#aae98e'],
                            [0.50, '#09cac8'],
                            [0.75, '#aae98e'],
                            [1, '#f3f774']
                        ]
                    },
                    name: name,
                    data: close,
                }]
            });
            waiting('default');
        },
        error: function (e) {
            waiting('default');
        }
    });
    //    $.getJSON('/data/get-data/' + SymbolId +'/'+getSetInterval('get'), function (data) {
    //        // $.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=aapl-c.json&callback=?', function (data) {
    //        data = JSON.parse(data);
    //        var close = [],
    ////            name = data['per_name'];
    //            name = SymbolId;
    //        data = JSON.parse(data['items']);
    //        var dataLength = data.length;
    //        for (var i = 0; i < dataLength; i++) {
    //            close.push([
    //                data[i][0], // date
    //                data[i][4], // close
    //                // Math.ceil(data[i][4]), // close
    //            ]);
    //        }
    //        Highcharts.stockChart('chart', {
    //
    //
    //            rangeSelector: {
    //                enabled: false,
    //                inputEnabled: false,
    //                // selected: 1
    //            },
    //            credits: {
    //                enabled: false,
    //            },
    //            yAxis: [{
    //                gridLineWidth: 0,
    //                minorGridLineWidth: 0,
    //                opposite: false,
    //            }],
    //            scrollbar: {
    //                enabled: false
    //            },
    //            navigator: {
    //                enabled: false
    //            },
    //            series: [{
    //                color: {
    //                    linearGradient: {x1: 0, x2: 0, y1: 0, y2: 1},
    //                    stops: [
    //                        [0, '#f3f774'],
    //                        [0.25, '#aae98e'],
    //                        [0.50, '#09cac8'],
    //                        [0.75, '#aae98e'],
    //                        [1, '#f3f774']
    //                    ]
    //                },
    //                name: name,
    //                data: close,
    //            }]
    //        });
    //        waiting('default');
    //
    //    });






    // Highcharts.setOptions({
    //     lang: {
    //         months: ['فروردين', 'ارديبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'],
    //         shortMonths: ['فروردين', 'ارديبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'],
    //         weekdays: ["یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه"]
    //     }
    // });

    Highcharts.createElement('link', {
        href: 'https://fonts.googleapis.com/css?family=Unica+One',
        rel: 'stylesheet',
        type: 'text/css'
    }, null, document.getElementsByTagName('head')[0]);
    Highcharts.theme = {
        colors: ['#2b908f', '#90ee7e', '#f45b5b', '#7798BF', '#aaeeee', '#ff0066', '#eeaaee',
            '#55BF3B', '#DF5353', '#7798BF', '#aaeeee'],
        chart: {
            // events: {
            //     load: function () {
            //
            //         // set up the updating of the chart each second
            //         var series = this.series[0];
            //         setInterval(function () {
            //             var x = (new Date()).getTime(), // current time
            //                 y = Math.round(23000);
            //             series.addPoint([x, y], true, true);
            //         }, 1000);
            //     }
            // },

            backgroundColor: {
                color: '#fff',
                /*linearGradient: {x1: 0, y1: 0, x2: 1, y2: 1},
                 stops: [
                 [0, '#2a2a2b'],
                 [1, '#3e3e40']
                 ]
                 },*/
                style: {
                    fontFamily: 'IRANSans'
                },
                plotBorderColor: '#606063',

                // zooming:
                // zoomType: 'x',
                // panning: true,
                // panKey: 'shift'
            },
            title: {
                style: {
                    color: '#E0E0E3',
                    // textTransform: 'uppercase',
                    fontSize: '20px'
                }
            },
            subtitle: {
                style: {
                    color: '#E0E0E3',
                    // textTransform: 'uppercase'
                }
            },
            xAxis: {
                gridLineColor: '#707073',
                labels: {
                    style: {
                        color: '#E0E0E3'
                    }
                },
                lineColor: '#707073',
                minorGridLineColor: '#505053',
                tickColor: '#707073',
                title: {
                    style: {
                        color: '#A0A0A3'

                    }
                }
            },
            yAxis: {
                gridLineColor: '#707073',
                labels: {
                    style: {
                        color: '#E0E0E3'
                    }
                },
                lineColor: '#707073',
                minorGridLineColor: '#505053',
                tickColor: '#707073',
                tickWidth: 1,
                title: {
                    style: {
                        color: '#A0A0A3'
                    }
                }
            },
            tooltip: {

                // xDateFormat: '%Y-%m-%d',
                shared: true,
                useHTML: true,
                // headerFormat: '<small>{point.key}</small><br><table>',
                // pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
                // '<td style="text-align: right"> <b>{point.y} </b></td></tr>',
                // footerFormat: '</table>',

                headerFormat: '',
                pointFormat: '<td style="text-align: right"> <b>{point.y}</b></td></tr>',
                // footerFormat: '</table>',
                valueDecimals: 0,

                backgroundColor: 'rgba(0, 0, 0, 0.85)',
                style: {
                    color: '#F0F0F0'
                }
            },
            plotOptions: {
                series: {
                    animation: false,

                    dataLabels: {
                        color: '#B0B0B3'
                    },
                    marker: {
                        lineColor: '#333'
                    }
                },
                boxplot: {
                    fillColor: '#505053'
                },
                candlestick: {
                    lineColor: 'white'
                },
                errorbar: {
                    color: 'white'
                }
            },
            legend: {
                itemStyle: {
                    color: '#E0E0E3'
                },
                itemHoverStyle: {
                    color: '#FFF'
                },
                itemHiddenStyle: {
                    color: '#606063'
                }
            },
            credits: {
                style: {
                    color: '#FFF'
                    // '#666'
                },
                text: 'treasurypto.com',
                href: 'http://www.treasurypto.com'
            },
            labels: {
                style: {
                    color: '#707073'
                }
            },

            drilldown: {
                activeAxisLabelStyle: {
                    color: '#F0F0F3'
                },
                activeDataLabelStyle: {
                    color: '#F0F0F3'
                }
            },

            navigation: {
                buttonOptions: {
                    symbolStroke: '#DDDDDD',
                    theme: {
                        fill: '#505053'
                    }
                }
            },

            // scroll charts
            rangeSelector: {
                buttonTheme: {
                    fill: '#505053',
                    stroke: '#000000',
                    style: {
                        color: '#CCC'
                    },
                    states: {
                        hover: {
                            fill: '#707073',
                            stroke: '#000000',
                            style: {
                                color: 'white'
                            }
                        },
                        select: {
                            fill: '#000003',
                            stroke: '#000000',
                            style: {
                                color: 'white'
                            }
                        }
                    }
                },
                inputBoxBorderColor: '#505053',
                inputStyle: {
                    backgroundColor: '#333',
                    color: 'silver'
                },
                labelStyle: {
                    color: 'silver'
                }
            },

            navigator: {
                handles: {
                    backgroundColor: '#666',
                    borderColor: '#AAA'
                },
                outlineColor: '#CCC',
                maskFill: 'rgba(255,255,255,0.1)',
                series: {
                    color: '#7798BF',
                    lineColor: '#A6C7ED'
                },
                xAxis: {
                    gridLineColor: '#505053'
                }
            },

            scrollbar: {
                barBackgroundColor: '#808083',
                barBorderColor: '#808083',
                buttonArrowColor: '#CCC',
                buttonBackgroundColor: '#606063',
                buttonBorderColor: '#606063',
                rifleColor: '#FFF',
                trackBackgroundColor: '#404043',
                trackBorderColor: '#404043'
            },

            // special colors for some of the
            legendBackgroundColor: 'rgba(0, 0, 0, 0.5)',
            background2: '#505053',
            dataLabelsColor: '#B0B0B3',
            textColor: '#C0C0C0',
            contrastTextColor: '#F0F0F3',
            maskColor: 'rgba(255,255,255,0.3)'
        },
    };
    Highcharts.setOptions(Highcharts.theme);

}

var modal,
    OrderId = '',
    order_type;

function trade(kind, type, order_id) {
    //    modal = document.getElementById(kind + 'Modal');
    //    modal.style.display = "block";
    order_type = type;
    if (type === 'order') {
        OrderId = '';
    } else {
        OrderId = order_id;
    }
}

//$(document).ready(function () {
//    var spanBuy = document.getElementsByClassName("close")[0];
//    var spanSell = document.getElementsByClassName("close")[1];
//
//    spanBuy.onclick = function () {
//        modal.style.display = "none";
//    }
//
//    spanSell.onclick = function () {
//        modal.style.display = "none";
//    }
//
//    window.onclick = function (event) {
//        if (event.target === modal) {
//            modal.style.display = "none";
//        }
//    }
//
//});

function showMessage(msg, status) {
    let msgBox = document.getElementById('orderMessage');
    msgBox.innerHTML = '<div id="msgPop">' + msg + '</div>';
    if (status === 'error') {
        msgBox.style.color = '#e74c3c';
    } else {
        msgBox.style.color = '#09cac8';
    }
    $('#msgPop').delay(2000).fadeOut('slow');
}

function sendOrder(orderSide) {
    var data = {
        symbol: SymbolId,
        quantity: Number($('#' + 'quantity').val()),
        side: orderSide,
        type: document.getElementById('orderType').value,
    };
    if (["LIMIT"].indexOf(data.type) > -1) {
        data.price = Number($('#' + 'price').val());
        if (!data.price) {
            showMessage('لطفا قیمت را وارد کنید', 'error');
            return false
        }
    }
    if (!data.quantity) {
        showMessage('لطفا تعداد را وارد کنید', 'error');
        return false
    }

    waiting('wait');
    $.ajax({
        type: 'POST',
        url: '/trade',
        data: {
            order: JSON.stringify(data),
        },
        success: function (result) {
            if (result.error) {
                showMessage(result.msg, 'error');

            } else {
                portfo();
                showMessage('سفارش ارسال شد', '');
            }
            waiting('default');
        },
        error: function (e) {
            alert(e.responseJSON.msg);
            waiting('default');
        },
    });
    getAccountStatus();
}


function portfo() {
    $.ajax({
        type: 'GET',
        url: '/portfolio',
        success: function (result) {
            let portfolio_div = document.getElementById('pportfo');
            portfolio_div.innerHTML = '';
            let head = '                            <div class="divTableRow">\n' +
                '                                <div class="divTableHead">نماد</div>\n' +
                '                                <div class="divTableHead">تعداد</div>\n' +
                '                                <div class="divTableHead">بلوکه شده</div>\n' +
                '                            </div>\n';
            let rows = '';
            let usdt = 0;
            result.assets.forEach(function (asset) {
                let row = '';
                if (asset.symbol === 'USDT') {
                    usdt = asset['free'];
                    row = '<div class="divTableCell">' + asset.symbol + '</div>';
                } else {
                    row = '<div class="divTableCell"><a href="/spot/' + asset.symbol + 'USDT' + '">' + asset.symbol + '</a></div>';
                }
                row += '<div class="divTableCell">' + asset['free'] + '</div>';
                row += '<div class="divTableCell">' + asset.locked + '</div>';
                rows += '<div class="divTableRow">' + row + '</div>';
            });
            portfolio_div.innerHTML = head + rows;
            //            document.getElementById('BuyingPower').innerHTML = usdt.toFixed(2) + ' usdt';
            orders();
        },
        error: function (e) {
            let portfolio_div = document.getElementById('pportfo');
            portfolio_div.innerHTML = '<h1><a href="/profile-setup/"><div style="font-family: IRANSans">ابتدا اکسچنج خود را متصل کنید</div></a></h1>';
        }
    })
}

function orders() {
    $.ajax({
        type: 'GET',
        url: '/orders?symbol=' + SymbolId,
        success: function (result) {
            let status_map = {
                NEW: 'در انتظار',
                CANCELED: 'کنسل شده', //- The order has been canceled by the user.
                REJECTED: 'رد شده', // - The order has been rejected and was not processed. (This is never pushed into the User Data Stream)
                TRADE: 'انجام جزیی', // - Part of the order or all of the order's quantity has filled.
                EXPIRED: 'منقضی شده', // - The order was canceled according to the order type's rules (e.g. LIMIT FOK orders with no fill, LIMIT IOC or MARKET orders that partially fill) or by the exchange, (e.g. orders canceled during liquidation, orders canceled during maintenance)
                DONE: 'انجام شده', // - added by hadi
                FILLED: 'انجام شده', // - added by hadi
            };
            let orders_div = document.getElementById('orders_place');
            orders_div.innerHTML = '';
            let head = '<div class="divTableRow">\n' +
                '    <div class="divTableHead">سفارش</div>\n' +
                '    <div class="divTableHead">نماد</div>\n' +
                '    <div class="divTableHead">حجم</div>\n' +
                '    <div class="divTableHead">قیمت</div>\n' +
                '    <div class="divTableHead">معامله شده</div>\n' +
                '    <div class="divTableHead">ارزش معامله</div>\n' +
                '    <div class="divTableHead">وضعیت</div>\n' +
                '    <div class="divTableHead"></div>\n' +
                '</div>';
            let rows = '';
            result.orders.forEach(function (order) {
                let order_status = order.status;
                if (order.origQty === order.executedQty) {
                    order_status = 'DONE';
                }
                let order_side = 'خرید';
                if (order.side === 'SELL') {
                    order_side = 'فروش';
                }
                let price = parseFloat(order.price);
                if (price === 0) {
                    price = 'بازار';
                }
                let row = '<div class="divTableCell">' + order_side + '</div>';
                row += '<div class="divTableCell">' + order.symbol + '</div>';
                //                row += '<div class="divTableCell"><a href="/spot/' + order.symbol + '">' + order.symbol + '</a></div>';
                row += '<div class="divTableCell">' + parseFloat(order.origQty) + '</div>';
                row += '<div class="divTableCell">' + price + '</div>';
                row += '<div class="divTableCell">' + parseFloat(order.executedQty) + '</div>';
                row += '<div class="divTableCell">' + parseFloat(order.cummulativeQuoteQty) + '</div>';
                row += '<div class="divTableCell">' + status_map[order_status] + '</div>';
                if (order_status === 'NEW' || order_status === 'TRADE') {
                    ordersIDS[order.orderId] = order.symbol;
                    row += '<div class="divTableCell"><i class="remove icon" title="حذف" style="color: #E35C67" onclick="cancelOrder(' + order.orderId + ')"></i></div>';
                } else {
                    row += '<div class="divTableCell"></div>';
                }
                rows += '<div class="divTableRow">' + row + '</div>';
                // {% if order.OrderState != 'لغو شده' and order.OrderState != 'کامل معامله شده' %}
                // <i class="edit icon" title="ویرایش" style="color: #00ca9d"
                //    onclick="{% if order.OrderSideId == 'خرید' %}trade('buy','edit',{{ order.OrderId }}){% else %}trade('sell','edit',{{ order.OrderId }}){% endif %}"></i>
                // <i class="remove icon" title="انصراف" style="color: #E35C67"
                //    onclick="cancelOrder('{{ order.OrderId }}')"></i>
                // {% endif %}
                // </div>
            });
            orders_div.innerHTML = head + rows;
        },
        error: function (err) {
            let orders_div = document.getElementById('orders_place');
            orders_div.innerHTML = '<h1><a href="/profile-setup/"><div style="font-family: IRANSans">ابتدا اکسچنج خود را متصل کنید</div></a></h1>';
        }
    });
    // getAccountStatus();
    //    portfo();
}

function getAccountStatus() {
    // portfo();
    // $.ajax({
    //     type: 'GET',
    //     url: '/account-status',
    //     success: function (result) {
    //         // result = JSON.parse(result);
    //         document.getElementById('BuyingPower').innerHTML = numberSeparator(result['BuyingPower']);
    //         // $('#account_values').html(result);
    //         // document.getElementById('account').style.display = 'block';
    //     },
    // });
}

function cancelOrder(OrderId, order_symbol) {
    waiting('wait');
    $.ajax({
        type: 'GET',
        url: '/cancel-order?orderId=' + OrderId + '&symbol=' + ordersIDS[OrderId],
        success: function (result) {
            showMessage('سفارش حذف شد', '');
            console.log(result);
            portfo();
            //            orders();
            waiting('default');
        },
        error: function (err) {
            waiting('default');
        }
    });
    getAccountStatus();
}

function checkTime() {
    return true
    // var opening = new JDate,
    //     closing = new JDate,
    //     now = new JDate;
    // if (now.getDay() == 4 || now.getDay() == 5) return false;
    // opening.setHours(8);
    // opening.setMinutes(30);
    // closing.setHours(12);
    // closing.setMinutes(30);
    // if (now > opening && now < closing) {
    //     return true
    // } else {
    //     return false
    // }
}

function changeOrderType(elm) {
    console.log(elm.value);
    document.getElementById('price').disabled = true;
    document.getElementById('price').placeholder = 'بازار';
    document.getElementById('price').value = '';
    document.getElementById('quantity').disabled = true;
    orderTypes[elm.value].forEach(function (param) {
        document.getElementById(param).disabled = false;
        if (param === 'price') {
            document.getElementById(param).placeholder = 'قیمت';
        }
    });
}