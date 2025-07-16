/**
 * Created by hadi on 10/31/16.
 */
var indicators;
var intervals = [];
var output = '';
var userTimeFrame;
let currentStrategyId;
let watchlistId = '0';
var groupingUnitsMap = {
    '15m': ['minute', [15]],
    '30m': ['minute', [30]],
    '1h': ['hour', [1]],
    '4h': ['hour', [4]],
    '1d': ['day', [1]],
}
console.log(currentStrategyId);
// TODO: reading indicators
function backtestPageSetup() {
    getSetIndicators();
    setIntervalsCandles();
    load_strategy_names();
    getWatchLists();
}
function setIntervalsCandles() {
    $.ajax({
        type: 'GET',
        url: "/data/intervals",
        success: function (result) {
            console.log(result);
            let intervalsDiv = document.getElementById('timeframes');
            let intervals_buttons = '';
            let intervals_buttons2 = '';
            intervals = Object.keys(result.intervals);
            intervals.forEach(function (chart_interval) {
                intervals_buttons += '<button onclick="changeTimeFrame(this.id)" id=' + chart_interval + '>' + chart_interval + '</button>';
                intervals_buttons2 += '<option>' + chart_interval + '</option>';
            });
            intervalsDiv.innerHTML = intervals_buttons;
            document.getElementById('strategyTimeFrame').innerHTML = intervals_buttons2;
            document.getElementById('timeframesStrategy')
            userTimeFrame = result.userTimeFrame;
            setTimeFrame(userTimeFrame);
            loadChartsReady();
        }
    });
}
function getSetIndicators() {
    $.ajax({
        type: 'GET',
        url: "/indicators-api",
        success: function (result) {
            indicators = JSON.parse(result);
            insert_indicators();
        }
    });
}
var isScaned = false;
var isStrategySaved;
var isBacktested = false;
var drawing_tool = { 'tool': { 'name': 'line', 'params': {} }, 'status': 0, 'num_of_points': 0 };
var per_name;
var portfo = [];
var num_of_charts = 1;
var dohlcv = [];
var ohlc = [];
var groupingUnits = [];
var result_type_1 = {};
var result_type_2 = {};
var chosen_strategies = {};
var indicators_cross = {};

window.ODate = Date;
window.Date = JDate;

function loadChartsReady() {
    //    isStrategySaved = false;
    changeIsStrategySaved(false);
    load_data('/data/get-data/' + symbol_id);
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
            // backgroundColor: {
            //     linearGradient: {x1: 0, y1: 0, x2: 1, y2: 1},
            //     stops: [
            //         [0, '#2a2a2b'],
            //         [1, '#3e3e40']
            //     ]
            // },
            style: {
                fontFamily: 'IranSanc'
            },
            plotBorderColor: '#606063',

            // zooming:
            zoomType: 'x',
            panning: true,
            panKey: 'shift'
        },
        title: {
            style: {
                fontFamily: 'IRANSans',
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
            headerFormat: '<small>{point.key}</small><br><table>',
            pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
                '<td style="text-align: right"> <b style="color: {series.color}">{point.y} </b></td></tr>',
            footerFormat: '</table>',
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
    };
    Highcharts.setOptions(Highcharts.theme);
};

//$(function(){
//    backtestPageSetup();
//});
window.onload = backtestPageSetup;
function load_data(url) {
    console.log('loading data');
    waiting('wait');
    isBacktested = false;
    $.ajax({
        url: url + '/' + userTimeFrame,
        success: function (data) {
            // window.history.pushState('page2', 'Title', '/backtest/stock=' + symbol_id);
            // console.log(data);
            data = JSON.parse(data);
            per_name = data['per_name'];
            symbol_id = data['measurement_name'];
            name = symbol_id;
            data = JSON.parse(data['items']);
            // console.log(data);
            data2 = data;
            var dataLength = data.length;
            groupingUnits = [
                groupingUnitsMap[userTimeFrame],
            ];
            dohlcv = [];
            ohlc = [];
            var type_1 = [];
            var type_2 = [];
            for (var i = 0; i < dataLength; i++) {
                ohlc.push([
                    data[i][0], // the date
                    data[i][1], // open
                    data[i][2], // high
                    data[i][3], // low
                    data[i][4] // close
                ]);

                dohlcv.push([
                    data[i][0], // the date
                    data[i][1], // open
                    data[i][2], // high
                    data[i][3], // low
                    data[i][4], // close
                    data[i][5] // the volume
                ]);

                type_1.push(0);
                type_2.push(1);
            }
            result_type_2[0] = type_2;
            draw_chart();
            delete_all(['indicators'], false);
            load_strategy();
            //            load_strategy_names();
            document.getElementById('search').children[0].children[0].value = '';
            waiting('default');

        },
        error: function (e) {
            waiting('default');
        },
    });
}

function draw_chart() {
    $('#container').highcharts('StockChart', {
        chart: {
            //test
            events: {
                click: function (e) {
                    switch (this.series.name) {
                        case name:
                            // console.log(name);
                            break;
                        default:
                            if (drawing_tool['status']) {
                                var chart = $('#container').highcharts();
                                // console.log(drawing_tool);
                                switch (drawing_tool['tool']['name']) {
                                    case 'line':
                                        var series = chart.get('line');
                                        if (series) {
                                            series.remove();
                                        }
                                        switch (drawing_tool['num_of_points']) {
                                            case 0:
                                                drawing_tool['tool']['params']['point1'] = [e.xAxis[0].value, e.yAxis[0].value];
                                                drawing_tool['num_of_points'] += 1;
                                                break;
                                            case 1:
                                                drawing_tool['tool']['params']['point2'] = [e.xAxis[0].value, e.yAxis[0].value];
                                                chart.addSeries({
                                                    data: [drawing_tool['tool']['params']['point1'], drawing_tool['tool']['params']['point2']],
                                                    color: 'yellow',
                                                    id: 'line',
                                                    name: 'line'
                                                });
                                                drawing_tool['num_of_points'] += 1;
                                                // drawing_tool['status'] = 0;
                                                break;
                                            case 2:
                                                // console.log('here');
                                                var new_point = [e.xAxis[0].value, e.yAxis[0].value],
                                                    point1 = drawing_tool['tool']['params']['point1'],
                                                    point2 = drawing_tool['tool']['params']['point2'];
                                                if (check_distance(point1, new_point) < check_distance(point2, new_point)) {
                                                    drawing_tool['tool']['params']['point1'] = new_point;
                                                } else {
                                                    drawing_tool['tool']['params']['point2'] = new_point;
                                                }
                                                chart.addSeries({
                                                    data: [drawing_tool['tool']['params']['point1'], drawing_tool['tool']['params']['point2']],
                                                    color: 'yellow',
                                                    id: 'line',
                                                    name: 'line'
                                                });
                                                // drawing_tool['status'] = 0;
                                                break;
                                        }
                                        break;
                                }
                            }
                            break;
                    }
                },
            },
        },
        rangeSelector: {
            selected: 1
        },
        plotOptions: {
            series: {
                animation: false
            }
        },
        title: {
            text: name
        },
        legend: {
            enabled: true
        },
        yAxis: [{
            opposite: false

        }],

        series: [{
            type: 'candlestick',
            name: name,
            data: ohlc,
            id: 'main',
            dataGrouping: {
                units: groupingUnits
            }
        }
        ],
    });
}

function check_distance(point1, point2) {
    if (point1.length === point2.length) {
        var l = point1.length,
            s = 0;
        for (var i = 0; i < l; i++) {
            s += Math.pow((point1[i] - point2[i]), 2);
        }
        s = Math.sqrt(s);
        // console.log(s);
        return s
    } else {
        // console.log('input error, inputs length does not match!');
    }
}

//function check_strategies_number1() {
//    var good_mouse_color = '#00ca9d',
//        bad_mouse_color = '#E35C67';
//    var stra_num = $('#strategies > div').length;
//    var buttons = ['back_test_button', 'delete_all_button', 'save_button', 'scan_button'];
//    buttons.forEach(function (button_id) {
//        if (document.getElementById(button_id)) {
//            document.getElementById(button_id).remove();
//        }
//    });
//    document.getElementById('results').style.display = 'none';
//    if (stra_num > 0) {
//        document.getElementById('results').style.display = 'block';
//        var button_place = document.getElementById('button_place');
//
//        var back_test_button = document.createElement('a');
//        back_test_button.setAttribute('id', 'back_test_button');
//        back_test_button.setAttribute('class', 'item');
//        back_test_button.addEventListener('mouseover', function () {
//            for (var i = 0; i < num_of_charts; i++) {
//                if (document.getElementById('' + i)) {
//                    document.getElementById('' + i).style.color = good_mouse_color;
//                }
//            }
//        });
//        back_test_button.addEventListener('mouseout', function () {
//            for (var i = 0; i < num_of_charts; i++) {
//                if (document.getElementById('' + i)) {
//                    document.getElementById('' + i).style.color = 'white';
//                }
//            }
//        });
//        back_test_button.addEventListener('click', function () {
//            toggle(this);
//        });
//        var txt = document.createTextNode('بک تست');
//        back_test_button.appendChild(txt);
//        button_place.appendChild(back_test_button);
//
//
//        // creating save button
//        var save_button = document.createElement('a');
//        save_button.setAttribute('id', 'save_button');
//        save_button.setAttribute('class', 'item');
//        save_button.addEventListener('mouseover', function () {
//            for (var i = 0; i < num_of_charts; i++) {
//                if (document.getElementById('' + i)) {
//                    document.getElementById('' + i).style.color = good_mouse_color;
//                }
//            }
//            // document.getElementById('strategies').style.color = 'red';
//        });
//        save_button.addEventListener('mouseout', function () {
//            for (var i = 0; i < num_of_charts; i++) {
//                if (document.getElementById('' + i)) {
//                    document.getElementById('' + i).style.color = 'white';
//                }
//            }
//        });
//        save_button.addEventListener('click', function () {
//            // pick_portfolio('block');
//            // toggle(this);
//            // save_filters('default');
//        });
//        var txt = document.createTextNode('‌ذخیره استراتژی');
//        save_button.appendChild(txt);
//        // button_place.appendChild(document.createTextNode('  '));
//        // button_place.appendChild(save_button);
//
//        // creating scan button
//        var scan_button = document.createElement('a');
//        scan_button.setAttribute('id', 'scan_button');
//        scan_button.setAttribute('class', 'item');
//        scan_button.addEventListener('mouseover', function () {
//            for (var i = 0; i < num_of_charts; i++) {
//                if (document.getElementById('' + i)) {
//                    document.getElementById('' + i).style.color = good_mouse_color;
//                }
//            }
//        });
//        scan_button.addEventListener('mouseout', function () {
//            for (var i = 0; i < num_of_charts; i++) {
//                if (document.getElementById('' + i)) {
//                    document.getElementById('' + i).style.color = 'white';
//                }
//            }
//        });
//        scan_button.addEventListener('click', function () {
//            toggle(this);
//        });
//        var txt = document.createTextNode('اسکن بازار  و ذخیره استراتژی');
//        scan_button.appendChild(txt);
//        button_place.appendChild(document.createTextNode('  '));
//        button_place.appendChild(scan_button);
//
//        // creating delete button
//        var delete_all_button = document.createElement('a');
//        delete_all_button.setAttribute('id', 'delete_all_button');
//        delete_all_button.setAttribute('class', 'left negative item');
//        // delete_all_button.setAttribute('style', 'float:left');
//        delete_all_button.addEventListener('mouseover', function () {
//            for (var i = 0; i < num_of_charts; i++) {
//                if (document.getElementById('' + i)) {
//                    document.getElementById('' + i).style.color = bad_mouse_color;
//                }
//            }
//        });
//        delete_all_button.addEventListener('mouseout', function () {
//            for (var i = 0; i < num_of_charts; i++) {
//                if (document.getElementById('' + i)) {
//                    document.getElementById('' + i).style.color = 'white';
//                }
//            }
//        });
//        delete_all_button.addEventListener('click', function () {
//            delete_all(['symbol_ids', 'indicators', 'back test', 'scan', 'filters'], true);
//        });
//        var txt = document.createTextNode('پاک کردن همه');
//        delete_all_button.appendChild(txt);
//        button_place.appendChild(document.createTextNode('  '));
//        button_place.appendChild(delete_all_button);
//    }
//}
function check_strategies_number() {
    var good_mouse_color = '#00ca9d',
        default_button_color = '#292d48',
        bad_mouse_color = '#E35C67';
    var filters_num = $('#strategies > div').length;
    var buttons = ['back_test_button', 'delete_all_button', 'save_button', 'scan_button'];
    buttons.forEach(function (button_id) {
        if (document.getElementById(button_id)) {
            let button = document.getElementById(button_id);
            button.addEventListener('mouseover', function () {
                let filters_color = good_mouse_color;
                if (button_id === 'delete_all_button') {
                    button.style.backgroundColor = bad_mouse_color;
                    filters_color = bad_mouse_color;
                } else {
                    button.style.backgroundColor = good_mouse_color;
                }
                for (var i = 0; i < num_of_charts; i++) {
                    if (document.getElementById('' + i)) {
                        document.getElementById('' + i).style.color = filters_color;
                    }
                }
            });
            button.addEventListener('mouseout', function () {
                for (var i = 0; i < num_of_charts; i++) {
                    if (document.getElementById('' + i)) {
                        document.getElementById('' + i).style.color = 'white';
                    }
                }
                button.style.backgroundColor = default_button_color;
            });
            //            button.addEventListener('click', function () {
            //                if (button_id === 'save_button'){
            //                     pick_portfolio('block');
            //                     toggle(this);
            //                     save_filters('default');
            //                }else if (button_id === 'delete_all_button'){
            //                    delete_all(['symbol_ids', 'indicators', 'back test', 'scan', 'filters'], true);
            //                }else{
            //                    toggle(this);
            //                }
            //                 button.style.color = 'white';
            //            });
            button.style.backgroundColor = default_button_color;
            if (filters_num > 0) {
                button.disabled = false;
                button.style.display = 'block';
            } else {
                button.disabled = true;
                button.style.display = 'none';
                button.classList.remove("active");
            }
        }
    });
}

function show_market() {
    var div = document.getElementById('scan-place');
    div.setAttribute('style', 'display: block');
}

function delete_all(targets, save) {
    let deletedStrategy = false;
    targets.forEach(function (target) {
        //    console.log(target);
        switch (target) {
            case 'indicators':
                for (var i = 1; i < num_of_charts; i++) {
                    delete result_type_1[i];
                    delete result_type_2[i];
                    //console.log('del div: ' + i);
                    if (document.getElementById('' + i)) {
                        document.getElementById('' + i).remove();
                    }
                    if (document.getElementById('div' + i)) {
                        document.getElementById('div' + i).remove();
                    }
                    var chart = $('#container').highcharts();
                    if (chart.get('' + i)) {
                        chart.get('' + i).remove();
                    }
                    chosen_strategies = {};
                }
                check_strategies_number();
                if (save && !deletedStrategy) {
                    // console.log(save);
                    // console.log('saved null filters');
                    //                    isStrategySaved = false;
                    deletedStrategy = true;
                    changeIsStrategySaved(false);
                    save_filters('default');
                }
                //                load_strategy();
                break;
            case 'filters':
                // check_strategies_number();
                break;
            case 'back test':
                var chart = $('#container').highcharts();
                if (chart) {
                    if (chart.get('back_b') != null) {
                        chart.get('back_b').remove();
                    }
                    if (chart.get('back_s') != null) {
                        chart.get('back_s').remove();
                    }
                }
                document.getElementById("table_place").innerHTML = '';
                document.getElementById("table_place").setAttribute('style', 'display:none');
                isBacktested = false;
                break;
            case 'scan':
                var div = document.getElementById('scan-place');
                div.setAttribute('style', 'display: none');
                changeIsStrategySaved(true);
                if (!deletedStrategy) {
                    deletedStrategy = true;
                    save_filters('default');
                }
                isScaned = false;
                //                isStrategySaved = false;
                //                changeIsStrategySaved(true);
                break;
            case 'symbol_ids':
                portfo = [];
                // console.log('names deleted');
                break;
            default:
                // console.log('undefined target: ' + target);
                break;
        }
    });
}

function apply() {
    var result1 = [];
    var keys = Object.keys(result_type_1);
    var L1 = keys.length;
    if (L1 > 0) {
        var len = result_type_1[keys[0]].length;
        for (var i = 0; i < len; i++) {
            var s = 0;
            Object.keys(result_type_1).forEach(function (r) {
                s += Number(result_type_1[r][i]);
            });
            switch (s) {
                case L1:
                    result1.push(1);
                    break;
                case -L1:
                    result1.push(-1);
                    break;
                default:
                    result1.push(0);
                    break;
            }
        }
    }
    var result2 = [];
    var keys = Object.keys(result_type_2);
    var L1 = keys.length;
    if (L1 > 0) {
        var len = result_type_2[keys[0]].length;
        for (var i = 0; i < len; i++) {
            var s = 1;
            Object.keys(result_type_2).forEach(function (r) {
                s *= Number(result_type_2[r][i]);
            });
            switch (s) {
                case 1:
                    result2.push(1);
                    break;
                case 0:
                    result2.push(0);
                    break;
            }
        }
    }

    for (var i = 0; i < result2.length; i++) {
        result2[i] *= result1[i];
    }
    var config = {
        'stop loss': {},
        // document.getElementById('config_stop loss').value,
        'take profit': {},
        // document.getElementById('config_take profit').value,
        'initial deposit': document.getElementById('config_initial deposit').value,
    };
    ['stop loss', 'take profit'].forEach(function (setting) {
        ['value', 'apply'].forEach(function (conf) {
            config[setting][conf] = document.getElementById(setting + ' ' + conf).value;
        })
    });
    var dd = { 'name': symbol_id, 'trades': JSON.stringify(result2), 'config': config, 'interval': userTimeFrame };
    // console.log(dd);
    waiting('wait');

    $.ajax({
        type: 'GET',
        url: "/back-test",
        data: {
            param: JSON.stringify(dd),
            //            strategyId: getSelectedStrategyId(),
        },
        error: function () {
            waiting('default');
            // alert('Sorry something went wrong.');
            alert('مشکلی پیش آمده است. لطفا بعدا دوباره تلاش کنید.');
        },
        //        beforeSend: function () {
        //            if (!isStrategySaved) {
        //                save_filters('wait');
        //            }
        //        },
        success: function (result) {
            // console.log(result);
            res = JSON.parse(result);
            if (res === "f") {
                alert('این فیلترها هیچ اشتراکی با هم ندارند.');
                waiting('default');
            } else {
                isBacktested = true;
                apply2(res);
            }
        }
    });
}

function apply2(backtest) {
    var res = backtest['result'];
    var num_of_trades = Object.keys(res).length,
        buy_b = [],
        sell_b = [],
        tbl = [];
    document.getElementById('table_place').innerHTML = '';
    if (num_of_trades !== 0) {
        add_table();
        var row_num = 0;
        for (var i = num_of_trades; i > 0; i -= 1) {
            if (Object.keys(res["" + i]).length === 2) {
                tbl = [num_of_trades - i + 1, dohlcv[res["" + i]["sell"]["date"]][0], translate(res["" + i]["sell"]['action']), quick_check(dohlcv[res["" + i]["sell"]["date"]][4]), 'NaN', res["" + i]["sell"]["candles in trade"], res["" + i]["sell"]["return"], res["" + i]["sell"]["capital"]];
                if (res["" + i]["sell"]['action'] !== 'Not Sold Yet') {
                    sell_b.unshift([dohlcv[res["" + i]["sell"]["date"]][0], dohlcv[res["" + i]["sell"]["date"]][2]]);
                }
                appendRow(tbl, row_num);
                row_num += 1;
            } else {
                // console.log('no sold yet');
                tbl = [num_of_trades - i + 1, dohlcv[dohlcv.length - 1][0], res["" + i]["sell"]['action'], 'NaN', 'NaN', 'NaN', "NaN", "NaN"];
                appendRow(tbl, row_num);
                row_num += 1;
            }
            if (i == 1) {
                tbl = [num_of_trades - i + 1, dohlcv[res["" + i]["buy"]["date"]][0], translate(res["" + i]["buy"]['action']), quick_check(dohlcv[res["" + i]["buy"]["date"]][4]), translate(res["" + i]["buy"]["waiting candles"]), 'NaN', 'NaN', translate('Initial Deposit: ') + numberSeparator(res["" + i]["buy"]["initaial deposit"])];
                buy_b.unshift([dohlcv[res["" + i]["buy"]["date"]][0], dohlcv[res["" + i]["buy"]["date"]][2]]);
                appendRow(tbl, row_num);
                row_num += 1;
            } else {
                tbl = [num_of_trades - i + 1, dohlcv[res["" + i]["buy"]["date"]][0], translate(res["" + i]["buy"]['action']), quick_check(dohlcv[res["" + i]["buy"]["date"]][4]), res["" + i]["buy"]["waiting candles"], 'NaN', 'NaN', 'NaN'];
                buy_b.unshift([dohlcv[res["" + i]["buy"]["date"]][0], dohlcv[res["" + i]["buy"]["date"]][2]]);
                appendRow(tbl, row_num);
                row_num += 1;
            }
        }
        var avg = backtest['summery']['average'];
        tbl = ['', '', '', translate('Average'), avg['waiting candles'], avg['candles in trade'], avg['profits'], "NaN"];
        appendRow(tbl, row_num);
        row_num += 1;

        var std = backtest['summery']['std'];
        tbl = ['', '', '', translate('Standard Deviation'), std['waiting candles'], std['candles in trade'], String(std['profits']) + '%', "NaN"];
        appendRow(tbl, row_num);
        row_num += 1;


        var chart = $('#container').highcharts();
        if (chart.get('back_b') != null) {
            chart.get('back_b').remove();
        }
        if (chart.get('back_s') != null) {
            chart.get('back_s').remove();
        }
        chart.addSeries({
            data: buy_b,
            color: 'green',
            type: 'flags',
            shape: 'circlepin',
            title: 'B',
            name: 'خرید',
            id: 'back_b',
            dataGrouping: {
                units: groupingUnits
            },

            onSeries: 'main'
        });
        chart.addSeries({
            data: sell_b,
            color: 'red',
            type: 'flags',
            title: 'S',
            name: 'فروش',
            id: 'back_s',
            dataGrouping: {
                units: groupingUnits
            },
            shape: 'circlepin',
            onSeries: 'main'
        });
        waiting('default');
    } else {
        waiting('default');
        // alert('these strategies have nothing in common!');
        alert('هیچ معالمه‌ای با این استراتژی در این سهم یافت نمی شود.');
    }

}

function translate(word) {
    var translate = {
        'sell': 'فروش',
        'buy': 'خرید',
        'Not Sold Yet': 'هنوز فروخته نشده',
        'Start': 'آغاز',
        'Initial Deposit: ': 'موجودی اولیه:  ',
        'Average': 'میانگین',
        'Standard Deviation': 'انحراف معیار ',
        'stoploss': 'حد ضرر',
        'takeprofit': 'حد سود'
    };
    if (translate[word]) {
        return translate[word]
    } else {
        return word
    }
}

function save_filters(pointer) {
    console.log('saving strategy -------');
    //    pick_portfolio('none');
    waiting('wait');
    var filters = Object.keys(chosen_strategies),
        strategy_id = getSelectedStrategyId();
    let strategy_name = getSelectedStrategyName(strategy_id);
    var strategy = {
        id: strategy_id,
        watchlistId: watchlistId,
        name: strategy_name, 'filters': filters, 'symbol_ids': portfo, 'interval': userTimeFrame
    };
    // console.log('save ajax');
    console.log(isStrategySaved);
    if (!isStrategySaved && strategy_name) {
        $.ajax({
            type: 'POST',
            url: "/save-strategy",
            data: {
                param: JSON.stringify(strategy),

                //                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            async: false,
            error: function () {
                waiting('default');
                alert('متاسفانه هنگام دخیره کردن استراتژی شما مشکلی پیش آمده است,\n لطفا بعدا تلاش کنید.');
                // alert('Sorry, while saving your strategy something went wrong.');
            },
            success: function (result) {
                if (result.s === 302) {
                    alert(result.m);
                    window.location = result.redirect;
                }
                //                isStrategySaved = true;
                waiting(pointer);
                // console.log(result);
                changeIsStrategySaved(true);
                if (result.result == 'delete') {
                    console.log("strategy deleted", isStrategySaved);
                    let elm = document.getElementById("strategyId-" + getSelectedStrategyId());
                    if (elm) {
                        elm.remove();
                    }
                    load_strategy();
                } else {
                    console.log("changed, isStrategySaved", isStrategySaved);
                    //                    let strategyNames = document.getElementById('strategyNames').children;
                    //                    for (let i=0; i++; i < strategyNames.length){
                    //                        strategyNames[i].selected = false;
                    //                    }
                    if (strategy_id !== result.id) {
                        new_strategy = '<option id="strategyId-' + result.id + '" value="strategyId-' + result.id + '" selected>' + strategy_name + '</option>';
                        document.getElementById('strategyNames').innerHTML = new_strategy + document.getElementById('strategyNames').innerHTML;
                    }
                    document.getElementById('strategyNames').value = "strategyId-" + result.id;
                }
            }
        });
    } else {
        waiting('default');
    }
}

function pick_portfolio(stat) {
    // document.getElementById('portfolio place').style.display = stat;
    // switch (state){
    //     case 'block':
    //         break;
    //     case 'none':
    //         break;
    // }
}

function add_stock(result) {
    // console.log(result);
    if (portfo.indexOf(result.symbol_id) == -1) {
        var div = document.getElementById('stocks place');
        var but = document.createElement('button');
        but.appendChild(document.createTextNode(result.title));
        but.setAttribute('class', 'ui button');
        but.setAttribute('title', 'حذف نماد');
        but.setAttribute('name', result.symbol_id);
        // console.log(result);
        portfo.push(result.symbol_id);
        but.addEventListener('click', function () {
            portfo.splice(portfo.indexOf(this.getAttribute('name')), 1);
            this.remove();
            //            isStrategySaved = false;
            changeIsStrategySaved(false);
        });
        div.appendChild(but);
        //        isStrategySaved = false;
        changeIsStrategySaved(false);
    }
}

function load_strategy_names() {
    delete_all(['indicators'], false);
    $.ajax({
        type: 'GET',
        url: "/get-strategy-names",
        success: function (result) {
            let strategyNames = '';
            result.strategies.forEach(function (strategy) {
                strategyNames += '<option id="strategyId-' + strategy.id + '" value="strategyId-' + strategy.id + '">' + strategy.name + '</option>';
            });
            strategyNames += '<option id="strategyId-0" value="strategyId-0">ساخت استراتژی جدید</option>';
            let strategyNamesDiv = document.getElementById('strategyNames');
            strategyNamesDiv.innerHTML = strategyNames;
            console.log(currentStrategyId);
            //                load_strategy();
            if (currentStrategyId !== undefined) {
                load_strategy();
            }
        }
    });
}
function getSelectedStrategyId() {
    let selectedStrategyId = document.getElementById('strategyNames').value.split('-')[1];
    return parseInt(selectedStrategyId)
}
function getSelectedStrategyName(selectedStrategyId) {
    let strategyName = '';
    if (selectedStrategyId === 0 && Object.keys(chosen_strategies).length > 0) {
        strategyName = prompt('برای استراتژی خود یک نام تعیین کنید:');
    } else {
        let strategyNameDiv = document.getElementById('strategyId-' + selectedStrategyId);
        if (strategyNameDiv) {
            strategyName = strategyNameDiv.innerHTML;
        }
    }
    return strategyName
}
function load_strategy() {
    let selectedStrategyId = getSelectedStrategyId();
    console.log("load-strategy", selectedStrategyId, currentStrategyId);
    waiting('wait');
    //    selectedStrategyId = parseInt(selectedStrategyId);
    if (selectedStrategyId > 0) {
        console.log('here');
        $.ajax({
            type: 'GET',
            url: "/load-strategy",
            data: {
                id: selectedStrategyId,
            },
            success: function (strategy) {
                strategy = JSON.parse(strategy);
                document.getElementById('watchListNames').value = strategy.watchlistId;
                changeWatchList();
                if (selectedStrategyId === currentStrategyId) {
                    delete_all(['symbol_ids', 'indicators', 'filters'], false);
                } else {
                    delete_all(['symbol_ids', 'indicators', 'back test', 'scan', 'filters'], false);
                    setTimeFrame(strategy.interval);
                    changeIsStrategySaved(true);
                }
                //                if (selectedStrategyId === currentStrategyId){
                //                    if (isStrategySaved)
                //                }
                currentStrategyId = selectedStrategyId;
                //                console.log(strategy);
                //                setTimeFrame(strategy.interval);
                //                changeIsStrategySaved(true);

                strategy['filters'].forEach(function (filter) {
                    filter = JSON.parse(filter);
                    waiting('wait');
                    filter['symbol_id'] = symbol_id;
                    calculate_indicators(filter, isStrategySaved);
                    // waiting('wait');
                });
            },
            error: function () {
                //                delete_strategy({'name': name});
                //                load_alternative_strategy({});
                // create_name_option({'new_name':name});
                // var opt = document.getElementById("strategy name: " + name);
                // opt.parentNode.removeChild(opt);
                // load_strategy({'name':document.getElementById('strategys_name_place').value});
            }

        });
    } else {
        //    console.log('here');
        delete_all(['symbol_ids', 'indicators', 'back test', 'scan', 'filters'], false);
    }
    waiting('default');
}

function scan() {
    // console.log('scan called: ' + isScaned);
    if (!isScaned) {
        isScaned = true;
        waiting('wait');
        $.ajax({
            type: 'GET',
            url: "/scan-market",
            data: {
                strategyId: getSelectedStrategyId(),
                //                interval: userTimeFrame,
            },
            error: function () {
                waiting('default');
                alert('متاسفانه مشکلی پیش آمد.');
                // alert('Sorry something went wrong.');
            },
            beforeSend: function () {
                if (!isStrategySaved) {
                    save_filters('wait');
                }
            },
            success: function (result) {
                // console.log(result);
                result = JSON.parse(result);
                show_scan_result(result);
                show_market();
                waiting('default');
                isScaned = true;
            }
        });
    } else {
        show_market();
    }
}


function show_scan_result(result) {
    Object.keys(result).forEach(function (signal) {
        var place = document.getElementById('scan result ' + signal);
        place.innerHTML = '';
        var table = document.createElement('table');
        table.setAttribute('style', 'width:100%');
        if (result[signal].length > 0) {
            var num = 1;
            result[signal].forEach(function (signal_symbol) {
                var signal_symbol_name = signal_symbol['symbol_id']; //signal_symbol['symbol_name'],
                description_text = ''; //signal_symbol['description'],
                color = '#1C1F32';
                //                    let color = '#1C1F32';
                let symbol_url = signal_symbol['symbol_id'];
                var item = document.createElement('tr');
                if (num % 2 == 0) color = '#4D5068';
                item.setAttribute('style', 'background: ' + color);
                item.setAttribute('name', symbol_url);
                item.addEventListener('mouseover', function () {
                    document.getElementById('stockwatch ' + symbol_url).style.display = 'block';
                });
                item.addEventListener('mouseout', function () {
                    document.getElementById('stockwatch ' + symbol_url).style.display = 'none';
                });

                var symbol_num = document.createElement('td');
                if (signal === 'buy') symbol_num.setAttribute('style', 'color: #00CA9D');
                else symbol_num.setAttribute('style', 'color: #E35C67');
                symbol_num.innerHTML = num;
                item.appendChild(symbol_num);
                num += 1;


                var symbol_name = document.createElement('td');
                var a = document.createElement('a');
                a.addEventListener('click', function () {
                    //                    delete_all(['indicators'], false);
                    symbol_id = symbol_url;
                    load_data('/data/get-data/' + symbol_id);
                    //                    load_strategy();
                });
                if (signal === 'buy') a.setAttribute('style', 'color: #00CA9D; cursor:pointer;');
                else a.setAttribute('style', 'color: #E35C67;cursor: pointer');
                a.innerHTML = signal_symbol_name;
                symbol_name.appendChild(a);
                item.appendChild(symbol_name);

                var company_name = document.createElement('td');
                company_name.setAttribute('style', 'color: white');
                company_name.innerHTML = description_text;
                item.appendChild(company_name);


                var stockwatch_link = document.createElement('td');
                var a = document.createElement('a');
                a.setAttribute('href', '/spot/' + symbol_url);
                a.setAttribute('id', 'stockwatch ' + symbol_url);
                a.setAttribute('style', 'display:none; color: #F7CA18');
                a.innerHTML = '(مشاهده نماد)';
                stockwatch_link.appendChild(a);
                item.appendChild(stockwatch_link);


                table.appendChild(item);
            });
            place.appendChild(table);
        } else {
            place.innerHTML = 'هیچ نمادی یافت نشد.';
        }
    });

}


function show_scan_result1(result) {
    Object.keys(result).forEach(function (signal) {
        var place = document.getElementById('scan result ' + signal);
        place.innerHTML = '';
        if (result[signal].length > 0) {
            result[signal].forEach(function (signal_symbol) {
                var signal_symbol_name = signal_symbol['symbol_name'],
                    description_text = signal_symbol['description'],
                    symbol_url = signal_symbol['symbol_id'];
                var item = document.createElement('div');
                item.setAttribute('class', 'item');
                item.setAttribute('name', symbol_url);
                item.addEventListener('click', function () {
                    delete_all(['indicators'], false);
                    symbol_id = symbol_url;
                    load_data('/data/get-data/' + symbol_id);
                });

                var content = document.createElement('div');
                content.setAttribute('class', 'content');
                var a = document.createElement('a');
                a.setAttribute('class', 'symbol');
                if (signal == 'buy') a.setAttribute('style', 'color: #00CA9D');
                else a.setAttribute('style', 'color: #E35C67;');
                a.innerHTML = signal_symbol_name;
                content.appendChild(a);
                var description = document.createElement('div');
                description.setAttribute('class', 'description');
                description.setAttribute('style', 'color: white');
                description.innerHTML = description_text;
                content.appendChild(description);
                item.appendChild(content);
                place.appendChild(item);
            });
        } else {
            place.innerHTML = 'No Symbol found';
        }
    });

}

// function get_settings() {
//     apply();
// }
function appendRow(vals, row_num) {
    var tbl = document.getElementById('table'), // table reference
        row = tbl.insertRow(tbl.rows.length),      // append table row
        color = '#1C1F32',
        i;
    if (row_num % 2 == 0) color = '#4D5068';
    // else color = 'blue';
    row.setAttribute('style', 'background: ' + color);
    // insert table cells to the new row
    for (i = 0; i < tbl.rows[0].cells.length; i++) {
        createCell(row.insertCell(i), vals[i], 'row', i);
    }
}

// create DIV element and append to the table cell
function createCell(cell, text, style, i) {
    var div = document.createElement('div'), // create DIV element
        txt = document.createTextNode(text); // create text node
    // div.appendChild(txt);                    // append text node to the DIV
    // div.setAttribute('class', style);        // set DIV class attribute
    // div.setAttribute('className', style);    // set DIV class attribute for IE (?!)
    // cell.appendChild(div);                   // append DIV to the table cell
    switch (i) {
        case 0:
            cell.setAttribute("style", "color: #00CA9D");
            break;
        case 1:
            if (!isNaN(text) && text != '') {
                var date = new Date(Number(text));
                var year = date.getUTCFullYear();
                var month = ("0" + (date.getMonth() + 1)).substr(-2);
                var day = ("0" + date.getDate()).substr(-2);

                text = day + " - " + month + " - " + year;
                txt = document.createTextNode(text);
            }
            break;
        case 4:
            if (text == 'NaN') {
                cell.setAttribute("class", "collapsed");
                txt = document.createTextNode('');
            }
            break;
        case 5:
            if (isNaN(text)) {
                cell.setAttribute("class", "collapsed");
                txt = document.createTextNode('');
            }
            break;
        case 6:
            if (isNaN(text)) {
                if (text == 'NaN') {
                    cell.setAttribute("class", "collapsed");
                    txt = document.createTextNode('');
                }
            } else {
                txt = document.createTextNode(text + ' %');
                div.setAttribute('dir', 'ltr');
                ic = document.createElement('i');
                ic.setAttribute('style', 'float: left');
                if (text < 0) {
                    cell.setAttribute('style', 'background-color: #E35C67 ');
                    // ic.setAttribute("class", "remove icon");
                    // div.appendChild(ic);
                } else {
                    cell.setAttribute('style', 'background-color: #00CA9D');
                    // ic.setAttribute("class", "icon checkmark");
                    // div.appendChild(ic);
                }
            }
            break;
        case 7:
            if (text == 'NaN') {
                cell.setAttribute("class", "collapsed");
                txt = document.createTextNode('');
            } else {
                if (text[0] != 'م') {
                    // console.log(text);
                    txt = document.createTextNode(numberSeparator(text));
                }
            }
            break;
    }
    div.appendChild(txt);                    // append text node to the DIV
    div.setAttribute('class', style);        // set DIV class attribute
    div.setAttribute('className', style);    // set DIV class attribute for IE (?!)
    cell.appendChild(div);                   // append DIV to the table cell
}

function numberSeparator(n) {
    n = String(n);
    var m = [],
        ll = n.length;
    for (var i = 0; i < ll; i++) {
        m.push(n.substring(i, i + 1));
    }
    m.reverse();
    var i = 0,
        n = '';
    m.forEach(function (digit) {
        i++;
        n = digit + n;
        if (i % 3 == 0 & i != ll) {
            n = ',' + n;
        }
    });
    return n
}

function add_table() {
    // {#create div for table#}
    // {#                var div = document.createElement("DIV");#}
    // {#                div.setAttribute("id", "table_place");#}
    // {#                div.setAttribute("class", "ui container");#}
    // {#                document.body.appendChild(div);#}

    // {#insert an empty line#}
    // var li = document.createElement("BR");
    // document.getElementById("table_place").appendChild(li);

    document.getElementById("table_place").setAttribute('style', 'display: block; height: 300px; overflow: auto');
    var x = document.createElement("TABLE");
    x.setAttribute("id", "table");
    x.setAttribute("style", "text-align:right");
    x.setAttribute("class", "ui selectable inverted celled  table");
    // {#                x.setAttribute("class", "ui compact celled definition table");#}
    document.getElementById("table_place").appendChild(x);


    var tb = document.createElement("THEAD");
    tb.setAttribute("id", "myTH");
    document.getElementById("table").appendChild(tb);

    var y = document.createElement("TR");
    y.setAttribute("id", "myTr");
    // y.setAttribute('class','title row');
    y.setAttribute('style', 'background: #292D48');
    document.getElementById("myTH").appendChild(y);

    var z = document.createElement("TH");
    // {#                z.setAttribute("class","colapse");#}
    var t = document.createTextNode("ردیف");
    z.appendChild(t);
    document.getElementById("myTr").appendChild(z);

    var z = document.createElement("TH");
    var t = document.createTextNode("تاریخ");
    z.appendChild(t);
    document.getElementById("myTr").appendChild(z);

    var z = document.createElement("TH");
    var t = document.createTextNode("نوع معامله");
    z.appendChild(t);
    document.getElementById("myTr").appendChild(z);
    var z = document.createElement("TH");
    var t = document.createTextNode("قیمت: پایانی");
    z.appendChild(t);
    document.getElementById("myTr").appendChild(z);

    var z = document.createElement("TH");
    var t = document.createTextNode("کندل های انتظار");
    z.appendChild(t);
    document.getElementById("myTr").appendChild(z);


    var z = document.createElement("TH");
    var t = document.createTextNode("کندل های در معامله");
    z.appendChild(t);
    document.getElementById("myTr").appendChild(z);

    var z = document.createElement("TH");
    var t = document.createTextNode("بازده");
    z.appendChild(t);
    document.getElementById("myTr").appendChild(z);

    var z = document.createElement("TH");
    var t = document.createTextNode("موجودی");
    z.appendChild(t);
    document.getElementById("myTr").appendChild(z);
}

function insert_indicators() {
    indicators['Trend Indicators']['ichimoku'] = {
        'fun_name': 'ichimoku',
        'outputs': {
            'Tenkan-sen': ['line', 'solid'],
            'Kijun-sen': ['line', 'solid'],
            'Senkou Span A': ['line', 'solid'],
            'Senkou Span B': ['line', 'solid'],
            'Chikou Span': ['line', 'solid']
        },
        'params': {
            'conversionLineperiod': 9,
            'BaseLineperiod': 26,
            'LagingB': 52
        },
        'settings': { 'shift': 0 }
    };
    var gp = ['Trend Indicators', 'Momentum Indicators', 'Volatility Indicators', 'Volume Indicators', 'Historical Data'];
    // var gp = {
    //     'Momentum Indicators': 'Momentum Indicators',
    //     'Trend Indicators': 'Trend Indicators',
    //     'Volatility Indicators': 'Volatility Indicators',
    //     'Volume Indicators': 'Volume Indicators',
    //     'Historical data': 'Historical data'
    // };
    var idss = ['shorter', 'draw', 'longer', 'ascending', 'main', 'minor', 'buying shorter', 'buying longer', 'selling shorter', 'selling longer'];
    var indic = {};
    // Object.keys(gp).forEach(function (gn) {
    gp.forEach(function (gn) {
        for (var ids in idss) {
            var place = document.getElementById(idss[ids]);
            var group = document.createElement('optgroup');
            // group.setAttribute('label', gp[gn]);
            group.setAttribute('label', gn);
            place.appendChild(group);
            Object.keys(indicators[gn]).forEach(function (indicator) {
                // indicator = sorted[indicator];
                indic[indicator] = indicators[gn][indicator];

                var ind = document.createElement('option');
                ind.setAttribute('value', indicator);
                t = document.createTextNode(indicator);
                ind.appendChild(t);
                place.appendChild(ind);
            });
        }
    });

    indicators = indic;
    indicators_cross = indicators;
    indicators_cross['config_trade'] = {
        'fun_name': 'config_trade',
        'outputs': { 'real': ['line', 'solid'] },
        'params': { 'stop loss': 0, 'take profit': 0 },
    };
    // indicators_cross['stop loss'] = {
    //     'fun_name':'STOP LOSS',
    //     'outputs':{'real':['line','solid']},
    //     'params':{'value':0},
    // };
    // indicators_cross['take profit'] = {
    //     'fun_name':'TAKE PROFIT',
    //     'outputs':{'real':['line','solid']},
    //     'params':{'value':0},
    // };

    // var sorted = [];
    // for (var key in indicators_cross) {
    //     sorted[sorted.length] = key;
    // }
    // sorted.sort();
}

function insert_param(id) {
    var place = document.getElementById(id + '_param');
    place.innerHTML = '';
    var indicator = document.getElementById(id).value;
    if (indicator != '') {
        indicator = indicators_cross[indicator];

        var out = Object.keys(indicator['outputs']);
        if (out.length > 1) {
            var select = document.createElement('select');
            select.setAttribute('id', id + '_output');
            out.forEach(function (output) {
                var opt = document.createElement('option');
                opt.setAttribute('value', output);
                var txt = document.createTextNode(output);
                opt.appendChild(txt);
                select.appendChild(opt);
            });
            place.appendChild(document.createTextNode(' output : '));
            place.appendChild(select);
        }

        var option = { 'params': '', 'settings': '' };
        Object.keys(option).forEach(function (options) {
            if (indicator[options]) {
                Object.keys(indicator[options]).forEach(function (param) {
                    console.log(options, param);
                    var inp = document.createElement('input');
                    inp.setAttribute('type', 'number');
                    inp.setAttribute('id', id + '_' + param);
                    inp.setAttribute('class', 'input');
                    inp.setAttribute('value', indicator[options][param]);
                    inp.setAttribute('style', 'max-width:5%');
                    if (options === 'settings' && param === 'shift') {
                        inp.addEventListener('change', function () {
                            let val = Math.round(this.value); if (val < 0) { val = -1 * val }; this.value = Math.max(val, 1);
                        });
                    }
                    var t = document.createTextNode(' ' + param + ' : ');
                    place.appendChild(t);
                    place.appendChild(inp);
                });

            }
        });

    }
}

function toggle(obj) {
    document.getElementById('results').style.display = 'block';
    if (!isStrategySaved) {
        isScaned = false;
        isBacktested = false;
    }
    switch (obj.id) {
        case 'scan_button':
            document.getElementById('table_place').style.display = 'none';
            if (!isScaned) {
                scan();
            } else {
                show_market();
            }
            break;
        case 'back_test_button':
            document.getElementById('scan-place').style.display = 'none';
            if (!isBacktested) {
                apply();
            } else {
                document.getElementById('table_place').style.display = 'block';
            }
            break;
        case '':
            document.getElementById('results').style.display = 'block';
            break;
    }
    ['back_test', 'delete_all', 'save', 'scan'].forEach(function (button) {
        var idx = button + '_button';
        var div = document.getElementById(idx);
        if (div) {
            var inititial = 'item';
            if (idx == 'delete_all_button') inititial = 'left negative item';
            if (idx == obj.id) div.className = 'item active';
            else div.className = inititial;
        }
    });
}

// function toggle(obj, div_id) {
//     var div = document.getElementById(div_id);
//     switch (obj.getAttribute('class')) {
//         case 'unhide icon':
//             obj.setAttribute('class', 'hide icon');
//             div.setAttribute('style', 'display: none');
//             break;
//         case 'hide icon':
//             obj.setAttribute('class', 'unhide icon');
//             div.setAttribute('style', 'display: block');
//             break;
//     }
// }
function show_div(id) {
    var idss = ["TSE_Filters", "config_trade", "just draw", "cross", "ascending_main", "more_than", "special_methods", "advance_cross"];
    idss.forEach(function (ids) {
        if (ids != id) {
            document.getElementById(ids).style.display = 'none';
        } else {
            document.getElementById(ids).style.display = 'block';
        }
    });
}

// function waiting(pointer) {
//     document.body.style.cursor = pointer;
//     switch (pointer) {
//         case 'wait':
//             document.getElementById("modal").style.display = 'block';
//             break;
//         case 'default':
//             document.getElementById("modal").style.display = 'none';
//             break;
//     }
// }
function let_draw(data) {
    drawing_tool['status'] = data['status'];
    // console.log(drawing_tool);
}

function call_add(kind) {
    var data = { 'kind': kind };
    switch (kind) {
        case 'more':
            data['ids'] = ['main', 'minor'];
            break;
        case 'ascending':
            data['ids'] = ['ascending'];
            break;
        case 'cross':
            data['ids'] = ['shorter', 'longer'];
            break;
        case 'special':
            data['ids'] = ['special'];
            break;
        case 'candlestick':
            data['ids'] = [kind];
            break;
        case 'draw':
            data['ids'] = [kind];
            break;
        case 'advance_cross':
            data['ids'] = ['buying shorter', 'buying longer', 'selling shorter', 'selling longer'];
            break;
        case 'config_trade':
            data['ids'] = ['config'];
            break;
    }
    add_method(data);
}

function describe(meth) {
    var desc = {
        'ichimoku': 'in progress',
        'MACD(Moving Average Convergence/Divergence)': 'در هنگام خرید MACD بالای خط سیگنال باشد و MACD خط صفر را رو به بالا قطع کند, همچنین در هنگام فروش MACD زیر خط سیگنال باشد و خط صفر را رو به پایین قطع کند.',
    };
    var p = document.getElementById('describe');
    if (meth != "") {
        p.innerHTML = desc[meth];
    } else {
        p.innerHTML = '';
    }
}

function add_method(data) {
    var ids = data['ids'];
    var kind = data['kind'];
    var valid = true;
    var strategy = new Object();
    strategy = {
        'kind': kind,
        'symbol_id': symbol_id,
        'request': 'add',
        'indicators': {},
        'valid': document.getElementById('valid_' + kind).value,
    };
    ids.forEach(function (idx) {
        strategy['indicators'][idx] = {};
        var nsi = document.getElementById(idx).value;
        if (nsi != '' & valid) {
            strategy['indicators'][idx]['name'] = indicators_cross[nsi]['fun_name'];
            var indicator = indicators_cross[nsi];
            var option = { 'params': '', 'settings': '' };
            Object.keys(option).forEach(function (options) {
                strategy['indicators'][idx][options] = {};
                if (indicator[options]) {
                    Object.keys(indicator[options]).forEach(function (param) {
                        var v = document.getElementById(idx + '_' + param).value;
                        strategy['indicators'][idx][options][param] = v;
                    });

                }
            });
            if (data['kind'] != 'candlestick') {
                strategy['indicators'][idx]['output'] = {};
                strategy['indicators'][idx]['output']['name'] = 'real';
                strategy['indicators'][idx]['output']['type'] = indicators_cross[nsi]['outputs']['real'];
            } else {
                strategy['indicators'][idx]['output'] = {};
                strategy['indicators'][idx]['output']['name'] = 'integer';
                strategy['indicators'][idx]['output']['type'] = indicators_cross[nsi]['outputs']['integer'];

            }
            if (document.getElementById(idx + '_output')) {
                var output = document.getElementById(idx + '_output').value;
                strategy['indicators'][idx]['output']['name'] = output;
                strategy['indicators'][idx]['output']['type'] = indicators_cross[nsi]['outputs'][output];
            }
            strategy['indicators'][idx]['apply_to'] = document.getElementById(idx + '_apply').value;
            strategy['indicators'][idx]['outputs'] = {};
            Object.keys(indicators_cross[nsi]['outputs']).forEach(function (output) {
                strategy['indicators'][idx]['outputs'][output] = {};
                strategy['indicators'][idx]['outputs'][output]['type'] = indicators_cross[nsi]['outputs'][output][0];
                strategy['indicators'][idx]['outputs'][output]['dash'] = indicators_cross[nsi]['outputs'][output][1];
                // strategy['indicators'][idx]['outputs'][output]['id'] = give_id();

            });
        } else {
            if (valid) {
                alert('لطفا اندیکاتور ' + translate(idx) + ' را انتخاب کنید.');
                // alert('please choose ' + idx + ' indicator.');
                valid = false;
            }
        }

    });
    if (valid) {
        strategy = check_strategy(strategy);
        switch (document.getElementById(strategy['kind'] + '_chart_place').value) {
            case 'on_chart':
                strategy['chart_place'] = 'on_chart';
                break;
            case 'below_chart':
                strategy['chart_place'] = 'below_chart';
                break;
        }
        var st = JSON.stringify(strategy);
        if (Object.keys(chosen_strategies).indexOf(st) == -1) {
            // are_objects_different(Object.keys(chosen_strategies), [st]);
            // object_stringify(strategy);
            // chosen_strategies[st] = {};
            // strategy['str_brief'] = st;
            calculate_indicators(strategy, false);
        } else {
            alert('فیلتر تکراری است. قبلا اضافه شده است');
            // alert('you already have this method');
        }
    }
}

function check_strategy(strategy) {
    var kind = strategy['kind'];
    switch (kind) {
        case 'ascending':
            strategy['days'] = document.getElementById('days_' + kind).value;
            break;
        // case 'more':
        //     strategy['indicators']['minor']['apply_to'] = document.getElementById('minor_apply').value;
        //     break;
    }
    return strategy
}

function calculate_indicators(strategy, saving_status) {
    var strg = jQuery.extend(true, {}, strategy);
    //    strategy['interval'] = userTimeFrame;
    waiting('wait');
    $.ajax({
        type: 'GET',
        url: "/calculate-filter/" + userTimeFrame,
        data: {
            param: JSON.stringify(strategy),
            //            interval: userTimeFrame;
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        error: function () {
            // chosen_strategies.splice(chosen_strategies.indexOf(strategy['str_brief']), 1);
            // delete chosen_strategies[strategy['str_brief']];
            waiting('default');
            alert('مشکلی پیش آمده است.\n مقدار یکی از پارامترها را اشتباه وارد کرده اید.');
            // alert('Sorry something went wrong \nCheck inputs please.');
        },
        success: function (result) {
            //            isStrategySaved = saving_status;
            changeIsStrategySaved(saving_status);
            console.log('isStrategySaved saving status', isStrategySaved);
            var st = JSON.stringify(strategy);
            chosen_strategies[st] = {};
            strategy['str_brief'] = st;
            strategy['id'] = num_of_charts;
            // console.log(result);
            result = JSON.parse(result);
            // console.log(result);
            // console.log(JSON.parse(result));
            switch (result['type']) {
                case 'second':
                    result_type_2[strategy['id']] = JSON.parse(result['result']);
                    break;
                case 'first':
                    result_type_1[strategy['id']] = JSON.parse(result['result']);
                    break;
                default:
                    // console.log('default');
                    break;
            }
            var candlestick = false;
            if (strategy['kind'] != 'candlestick') {
                Object.keys(strategy['indicators']).forEach(function (chosen) {
                    if (chosen != 'result') {
                        Object.keys(strategy['indicators'][chosen]['outputs']).forEach(function (output) {
                            strategy['indicators'][chosen]['outputs'][output]['id'] = give_id();
                            strg['indicators'][chosen]['outputs'][output]['id'] = strategy['indicators'][chosen]['outputs'][output]['id'];
                            strategy['indicators'][chosen]['outputs'][output]['values'] = JSON.parse(result[chosen][output]);
                        });
                    }
                });
            } else {
                Object.keys(strategy['indicators']).forEach(function (chosen) {
                    if (chosen != 'result') {
                        Object.keys(strategy['indicators'][chosen]['outputs']).forEach(function (output) {
                            var candle = JSON.parse(result[chosen][output]);
                            var candle_area = [];
                            for (var i = 0; i < candle.length; i++) {
                                if (candle[i][1] == 0) {
                                    candle_area.push([candle[i][0], null, null]);
                                } else {
                                    candle_area.push([candle[i][0], 0.95 * ohlc[i][3], 1.05 * ohlc[i][2]]);
                                    candlestick = true;
                                }
                            }
                            strategy['indicators'][chosen]['outputs'][output]['id'] = give_id();
                            strg['indicators'][chosen]['outputs'][output]['id'] = strategy['indicators'][chosen]['outputs'][output]['id'];
                            strategy['indicators'][chosen]['outputs'][output]['values'] = candle_area;
                            strategy['indicators'][chosen]['outputs'][output]['type'] = 'columnrange';
                        });
                    }
                });
            }
            strategy['id_finish'] = num_of_charts - 1;
            strg['id_finish'] = strategy['id_finish'];
            chosen_strategies[strategy['str_brief']] = JSON.stringify(strg);
            if (strategy['kind'] != 'candlestick') {
                add(strategy);
            } else {
                if (candlestick) {
                    add(strategy);
                } else {
                    alert('No ' + strategy['indicators']['candlestick']['name'] + ' detected!');
                }
            }
            waiting('default');
            // if(!isStrategySaved){
            //     waiting('default');                
            // }
        }
    })

}

function add(data) {
    var brief;
    var title;
    var opt = {
        rangeSelector: {
            selected: 1
        },
        plotOptions: {
            series: {
                animation: false
            }
        },
        credits: {
            enabled: false
        },
        legend: {
            enabled: true
        },
        // tooltip: {
        //     crosshairs: true,
        //     shared: true,
        // },
        xAxis: {
            crosshair: true,
            labels: {
                enabled: true
            }
        },

        yAxis: [{ opposite: false }]
    };
    switch (data['kind']) {
        case 'cross':
            var brief1 = give_abr({
                'name': data['indicators']['shorter']['name'],
                'params': data['indicators']['shorter']['params'],
                'output': {
                    'name': data['indicators']['shorter']['output']['name'],
                    'type': data['indicators']['shorter']['output']['type']
                },
            });
            brief = ' و ' + brief1['abr'] + ' قطع دادن ';
            brief1 = give_abr({
                'name': data['indicators']['longer']['name'],
                'params': data['indicators']['longer']['params'],
                'output': {
                    'name': data['indicators']['longer']['output']['name'],
                    'type': data['indicators']['longer']['output']['type']
                },
            });
            brief = brief1['abr'] + brief;
            title = brief;
            break;
        case 'ascending':
            brief = give_abr({
                'name': data['indicators']['ascending']['name'],
                'params': data['indicators']['ascending']['params'],
                'output': {
                    'name': data['indicators']['ascending']['output']['name'],
                    'type': data['indicators']['ascending']['output']['type']
                },
            });
            title = brief['abr'] + 'صعودی یا نزولی بودن';
            brief = title;
            // brief['abr'] + ' be ascending';
            break;
        case 'more':
            var brief1 = give_abr({
                'name': data['indicators']['main']['name'],
                'params': data['indicators']['main']['params'],
                'output': {
                    'name': data['indicators']['main']['output']['name'],
                    'type': data['indicators']['main']['output']['type']
                },
            });
            brief = ' از  ' + brief1['abr'] + ' بیشتر بودن ';
            brief1 = give_abr({
                'name': data['indicators']['minor']['name'],
                'params': data['indicators']['minor']['params'],
                'output': {
                    'name': data['indicators']['minor']['output']['name'],
                    'type': data['indicators']['minor']['output']['type']
                },
            });
            brief = brief1['abr'] + brief;
            title = brief;

            break;
        case 'special':
            brief = give_abr({
                'name': data['indicators']['special']['name'],
                'params': data['indicators']['special']['params'],
                'output': {
                    'name': data['indicators']['special']['output']['name'],
                    'type': data['indicators']['special']['output']['type']
                },
            });
            title = brief['abr'] + ' روش ویژه ';
            brief = title;
            // brief['abr'] + ' special method';
            break;
        case 'draw':
            brief = give_abr({
                'name': data['indicators']['draw']['name'],
                'params': data['indicators']['draw']['params'],
                'output': {
                    'name': 'real',
                    'type': data['indicators']['draw']['output']['type']
                },
            });
            title = brief['abr'] + 'رسم ';
            brief = title;
            // 'draw ' + brief['abr'];
            break;
        case 'candlestick':
            brief = give_abr({
                'name': data['indicators']['candlestick']['name'],
                'params': data['indicators']['candlestick']['params'],
                'output': {
                    'name': data['indicators']['candlestick']['output']['name'],
                    'type': data['indicators']['candlestick']['output']['type']
                },
            });
            title = 'Detect ' + brief['abr'];
            brief = 'Detecting ' + brief['abr'];
            break;
        case 'advance_cross':
            brief1 = give_abr({
                'name': data['indicators']['buying shorter']['name'],
                'params': data['indicators']['buying shorter']['params'],
                'output': {
                    'name': data['indicators']['buying shorter']['output']['name'],
                    'type': data['indicators']['buying shorter']['output']['type']
                },
            });
            brief = ' و ' + brief1['abr'] + ' قطع دادن ';
            brief1 = give_abr({
                'name': data['indicators']['buying longer']['name'],
                'params': data['indicators']['buying longer']['params'],
                'output': {
                    'name': data['indicators']['buying longer']['output']['name'],
                    'type': data['indicators']['buying longer']['output']['type']
                },
            });
            brief = ' رو به بالا و ' + brief1['abr'] + brief;

            brief1 = give_abr({
                'name': data['indicators']['selling shorter']['name'],
                'params': data['indicators']['selling shorter']['params'],
                'output': {
                    'name': data['indicators']['selling shorter']['output']['name'],
                    'type': data['indicators']['selling shorter']['output']['type']
                },
            });
            brief = ' با ' + brief1['abr'] + brief;
            brief1 = give_abr({
                'name': data['indicators']['selling longer']['name'],
                'params': data['indicators']['selling longer']['params'],
                'output': {
                    'name': data['indicators']['selling longer']['output']['name'],
                    'type': data['indicators']['selling longer']['output']['type']
                },
            });
            brief = ' رو به پایین' + brief1['abr'] + brief;
            title = ' قطع دادن پیشرفته ';
            break;
    }
    var chart;
    // switch (document.getElementById(data['kind'] + '_chart_place').value) {
    switch (data['chart_place']) {
        case 'on_chart':
            chart = $('#container').highcharts();
            break;
        case 'below_chart':
            opt['title'] = {};
            opt['title']['text'] = title;
            $('<div class="chart" style="height: 100px; min-height: 500px" id =div' + data['id'] + ' >')
                .appendTo('#container1')
                .highcharts('StockChart', opt);
            chart = $('#div' + data['id']).highcharts();
            break;
        default:
            break;

    }
    var chosens = [];
    Object.keys(data['indicators']).forEach(function (chosen) {
        var new_indic = Object.assign({}, data['indicators'][chosen]);
        delete new_indic['outputs'];
        delete new_indic['output'];
        new_indic = JSON.stringify(new_indic);
        if (chosens.indexOf(new_indic) == -1) {
            chosens.push(new_indic);
            Object.keys(data['indicators'][chosen]['outputs']).forEach(function (output) {
                var abr = give_abr({
                    'name': data['indicators'][chosen]['name'],
                    'params': data['indicators'][chosen]['params'],
                    'output': { 'name': output, 'type': data['indicators'][chosen]['outputs'][output]['type'] },
                });
                switch (data['indicators'][chosen]['name']) {
                    case 'ichimoku':
                        var ichimoku_normal_outputs = ['Tenkan-sen', 'Kijun-sen', 'Chikou Span'];
                        if (ichimoku_normal_outputs.indexOf(output) != -1) {
                            chart.addSeries({
                                type: abr['type'],
                                name: abr['abr'],
                                dashStyle: abr['dash'],
                                data: data['indicators'][chosen]['outputs'][output]['values'],
                                id: '' + data['indicators'][chosen]['outputs'][output]['id'],
                                dataGrouping: {
                                    units: groupingUnits
                                }
                            });
                        } else {
                            if (output == 'Senkou Span A') {
                                var cloud_sell = [],
                                    cloud_buy = [],
                                    senkouA = data['indicators'][chosen]['outputs'][output]['values'],
                                    senkouB = data['indicators'][chosen]['outputs']['Senkou Span B']['values'];
                                for (var i = 0; i < senkouA.length; i++) {
                                    if (senkouA[i][1] <= senkouB[i][1]) {
                                        cloud_sell.push([
                                            senkouA[i][0],
                                            senkouA[i][1],
                                            senkouB[i][1],
                                        ]);
                                        cloud_buy.push([
                                            senkouA[i][0],
                                            null,
                                            null,
                                        ]);
                                    } else {
                                        cloud_buy.push([
                                            senkouA[i][0],
                                            senkouA[i][1],
                                            senkouB[i][1],
                                        ]);
                                        cloud_sell.push([
                                            senkouA[i][0],
                                            null,
                                            null,
                                        ]);

                                    }
                                }
                                chart.addSeries({
                                    type: 'arearange',
                                    name: 'ichimoku cloud sell',
                                    dashStyle: 'Dash',
                                    data: cloud_sell,
                                    color: '#ff0000',
                                    fillOpacity: 0.3,
                                    id: '' + data['indicators'][chosen]['outputs'][output]['id'],
                                    dataGrouping: {
                                        units: groupingUnits
                                    }
                                });
                                chart.addSeries({
                                    type: 'arearange',
                                    name: 'ichimoku cloud buy',
                                    dashStyle: 'Dash',
                                    data: cloud_buy,
                                    color: '#66ff33',
                                    fillOpacity: 0.3,
                                    id: '' + data['indicators'][chosen]['outputs']['Senkou Span B']['id'],
                                    dataGrouping: {
                                        units: groupingUnits
                                    }
                                });
                            }

                        }
                        break;
                    default:
                        if (data['kind'] != 'candlestick') {
                            chart.addSeries({
                                type: abr['type'],
                                name: abr['abr'],
                                dashStyle: abr['dash'],
                                data: data['indicators'][chosen]['outputs'][output]['values'],
                                id: '' + data['indicators'][chosen]['outputs'][output]['id'],
                                dataGrouping: {
                                    units: groupingUnits
                                }
                            });
                        } else {
                            chart.addSeries({
                                type: abr['type'],
                                name: abr['abr'],
                                dashStyle: abr['dash'],
                                data: data['indicators'][chosen]['outputs'][output]['values'],
                                // color: 'rgba(68, 170, 213, .2)',
                                color: 'rgba(242, 229, 53, .2)',
                                fillOpacity: 0.3,
                                id: '' + data['indicators'][chosen]['outputs'][output]['id'],
                                dataGrouping: {
                                    units: groupingUnits
                                }
                            });
                        }
                        break;
                }
            });
        }
    });
    insert_strategy({ 'brief': brief, 'id': data['id'], 'id_finish': data['id_finish'], 'str_brief': data['str_brief'] });
    check_strategies_number();
}

function give_abr(data) {
    var abr = data['name'];
    var dash = 'solid';
    var params = Object.keys(data['params']);
    if (params.length > 0) {
        abr += ' (';
        var i = 1;
        params.forEach(function (param) {
            if (i > 1) {
                abr += ',' + data['params'][param];
            } else {
                abr += data['params'][param];
            }

            i += 1;
        });
        abr += ')'
    }

    if (data['output']['name'] != 'real' && data['output']['name'] != 'integer') {
        abr += ' ' + data['output']['name'];
    }
    var ind_type;
    ind_type = data['output']['type'];
    dash = data['output']['dash'];
    // switch (data['output']['type']) {
    //     case 'Line':
    //         ind_type = 'line';
    //         break;
    //     case 'Histogram':
    //         ind_type = 'column';
    //         break;
    //     case 'Dashed Line':
    //         ind_type = 'line';
    //         dash = 'Dash';
    //         break;
    //     case 'star':
    //         ind_type = 'line';
    //         dash = 'Dot';
    //         break;
    //     case 'columnrange':
    //         ind_type = 'columnrange';
    //         dash = 'Dash';
    //         break;
    //     default:
    //         ind_type = 'line';
    //         break;
    // }
    return { 'abr': abr, 'type': ind_type, 'dash': dash }
}

function give_id() {
    var i = num_of_charts;
    num_of_charts += 1;
    return i
}

function insert_strategy(data) {
    var div_main = document.getElementById('strategies');
    var div = document.createElement('div');
    div.setAttribute('class', 'field');
    div.setAttribute('id', data['id']);
    div.setAttribute('name', data['id_finish']);
    var ic = document.createElement('i');
    //    ic.setAttribute('class', 'icon checkmark');
    ic.setAttribute('class', 'trash icon');
    //    ic.setAttribute('style', 'text-align: right; float: right;cursor:pointer;margin-right:5%');
    ic.setAttribute('style', 'color:#E35C67;text-align: right; float: right;cursor:pointer;margin-right:5%');
    ic.setAttribute('title', 'حذف فیلتر');
    ic.setAttribute('name', data['str_brief']);
    ic.addEventListener("click", function () {
        del(this.parentElement.id, this.parentElement.getAttribute('name'), this.getAttribute('name'));
        this.parentElement.remove();
        check_strategies_number();
    });
    ic.addEventListener("mouseover", function () {
        this.parentElement.style.color = '#E35C67';
        //        this.setAttribute('class', 'remove icon');
    });
    ic.addEventListener("mouseout", function () {
        this.parentElement.style.color = 'white';
        //        this.setAttribute('class', 'checkmark icon');
    });
    div.appendChild(ic);
    var para = document.createElement("P");
    para.setAttribute('dir', 'ltr');
    var txt = data['brief'];
    para.appendChild(document.createTextNode(txt));
    div.appendChild(para);

    // var del_btn = document.createElement('button');
    // del_btn.appendChild(document.createTextNode('delete'));
    // del_btn.setAttribute('style', 'float: right;');
    // del_btn.setAttribute('title', 'delete');
    // para.appendChild(del_btn);

    div_main.appendChild(div);

}

function del(start, finish, str) {
    delete chosen_strategies[str];
    if (document.getElementById('div' + start)) {
        document.getElementById('div' + start).remove();
    } else {
        var chart = $('#container').highcharts();
        for (var i = 1; i <= num_of_charts; i++) {
            if (i >= start && i <= finish) {
                if (chart.get('' + i)) {
                    chart.get('' + i).remove();
                }
            }
        }
    }
    delete result_type_1[start];
    delete result_type_2[start];
    //    isStrategySaved = false;
    changeIsStrategySaved(false);
}

function update_indicators(c) {
    Object.keys(chosen_strategies).forEach(function (strategy) {
        strategy = JSON.parse(chosen_strategies[strategy]);
        var start = find_first_id(strategy),
            // finish = strategy['id_finish'],
            chart;
        if (document.getElementById('div' + start)) {
            chart = $('#div' + start).highcharts();
        } else {
            chart = $('#container').highcharts();
        }
        Object.keys(strategy['indicators']).forEach(function (type) {
            var params = strategy['indicators'][type];
            params['symbol_id'] = strategy['symbol_id'];
            $.ajax({
                type: 'GET',
                url: "finance/update-indicators",
                data: {
                    param: JSON.stringify({ 'params': params, 'price': c }),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                error: function () {
                    // console.log('Sorry something went wrong \nCheck your network connection please.');
                },
                success: function (result) {
                    var ids = [];
                    Object.keys(params['outputs']).forEach(function (output) {
                        ids.push(params['outputs'][output]['id']);
                    });
                    result = JSON.parse(result);
                    ids.forEach(function (i) {
                        // console.log(i);
                        var series = chart.get('' + i);
                        var l = series.data.length;
                        // d = series.data[l - 1].x;

                        series.data[l - 1].remove();
                        series.addPoint(JSON.parse(result[i])[0], false, true);
                        chart.redraw({ 'animation': { 'duration': 0 } });

                    });
                }
            });
        });
    });
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}


var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};
$(document).ready(function () {
    $('input.prompt').attr('style', 'background-color:white;text-align: right;font-family:IRANSans; border-radius:4px;height: 5vh;');
    $('.ui.search').search({
        type: 'category',
        error: false,
        onResultsClose: function (yes) {
            // console.log(this);
        },
        onSelect: function (result) {
            if (this.id == 'search') {
                var value = result;
                // console.log(value);
                symbol_id = value.symbol_id;
                var backtest_state = document.getElementById('table_place').style.display;
                load_data('/data/get-data/' + symbol_id);
                if (backtest_state === 'block') {
                    delete_all(['back test']);
                }
                // window.history.pushState('page2', 'Title', '/backtest/stock=' + symbol_id);
            } else {
                document.getElementById('portfolio search id').innerHTML = '';
                add_stock(result);
            }
            // console.log(this);
        },
        apiSettings: {
            onResponse: function (serverResponse) {
                var response = {
                    results: {}
                };
                // translate GitHub API response to work with search
                $.each(serverResponse.items, function (index, item) {
                    // console.log(item);
                    var
                        category = item.category || 'Unknown',
                        maxResults = 8
                        ;
                    if (index >= maxResults) {
                        return false;
                    }
                    // create new language category
                    if (response.results[category] === undefined) {
                        response.results[category] = {
                            name: category,
                            results: []
                        };
                    }
                    // add result to category
                    response.results[category].results.push({
                        // symbol_id=self.SymbolId,//symbol id
                        // kind='kind', // price
                        // category=self.ExchangeName,
                        // symbol_name=self.InstrumentName,//title
                        // name=self.InstrumentName,//discription
                        // description='description',
                        // title='title',
                        title: item.symbol_name,
                        description: item.name,
                        price: item.kind,
                        eng_name: 'eng',
                        // item.eng_name,
                        symbol_id: item.symbol_id,
                    });
                });
                return response;
            },
            url: '/data/symbol-search/q={query}'
        }
    });

    $('.ui.search').dblclick(function () {
        $('.ui.search').transition('jiggle');
    });
});

function changeTimeFrame(new_timeFrame) {
    //    console.log(elm.id);
    let selectedTimeFrame = new_timeFrame;
    if (selectedTimeFrame === userTimeFrame) {
        return true
    }
    userTimeFrame = selectedTimeFrame;
    setTimeFrame(userTimeFrame);
    //    isStrategySaved = false;
    changeIsStrategySaved(false);
    isBacktested = false;
    isScaned = false;
    console.log("timeframe changed, isStrategySaved", isStrategySaved);
    load_data('/data/get-data/' + symbol_id);
}
function setTimeFrame(chosen_interval) {
    intervals.forEach(function (interval) {
        document.getElementById(interval).style.backgroundColor = '';
        document.getElementById(interval).style.color = 'black';
    });
    document.getElementById(chosen_interval).style.backgroundColor = '#1c1f32';
    document.getElementById(chosen_interval).style.color = 'white';
    document.getElementById('strategyTimeFrame').value = chosen_interval;
    userTimeFrame = chosen_interval;
}
function changeIsStrategySaved(saving_status) {
    isStrategySaved = saving_status;
    let strategySavingStatusDiv = document.getElementById('strategySavingStatus');
    if (saving_status) {
        strategySavingStatus.value = 'ذخیره شده';
        strategySavingStatus.style.color = '#00ca9d';
    } else {
        strategySavingStatus.value = 'ذخیره نشده';
        strategySavingStatus.style.color = 'rgb(227, 92, 103)';
    }
}


function getWatchLists() {
    let url = '/get-watchlists'
    $.ajax({
        url: url,
        success: function (result) {
            insertWatchlists(result.watchlists);
            //            console.log(result);
        },
    });
}
function insertWatchlists(watchlists) {
    let watchListNamesDiv = document.getElementById('watchListNames');
    watchListNamesDiv.innerHTML = '';
    watchlists.forEach(function (watchlist) {
        watchListNamesDiv.innerHTML += '<option value="' + watchlist.id + '">' + watchlist.name + '</option>'
    });
    //    getWatchLists(watchListNamesDiv.value);
}
function changeWatchList() {
    watchlistId = document.getElementById('watchListNames').value;
    changeIsStrategySaved(false);
}