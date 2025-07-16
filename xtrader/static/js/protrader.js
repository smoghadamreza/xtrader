let words = window.location.href.split('/');
let proTraderBrand = '';
const proTraderId = words[words.length - 1];

window.onload = initPage;
function initPage() {
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
            text: 'ramzservat.com',
            href: 'http://ramzservat.com'
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
    waiting('wait');
    getProfile();
}

function getProfile() {
    $.ajax({
        url: '/social/get-profile/' + proTraderId,
        success: function (result) {
            if (result.s === 302) {
                window.location = result.href;
            }
            waiting('default');
            proTraderBrand = result.proTraderBrand;
            document.getElementById('traderBrand').value = proTraderBrand;
            document.getElementById('subsFee').value = result.subsFee;
            let status = 'لاگین کنید';
            if (result.status === 1) {
                status = 'دنبال شده';
                document.getElementById('unfollow').style.display = 'inline';
                document.getElementById('follow').style.display = 'none';
            }
            document.getElementById('status').value = status;
            if (result.status === 2) {
                status = 'دنبال نشده';
                document.getElementById('status').value = status;
                document.getElementById('status').style.color = 'rgb(227, 92, 103)';
            }
            if (result.status === 3) {
                status = 'تریدر دیگری دارید';
                document.getElementById('status').value = status;
                document.getElementById('status').style.color = 'rgb(227, 92, 103)';
            }
            var seriesOptions = [
                {
                    name: 'btc',
                    data: result.history.btc,
                },
                {
                    name: proTraderBrand,
                    data: result.history.trader,
                },
            ];
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
                title: {
                    text: 'مقایسه عملکرد تریدر با بیت‌کوین'
                },
                subtitle: {
                    text: proTraderBrand.toUpperCase() + ' VS ' + 'BTCUSDT' // dummy text to reserve space for dynamic subtitle
                },
                series: seriesOptions,
            });
        },
        error: function (e) {
            waiting('default');
        },
    });
}

function showRiskModal(action) {
    if (action === 1) {
        $('#followRisk').modal('show');
    } else {
        $('#unfollowRisk').modal('show');
    }
}
function copytrade(action) {
    //  console.log(action, protrader_id);
    //  if (action === 1){
    //    showRiskModal();
    //  }
    $.ajax({
        'url': '/social/copy-trade/follow-toggle',
        'method': 'POST',
        'data': JSON.stringify({
            action: action,
            protrader_brand: proTraderBrand,
        }),
        success: function (result) {
            console.log(result);
            if (result.c === 200) {
                window.location = '/social/trader/' + proTraderBrand;
            } else if (result.c === 302) {
                alert(result.msg);
                window.location = result.href;
            } else {
                alert(result.msg);
            }
        },
        error: function () {

        }
    })
}
