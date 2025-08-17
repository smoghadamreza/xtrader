let settingItems = [];
let content = [];

function saveExchange() {
    let params = {
        ex_name: document.getElementById('exchangeName').value,
        public: document.getElementById('publicKey').value,
        secret: document.getElementById('secretKey').value,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    };

    if (params.public === "") {
        alert("وارد کردن کلید عمومی اجباری است");

    } else if (params.secret === "") {
        alert("وارد کردن کلید خصوصی اجباری است");
    }
    $.ajax({
        url: '/saveExchange',
        data: params,
        method: 'POST',
        success: function (result) {
            if (result.status) {
                document.getElementById('removeExchange').style.display = 'block';
                document.getElementById('saveExchange').style.display = 'none';
                changeExchangeSetup('disabled');
            } else {
                alert("کلید عمومی یا خصوصی اشتباه است!");
            }
        },
    })
}

function removeExchange() {
    $.ajax({
        url: '/remove-exchange',
        method: 'DELETE',
        success: function (result) {
            if (result.status) {
                document.getElementById('publicKey').value = '';
                document.getElementById('secretKey').value = '';
                document.getElementById('removeExchange').style.display = 'none';
                document.getElementById('saveExchange').style.display = 'block';
                changeExchangeSetup('enabled');
            } else {
                alert("برای پاک کردن اکسچنج ابتدا اتصال ترید در تنظیمات تردینگ ویو را حذف کنید");
            }

        },
    })

}

function getExchange() {
    $.ajax({
        url: '/get-exchanges',
        method: 'GET',
        success: function (result) {
            if (result.api_key) {
                document.getElementById('publicKey').value = result.api_key;
                document.getElementById('secretKey').value = result.secret_key;
                changeExchangeSetup('disabled');
                document.getElementById('removeExchange').style.display = 'block';
                document.getElementById('saveExchange').style.display = 'none';
            }

        },
    })
}

function changeExchangeSetup(status) {
    if (status === 'disabled') {
        document.getElementById('publicKey').setAttribute(status, "");
        document.getElementById('secretKey').setAttribute(status, "");

    } else {
        document.getElementById('publicKey').removeAttribute('disabled');
        document.getElementById('secretKey').removeAttribute("disabled");

    }
}

function getWatchList() {
    $.ajax({
        url: '/data/symbols',
        success: function (result) {
            //        let watchListSymbols = document.getElementById('watchListSymbols');
            //        watchListSymbols.innerHTML = '';
            //        result.symbols.forEach(function (symbol){
            //            watchListSymbols.innerHTML += '<li><a href="/spot/'+symbol+'">'+symbol+'</a></li><br>';
            //        });
        },
    });
}

function initSetup() {
    getExchange();
    getWebhook();
    getTelegram();
    getWatchList();
    getWallet();
    getDeposits();
    setSettingItems();
    go2Setting();
    getWatchLists();
    setSymbols();
    getPackages();
    $('#watchlistsearch > div.ui.icon.input > input').attr('style', 'width: 100%;background-color:white;text-align: right;font-family:IRANSans; border-radius:4px;height: 5vh;');
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
                        // item.eng_name,
                        symbol_id: item.symbol_id,
                    });
                });
                return response;
            },
            url: '/data/symbol-search/q={query}'
        }
    });
}
function setSettingItems() {
    let options = document.getElementById('settingMenu').children;
    for (let i = 0; i < options.length; i++) {
        settingItems.push(options[i].value);
    };
}
function go2Setting() {
    var url_string = window.location.href;
    var url = new URL(url_string);
    var s = url.searchParams.get("s");
    if (settingItems.indexOf(s) > -1) {
        toggleSetup(s);
    }
}
function toggleSetup(itemId) {
    settingItems.forEach(function (item) {
        document.getElementById(item).style.display = 'none';
    });
    document.getElementById(itemId).style.display = 'block';
    document.getElementById('settingMenu').value = itemId;
    console.log(itemId);
}

function webhookSave() {
    $.ajax({
        url: '/trading-view',
        method: 'POST',
        data: JSON.stringify({
            'trading': document.getElementById('webhookTrading').checked,
            'notification': document.getElementById('webhookNotification').checked,
        }),
        success: function (result) {
            let webhook = document.getElementById('webhook');
            webhook.value = result.webhook;
            webhook.setAttribute("disabled", "");
            document.getElementById('webhookTrading').checked = result.trading;
            document.getElementById('webhookNotification').checked = result.notification;
            if (result.msg !== "") {
                alert(result.msg);
            } else {
                alert('تغییرات انجام شد.');
            }
        },
    });

}

function getWebhook() {
    $.ajax({
        url: '/trading-view',
        method: 'GET',
        success: function (result) {
            let webhook = document.getElementById('webhook');
            webhook.value = result.webhook;
            webhook.setAttribute("disabled", "");
            document.getElementById('webhookTrading').checked = result.trading;
            document.getElementById('webhookNotification').checked = result.notification;
        }
    });
}

function getTelegramStatus() {
    $.ajax({
        url: '/accounts/telegram-status/',
        method: 'GET',
        success: function (result) {
            if (result.telegram_id) {
                document.getElementById('telegramStatus').innerHTML = 'اتصال حساب شما به تلگرام انجام شده است.'
                document.getElementById('TelegramActivationCode').style.display = 'none';
                document.getElementById('TelegramActivationGuide').style.display = 'none';
                document.getElementById('telegramCheckButton').style.display = 'none';
            } else {
                document.getElementById('TelegramActivationCodePlace').value = result.activation_code;
                // document.getElementById('TelegramActivationCodePlace').setAttribute("disabled", "");
            }
        }
    });
}
function watchlistMsg(msg, status) {
    let msgBox = document.getElementById('watchlistMsgs');
    msgBox.innerHTML = '<div id="msgPop">' + msg + '</div>';
    if (status === 'error') {
        msgBox.style.color = '#e74c3c';
    } else {
        msgBox.style.color = '#09cac8';
    }
    $('#msgPop').delay(1000).fadeOut('slow');
}
function getWallet() {
    $.ajax({
        url: '/accounts/get-wallet/',
        method: 'GET',
        success: function (result) {
            console.log(result);
            let walletAddress = document.getElementById('walletAddress');
            walletAddress.value = result.address;
            walletAddress.setAttribute("disabled", "");
            document.getElementById('walletBalance').innerHTML = result.balance;
            document.getElementById('walletIncome').innerHTML = result.income;
            document.getElementById('walletBalance2').value = result.balance + ' usdt';
        }
    });
}

function updateWallet() {
    $.ajax({
        url: '/accounts/check-deposits',
        success: function (result) {
            if (result.status === 200) {
                if (result.newDeposit) {
                    getWallet();
                    getDeposits();
                }
            }
        },
    });
}

function getDeposits() {
    document.getElementById('depositsContainer').innerHTML = '<br><table id="depositsTable" class="strip" style="width:99%;"></table>';
    $('#depositsTable').DataTable({
        ajax: '/accounts/get-deposits',
        order: [[0, "desc"]],
        columns: [
            {
                data: 'id',
                title: 'شناسه'
            },
            {
                data: 'amount',
                title: 'مقدار',
                render: $.fn.dataTable.render.number(',', '.', 2, '')
            },
            {
                data: 'coin',
                title: 'کوین',
            },
            {
                data: 'action',
                title: 'عملیات',
            },
            {
                data: 'txid',
                title: 'شناسه تراکنش',
            },
            {
                data: 'time',
                title: 'تاریخ',
            },
        ],
    });
    document.getElementById('depositsTable_length').style.display = 'none';
    document.getElementById('depositsTable_info').style.display = 'none';
    document.getElementById('depositsTable_paginate').style.display = 'none';
    let label = document.querySelector('#depositsTable_filter > label');
    label.style.display = 'none';
    let input = label.children[0];
    label.innerHTML = 'جستجو: ';
    input.placeholder = 'سرمایه‌گذار';
    input.style.display = 'none';
    input.style.fontFamily = 'IranSans';
    label.appendChild(input);

}
window.onload = initSetup;


function addNewWatchList() {
    let watchListName = document.getElementById('watchListName').value;
    if (watchListName) {
        $.ajax({
            url: '/add-new-watchlist',
            method: 'POST',
            data: { 'name': watchListName },
            success: function (result) {
                if (result.s === 200) {
                    let watchListNamesDiv = document.getElementById('watchListNames');
                    watchListNamesDiv.innerHTML = '<option value="' + result.id + '">' + watchListName + '</option>' + watchListNamesDiv.innerHTML;
                    getWatchLists(result.id);
                    watchlistMsg('واچ‌لیست ساخته شد', '');
                    //                    console.log(result.id);
                } else if (result.s === 302) {
                    alert(result.m);
                    window.location = result.redirect;
                } else {
                    alert(result.m);
                }
            },
        });
    } else {
        alert('اسم');
    }
}
function getWatchLists(watchListId, action) {
    let url = '/get-watchlists'
    if (watchListId !== undefined) {
        url += '?id=' + watchListId;
        if (action) {
            url += '&action=' + action;
        }
    }
    $.ajax({
        url: url,
        success: function (result) {
            console.log(result);
            if (result.s === 200) {
                if (watchListId) {
                    if (action === 'remove') {
                        watchlistMsg('واچ‌لیست حذف شد', 'error');
                        getWatchLists();
                    } else {
                        showWatchlistSymbols(result.symbols);
                    }
                } else {
                    insertWatchlists(result.watchlists);
                }
            } else {
                alert(result.m);
            }
        },
    });
}
function showWatchlistSymbols(symbols) {
    let watchListSymbolsDiv = document.getElementById('watchListSymbols');
    watchListSymbolsDiv.innerHTML = '';
    if (symbols.length > 0) {
        let counter = 0;
        console.log("ghe");
        let buttons = '<table style="width: 100%" id="qws"><tr>';
        symbols.forEach(function (symbol) {
            //            watchListSymbolsDiv.innerHTML += '<button class="ui labeled icon mini button"><i class="remove icon" style="background-color:red" onclick="updateSymbol2Watchlist(this.parentElement.innerText, \'remove\')"></i>'+symbol+'</button>';
            buttons += '<td>';
            buttons += '<button class="ui labeled icon mini button" style="width: 80%;"><i title="حذف" class="remove icon" style="background-color:#db2828" onclick="updateSymbol2Watchlist(this.parentElement.innerText, \'remove\')"></i>' + symbol + '</button>';
            buttons += '</td>';

            counter += 1;
            if (counter % 3 === 0) {
                buttons += '</tr><tr>';
            }
        });
        watchListSymbolsDiv.innerHTML = buttons + '</tr></table>';
    } else {
        watchListSymbolsDiv.innerHTML = '<h2>هیچ نمادی انتخاب نشده است.</h2>';
    }
}
function insertWatchlists(watchlists) {
    let watchListNamesDiv = document.getElementById('watchListNames');
    watchListNamesDiv.innerHTML = '';
    watchlists.forEach(function (watchlist) {
        watchListNamesDiv.innerHTML += '<option value="' + watchlist.id + '">' + watchlist.name + '</option>'
    });
    getWatchLists(watchListNamesDiv.value);
}
function removeWatchlist() {
    let watchListId = document.getElementById('watchListNames').value;
    getWatchLists(watchListId, 'remove');
}
function setSymbols() {
    $.ajax({
        url: '/data/all-symbols',
        success: function (response) {
            $('#watchlistsearch').search({
                source: response.symbols,
                onSelect: function (result) {
                    console.log(this);
                    if (this.id == 'watchlistsearch') {
                        var value = result;
                        console.log(value);
                        updateSymbol2Watchlist(result.title, 'add');
                        //                        symbol_id = value.symbol_id;
                        //                        var backtest_state = '';
                        //                        //document.getElementById('table_place').style.display;
                        //                        window.location = '/spot/' + symbol_id;
                        //                        if (backtest_state == 'block') {
                        //                            delete_all(['back test']);
                        //                        }
                    }
                    // window.history.pushState('page2', 'Title', '/backtest/stock=' + symbol_id);
                },
            });
        },
    });
}

function updateSymbol2Watchlist(symbol, action) {
    let watchListId = document.getElementById('watchListNames').value;
    $.ajax({
        url: '/updateSymbol2Watchlist',
        data: { symbol: symbol, action: action, watchListId: watchListId },
        success: function (result) {
            if (result.s === 200) {
                getWatchLists(watchListId);
                if (action === 'remove') {
                    watchlistMsg('نماد از واچ لیست حذف شد', 'error');
                } else {
                    watchlistMsg('نماد به واچ لیست اضافه شد', '');
                }
            } else {
                alert(result.m);
            }
        },
    });
}

function getPackages() {
    $.ajax({
        url: '/sales/packages',
        success: function (result) {
            document.getElementById('myPack').value = result.currentPack.name;
            document.getElementById('myPackEx').value = result.currentPack.expiry;
            document.getElementById('myGasFee').value = result.currentPack.gasFee;
            let packItems = document.getElementById('packageItems');
            packageItems.innerHTML = '';
            let counter = 0;
            result.packages.forEach(function (pack) {
                let featured = '';
                if (counter % 2 === 1) {
                    featured = ' featured';
                }
                let watchListLimit = 0;
                if (pack.price > 0) {
                    watchListLimit = pack.limit;
                }
                let itemDiv = '<div class="plan col' + featured + '">';
                itemDiv += '<div class="plan-title">' + pack.name + '</div>';
                //                itemDiv += '<h3 class="plan-title">' + pack.name + '</h3>';
                itemDiv += '<div class="plan-cost"><span class="plan-price">$' + pack.monthPrice + '</span><span class="plan-type">/ ماهانه</span></div>';
                itemDiv += '<ul class="plan-features">';
                itemDiv += '<li class=""><i class="ion-checkmark"> </i>قیمت: ' + pack.price + ' تتر</li>';
                itemDiv += '<li><i class="ion-checkmark"> </i>اشتراک: ' + pack.days + ' روزه</li>';
                itemDiv += '<li><i class="ion-checkmark"> </i>' + pack.gasFee + ' gasFee</li>';
                itemDiv += '<li><i class="ion-checkmark"> </i>تعداد واچ‌لیست: ' + watchListLimit + '</li>';
                itemDiv += '<li><i class="ion-checkmark"> </i>تعداد استراتژی: ' + pack.limit + '</li>';
                if (pack.price === 0) {
                    itemDiv += '<li class=""><button disabled style="width: 100%" class="positive ui button">رایگان استفاده کنید</button></li>';
                } else {
                    itemDiv += '<li class=""><button style="width: 100%" class="positive ui button" value="' + pack.id + '" onclick="buyPack(this)">خرید</button></li>';
                }

                itemDiv += '</ul>';
                //                itemDiv += '<div class="plan-select"><button style="width: 100%" class="positive ui button">خرید</button></div>';
                //                itemDiv += '<div class="plan-select"><a href="">خرید</a></div>';
                itemDiv += '</div>';
                packageItems.innerHTML += itemDiv;
                counter += 1;
            });
        },
    });
}

function buyPack(elm) {
    $.ajax({
        url: '/sales/subscribe/',
        method: 'POST',
        data: JSON.stringify({ subscribe: parseInt(elm.value) }),
        success: function (result) {
            console.log(result);
            if (result.s === 403) {
                alert(result.m);
            } else {
                location.reload();
            }
        },
    });
    console.log(elm, elm.value);
}


function promote() {
    let brand = document.getElementById('brand').value;
    let subscriptionFee = parseFloat(document.getElementById('subscriptionFee').value);
    if (!brand) {
        alert('لطفا یک نام نمایشی برای خود انتخاب کنید.');
        return 0
    } else if (isNaN(subscriptionFee) || subscriptionFee === null || subscriptionFee === undefined || subscriptionFee < 1) {
        alert('اشتراک ماهانه معتبر نیست.');
        return 0
    }
    $.ajax({
        url: '/social/promote',
        method: 'POST',
        data: JSON.stringify({ brand: brand, subscription: subscriptionFee }),
        success: function (result) {
            if (result.s === 302) {
                alert(result.m);
                window.location = '/profile-setup/?s=' + result.href;
            }
            else if (result.s === 200) {
                alert(result.m);
            }
        },
    });
}