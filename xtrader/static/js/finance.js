var info = {
    "SymbolId": "IRO7SASP0001",
    "InstrumentName": "سجام",
    "InstrumentTitle": "مجتمع سیمان غرب آسیا",
    "InstrumentCode": "309",
    "InstrumentStateCode": "A",
    "InstrumentStateTitle": "مجاز",
    "BaseQuantity": 1.0,
    "BidAsk": [{
        "RowPlace": 1,
        "AskNumber": 1,
        "AskPrice": 853.0,
        "AskQuantity": 5800,
        "BidNumber": 1,
        "BidPrice": 879.0,
        "BidQuantity": 1200
    }, {
        "RowPlace": 2,
        "AskNumber": 2,
        "AskPrice": 852.0,
        "AskQuantity": 60000,
        "BidNumber": 1,
        "BidPrice": 880.0,
        "BidQuantity": 5264
    }, {
        "RowPlace": 3,
        "AskNumber": 1,
        "AskPrice": 841.0,
        "AskQuantity": 4000,
        "BidNumber": 1,
        "BidPrice": 931.0,
        "BidQuantity": 144
    }],
    "BuyGroupCount": 0,
    "BuyGroupVolume": 0,
    "BuyGroupVolumePercentage": 0.0,
    "BuyFirmCount": 0,
    "BuyFirmVolume": 0,
    "BuyFirmVolumePercentage": 0.0,
    "BuyIndividualCount": 10,
    "BuyIndividualVolume": 57721,
    "BuyIndividualVolumePercentage": 100.0,
    "SellFirmCount": 0,
    "SellFirmVolume": 0,
    "SellFirmVolumePercentage": 0.0,
    "SellIndividualCount": 7,
    "SellIndividualVolume": 57721,
    "SellIndividualVolumePercentage": 100.0,
    "ClosingPrice": 854.0,
    "ClosingPriceVariation": -72.00,
    "ClosingPriceVariationPercent": -7.78,
    "CompanyName": "مجتمع سيمان غرب آسيا          ",
    "ExchangeName": "پایه فرابورس",
    "ExchangeCode": "366",
    "FirstTradePrice": 900.0,
    "LastTradePrice": 853.0,
    "LastTradeDate": "2017-04-24T12:30:07",
    "ReferencePrice": 926.00,
    "ReferencePriceVariation": -73.00,
    "ReferencePriceVariationPercent": -7.88,
    "YearHighestTradePrice": 1026.00,
    "YearLowestTradePrice": 521.00,
    "MinimumOrderQuantity": 1,
    "MaximumOrderQuantity": 50000,
    "LowerPriceThreshold": 834.00,
    "UpperPriceThreshold": 1018.00,
    "LowestTradePrice": 850.0,
    "HighestTradePrice": 900.0,
    "PreviousDayPrice": 926.00,
    "TotalNumberOfSharesTraded": 57721,
    "TotalNumberOfTrades": 15.0,
    "TotalTradeValue": 49271653.0,
    "Eps": -2,
    "PricePerEarningGroup": 0.0,
    "PricePerEarning": -427.0,
    "FreeFloatPercent": 0.0,
    "MonthAverageVolume": 410764,
    "InstrumentMarketValue": 1317564010000.0,
    "NumberOfSharesOrBonds": 1542815000
};
/*
 function get_stock_info(){
 var persianlist = {
 "InstrumentTitle":'نام شرکت',
 "InstrumentName":"نماد",
 "InstrumentStateTitle":"وضعیت",
 'Eps':'EPS',
 'PricePerEarning':'P/E',
 'PricePerEarningGroup': 'P/E گروه',
 'InstrumentMarketValue': 'ارزش بازار',
 'TotalTradeValue':'ارزش معاملات',
 'ExchangeName':'بازار',
 }
 var place = document.getElementById('tsetmc');
 place.innerHTML = '';
 Object.keys(persianlist).forEach(function (detail_key) {
 var item = document.createElement('div');
 item.setAttribute('class', 'item');
 var content = document.createElement('div');
 content.setAttribute('class', 'content');
 var p = document.createElement('p');
 p.innerHTML = persianlist[detail_key]+' :';
 content.appendChild(p);

 var description = document.createElement('div');
 description.setAttribute('class', 'description');
 description.setAttribute('style', 'float: left;color: white');
 description.innerHTML = info[detail_key];

 content.appendChild(description);

 item.appendChild(content);
 place.appendChild(item);
 });

 var price_list = {
 'LowerPriceThreshold': 'حداقل قیمت مجاز',
 'UpperPriceThreshold':'حداکثر قیمت مجاز',
 'BuyFirmVolumePercentage':'درصد حجم خرید حقوقی',
 'BuyFirmVolume':'حجم خرید حقوقی',
 'BuyIndividualVolumePercentage':'درصد حجم خرید حقیقی',
 'BuyIndividualVolume':'حجم خرید حقیقی',

 };
 var place = document.getElementById('price');
 place.innerHTML = '';
 Object.keys(price_list).forEach(function (detail_key) {
 var item = document.createElement('div');
 item.setAttribute('class', 'item');
 var content = document.createElement('div');
 content.setAttribute('class', 'content');
 var p = document.createElement('p');
 p.innerHTML = price_list[detail_key]+' :';
 content.appendChild(p);

 var description = document.createElement('div');
 description.setAttribute('class', 'description');
 description.setAttribute('style', 'float: left;color: white');
 description.innerHTML = info[detail_key];

 content.appendChild(description);

 item.appendChild(content);
 place.appendChild(item);
 });

 }
 */


var user_strategy_names;
var user_current_strategy;
function add_new_strategy() {
    var new_name = prompt('برای استراتژی جدید خود یک نام انتخاب کنید', 'جدید ' + (user_strategy_names.length + 1));
    // strategys_name_place = document.getElementById('strategys_name_place'),
    // new_option = document.createElement('option'),
    // text_node = document.createTextNode(new_name);
    if (check_new_name(new_name)) {
        save_filters('default');
        /*
                new_option.appendChild(text_node);
                new_option.setAttribute('id', "strategy name: " + new_name);
                strategys_name_place.appendChild(new_option);
                strategys_name_place.value = new_name;
        */
        create_name_option({ 'new_name': new_name });
        user_current_strategy = new_name;
        isStrategySaved = false;
        // save_filters('default');
        delete_all(['symbol_ids', 'indicators', 'back test', 'filters'], false);
    }
}

function check_new_name(new_name) {
    return new_name
}


function insert_strategys_names() {
    var strategys_name_place = document.getElementById('strategys_name_place');
    strategys_name_place.innerHTML = '';
    user_strategy_names.forEach(function (new_name) {
        create_name_option({ 'new_name': new_name });
        // var new_option = document.createElement('option'),
        //     text_node = document.createTextNode(new_name);
        // new_option.appendChild(text_node);
        // new_option.setAttribute('id', 'strategy name: ' + new_name);
        // strategys_name_place.appendChild(new_option);
    });
}


function load_another_strategy(new_name) {
    delete_all(['symbol_ids', 'indicators', 'back test', 'filters'], false);
    load_strategy({ 'name': new_name });
    // set_strategy_name({'name': new_name});
}



function find_first_id(strategy) {
    var ids = [];
    Object.keys(strategy['indicators']).forEach(function (indicator) {
        Object.keys(strategy['indicators'][indicator]['outputs']).forEach(function (output) {
            ids.push(strategy['indicators'][indicator]['outputs'][output]['id']);
        });
    });
    // console.log(ids);
    return Math.min.apply(null, ids)
}

function load_alternative_strategy(data) {
    /*
     function tasks:
     1. loading another strategy if the current one deleted.
     2. if alternative strategy does not exist pick a default name and create empty strategy.
     input: place and the purpose of calling function.
     */
    var strategys_name_place = document.getElementById('strategys_name_place');
    var names = strategys_name_place.childNodes;
    if (names[0]) {
        load_another_strategy(names[0].value);
        // strategys_name_place.value = names[0].value;
    } else {
        create_name_option({ 'new_name': 'جدید' });
    }
}

function delete_strategy(data) {
    var strategy_name = data['name'],
        opt = document.getElementById("strategy name: " + strategy_name);
    opt.parentNode.removeChild(opt);
    load_alternative_strategy({});
    // var name_place = document.getElementById('strategys_name_place');

}

function create_name_option(data) {
    /*
     task: create another option in select tag strategy names
     */
    var strategys_name_place = document.getElementById('strategys_name_place'),
        new_option = document.createElement('option'),
        new_name = data['new_name'],
        text_node = document.createTextNode(new_name);
    new_option.appendChild(text_node);
    new_option.setAttribute('id', 'strategy name: ' + new_name);
    strategys_name_place.appendChild(new_option);
    strategys_name_place.value = new_name;

}

function set_strategy_name(data) {
    var strategys_name_place = document.getElementById('strategys_name_place'),
        name = data['name'];
    strategys_name_place.value = name;
    user_current_strategy = name;
}

function hadi() {
    setInterval(function () {
        // console.log('working');
        var chart = $('#container').highcharts(),
            series = chart.get('main');
        var y = Math.round((Math.random() - 0.5) * 15),
            l = series.data.length,
            d = series.data[l - 1].x,
            o = series.data[l - 1].open,
            h = series.data[l - 1].high,
            L = series.data[l - 1].low,
            c = series.data[l - 1].close + y;
        d = [d, o, Math.max(h, c), Math.min(L, c), c];
        series.data[l - 1].remove();
        series.addPoint(d, false, true);
        chart.redraw();
        chart.yAxis[0].removePlotLine('plot-line-1');
        chart.yAxis[0].addPlotLine({
            value: c,
            color: 'yellow',
            dashStyle: 'DashDot',
            width: 2,
            id: 'plot-line-1'
        });
        update_indicators({ 'close': c, 'open': o, 'low': L, 'high': h });
    }, 2000);
    // });
}
