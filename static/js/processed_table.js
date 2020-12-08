var $table = $('#table')
var $remove = $('#remove')
var selections = []
let file_names = JSON.parse(res_data).file_names;
let file_status = JSON.parse(res_data).file_status;
let invalidated_file_number = 0

function getIdSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.name
    })
}

function responseHandler(res) {
    $.each(res.rows, function (i, row) {
        row.state = $.inArray(row.id, selections) !== -1
    })
    return res
}

function detailFormatter(index, row) {
    var html = []
    $.each(row, function (key, value) {
        html.push('<p><b>' + key + ':</b> ' + value + '</p>')
    })
    return html.join('')
}

function operateFormatter(value, row, index) {
    return [
        '<a class="like" href="javascript:void(0)" title="Like">',
        '<i class="fa fa-heart"></i>',
        '</a>  ',
        '<a class="remove" href="javascript:void(0)" title="Remove">',
        '<i class="fa fa-trash"></i>',
        '</a>'
    ].join('')
}

window.operateEvents = {
    'click .like': function (e, value, row, index) {
        alert('You click like action, row: ' + JSON.stringify(row))
    },
    'click .remove': function (e, value, row, index) {
        $table.bootstrapTable('remove', {
            field: 'id',
            values: [row.id]
        })
    }
}

function totalTextFormatter(data) {
    return 'Total'
}

function totalNameFormatter(data) {
    return data.length
}

function totalPriceFormatter(data) {
    var field = this.field
    return '$' + data.map(function (row) {
        return +row[field].substring(1)
    }).reduce(function (sum, i) {
        return sum + i
    }, 0)
}

function initTable(invoice_data) {
    $table.bootstrapTable({data: invoice_data})
    $table.on('check.bs.table uncheck.bs.table ' +
        'check-all.bs.table uncheck-all.bs.table',
        function () {
            $remove.prop('disabled', !$table.bootstrapTable('getSelections').length)

            // save your data, here just save the current page
            selections = getIdSelections()
            // push or splice the selections if you want to save all data selections
        })
    $table.on('all.bs.table', function (e, name, args) {
    })
    $remove.click(function () {
        var ids = getIdSelections()
        $table.bootstrapTable('remove', {
            field: 'id',
            values: ids
        })
        $remove.prop('disabled', true)
    })
}

function buttons() {
    return {
        btnCheck: {
            text: 'Check',
            icon: 'fa-check-square',
            event: function () {
                document.location.href = "/modification/" + invalidated_file_number
            },
            attributes: {
                title: 'Check information and validate'
            }
        }
    }
}

function cellStyle(value, row, index) {
    if (value === "Validated") {
        return {
            css: {
                color: 'green'
            }
        }
    } else {
        return {
            css: {
                color: 'red'
            }
        }
    }

}

$(function () {
    let invoice_data = [];
    for (let i = 0; i < file_names.length; i += 1) {
        if (file_status[i] === "0") {
            invoice_data.push({"name": file_names[i], "status": "Invalidated"})
            invalidated_file_number += 1
        } else {
            invoice_data.push({"name": file_names[i], "status": "Validated"})
        }
    }
    if (invalidated_file_number === 0){
        $("[name='btnCheck']").prop('disabled', true)
    }
    console.log(invoice_data)
    initTable(invoice_data)
})

