function quick_check(str) {
    if (!isNaN(str)) {
        var sign = '';
        if (Number(str) < 0) {
            str = -1 * Number(str);
            sign = '-';
        }
        str = String(str);
        var str1 = '',
            str2 = '',
            l = str.length;
        for (var i = 0; i < l; i++) {
            if (str.substring(i, i + 1) === '.') {
                str2 = str.substring(i + 1, l);
                str2 = '.' + str2;
                break
            } else {
                str1 += str.substring(i, i + 1);
            }
        }
        // let l = str.length;
        // if(l>6 && l<=9){
        //     return str.substring(0,l-6)+'.'+str.substring(l-6,l-5)+' M'
        // }
        // if(l>9){
        //     return quick_check(str.substring(0,l-9)) +'.'+str.substring(l-9,l-8)+' B'
        // }
        return sign + numberSeparator(str1) + str2;
    } else {
        return str
    }
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

$(document).ready(function () {
    //    $('input.prompt').attr('style', 'background-color:white;text-align: right;font-family:IRANSans; border-radius:4px;height: 5vh;');
    $('#search > div.ui.icon.input > input').attr('style', 'background-color:white;text-align: right;font-family:IRANSans; border-radius:4px;height: 5vh;');
    $('#search').search({
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
                var backtest_state = '';
                //document.getElementById('table_place').style.display;
                window.location = '/spot/' + symbol_id;
                if (backtest_state == 'block') {
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
                        title: item.symbol_name,
                        description: item.name,
                        price: item.kind,
                        eng_name: 'eng',
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

function waiting(pointer) {
    document.body.style.cursor = pointer;
    switch (pointer) {
        case 'wait':
            document.getElementById("modal").style.display = 'block';
            break;
        case 'default':
            document.getElementById("modal").style.display = 'none';
            break;
    }
}
