/**
 * Created by hadi on 7/5/17.
 */


var filter_ids = [];
var choosen_filters = {};
// $(document).ready(function () {
//     $.ajax({
//         url:'http://localhost:8000/get-filters',
//         success:function (givenfilters) {
//             var filters_data = JSON.parse(givenfilters);
//             insertfilters(filters_data);
//             read_filters();
//             $("select").change(function () {
//                 read_filters();
//             });
//         },
//         error: function (e) {
//             console.log(e)
//         }
//     });
// });
//

function insertfilters(filters) {
    filters.forEach(function (kind) {
        var filters_div = document.getElementById(kind['kind']),
            column_num = 4, tr, counter = 0;
        kind['filters'].forEach(function (filter) {
            filter['target'].forEach(function (target) {
                if (counter == 0) tr = document.createElement('tr');
                var name = Object.keys(target)[0];
                tr = insertFilterName(tr, target[name]);
                var select = document.createElement('select'),
                    options = filter['benchmark'];
                select.setAttribute('class', 'selectpicker');
                tr = insertFilterOptions(tr, name, select, options);
                select.setAttribute('id', name);
                filter_ids.push(name);
                if (counter == 4) filters_div.appendChild(tr);
                counter = (counter + 1) % column_num;
            });
            filters_div.appendChild(tr);
        });

    });
}

function insertFilterName(tr, name) {
    var td = document.createElement('td');
    td.setAttribute('class', 'filter-name');
    td.innerHTML = name;
    tr.appendChild(td);
    return tr
}

function insertFilterOptions(tr, name, select, options) {
    var td = document.createElement('td'),
        operators = { '__lt': 'کمتر از ', '__gt': 'بیشتر از ' };
    var option = document.createElement('option');
    option.innerHTML = 'همه';
    option.setAttribute('value', '');
    select.appendChild(option);
    Object.keys(operators).forEach(function (operator) {
        options.forEach(function (opt) {
            var option = document.createElement('option');
            option.innerHTML = operators[operator] + quick_check(opt);
            var d = {};
            d[name + operator] = opt;
            option.setAttribute('value', JSON.stringify(d));
            select.appendChild(option);
        });
        td.appendChild(select);
        tr.appendChild(td);
    });
    return tr
}
function read_filters(page) {
    filter_ids.forEach(function (filter) {
        var select = document.getElementById(filter);
        if (!select.value == '') {
            choosen_filters[filter] = select.value;
            select.style.background = '#00CA9D';
        } else {
            select.style.background = '#4d5068';
            if (choosen_filters[filter]) {
                delete choosen_filters[filter];
            }
        }
    });
    var filters_list = [];
    Object.keys(choosen_filters).forEach(function (filter) {
        filters_list.push(choosen_filters[filter]);
    });
    filter_market(filters_list, page);
}

function filter_market(filters, page) {
    waiting('wait');
    $.ajax({
        type: 'GET',
        url: "/filter-market?page=" + page,
        data: {
            filters: JSON.stringify(filters),
            sort_by: JSON.stringify(sort_by),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        error: function () {
            // alert('متاسفانه هنگام دخیره کردن استراتژی شما مشکلی پیش آمده است,\n لطفا بعدا تلاش کنید.');
            waiting('default');
        },
        success: function (result) {
            $('#filters_scan_place').html(result);
            waiting('default');
        }
    });
}

///////////////////////////////////////////////////////////////////////////////////////////////
var mn = $(".main-nav");
mns = "main-nav-scrolled";
hdr = $('header').height();

$(window).scroll(function () {
    if ($(this).scrollTop() > hdr) {
        mn.addClass(mns);
    } else {
        mn.removeClass(mns);
    }
});

function sortTable(n, tablekind) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("table_" + tablekind);
    switching = true;
    //Set the sorting direction to ascending:
    dir = "asc";
    /*Make a loop that will continue until
     no switching has been done:*/
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.getElementsByClassName('divTableRow');
        /*Loop through all table rows (except the
         first, which contains table headers):*/
        for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
             one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("DIV")[n];
            y = rows[i + 1].getElementsByTagName("DIV")[n];
            /*check if the two rows should switch place,
             based on the direction, asc or desc:*/
            // console.log(Number(x.innerHTML.toLowerCase()) + 22);
            if (dir == "asc") {
                if (Number(x.innerHTML.toLowerCase()) > Number(y.innerHTML.toLowerCase())) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (Number(x.innerHTML.toLowerCase()) < Number(y.innerHTML.toLowerCase())) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /*If a switch has been marked, make the switch
             and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            //Each time a switch is done, increase this count by 1:
            switchcount++;
        } else {
            /*If no switching has been done AND the direction is "asc",
             set the direction to "desc" and run the while loop again.*/
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
    recoloring(dir, n);
}
var sort_by;
function recoloring(dir, n) {
    var table = document.getElementById("table"),
        sort_dict = { 'asc': '', 'desc': '-' },
        rows = table.getElementsByClassName('divTableRow');
    for (i = 1; i < rows.length; i++) {
        if (i % 2 == 1) {
            rows[i].style.background = '#4d5068';
        } else {
            rows[i].style.background = '#1c1f32';
        }
    }
    sort_by = sort_dict[dir] + Object.keys(columns)[n];
}
function reset_filters() {
    filters_data.forEach(function (kind) {
        kind['filters'].forEach(function (filter) {
            filter['target'].forEach(function (target) {
                Object.keys(target).forEach(function (filter_id) {
                    document.getElementById(filter_id).value = '';
                });
            });
        });
    });
    read_filters();
}

function change_dir() {
    var obj = document.getElementById('filters-place'),
        dict = { 'rtl': 'ltr', 'ltr': 'rtl' },
        dir = obj.dir;
    obj.dir = dict[dir];

}

function show_kind(kind) {
    ['stockwatch', 'fundamental'].forEach(function (idd) {
        document.getElementById(idd).style.display = (kind != 'all') ? 'none' : 'block';
    });
    if (kind != 'all') document.getElementById(kind).style.display = 'block';
}

function show_table(tablekind) {
    console.log(tablekind);
    ['_stockwatch', '_ratio', '_balanceSheet', '_income'].forEach(function (idd) {
        document.getElementById(idd).style.background = '#1c1f32';
        document.getElementById('table' + idd).style.display = 'none';
    });
    document.getElementById(tablekind).style.background = '#4d5068';
    document.getElementById('table' + tablekind).style.display = 'block';
}
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
            if (str.substring(i, i + 1) == '.') {
                str2 = str.substring(i + 1, l);
                str2 = '.' + str2;
                break
            } else {
                str1 += str.substring(i, i + 1);
            }
        }
        var l = str.length;
        if (l > 6 & l <= 9) {
            return str.substring(0, l - 6) + '.' + str.substring(l - 6, l - 5) + ' M'
        }
        if (l > 9) {
            return quick_check(str.substring(0, l - 9)) + '.' + str.substring(l - 9, l - 8) + ' B'
        }
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
