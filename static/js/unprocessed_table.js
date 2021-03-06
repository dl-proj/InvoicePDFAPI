var $table = $('#table')
var $remove = $('#remove')
var selections = []
let file_names = JSON.parse(res_data).file_names;
let selected_files_number = 0;

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
        selections = getIdSelections()
        if (selections.length > 0) {
            $("[name='btnProcess']").prop('disabled', false)
        } else {
            $("[name='btnProcess']").prop('disabled', true)
        }
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

function buttons () {
    return {
        btnProcess: {
            text: 'Process',
            icon: 'fa-file-pdf',
            event: function () {
                let selected_files = getIdSelections();
                selected_files_number = selected_files.length
                let selected_file_str = ""
                for (let i = 0; i < selected_files.length; i += 1){
                    selected_file_str += selected_files[i] + ","
                }
                if (selected_files.length !== 0){
                    $.post("/unprocessed_files",
                    {
                        file_names: selected_file_str
                    },
                    function(data){
                        if (data === "Complete"){
                            document.location.href = '/unprocessed';
                        }
                    });
                    setTimeout(display_status, 100);
                    $('.progress').css("visibility", "visible");
                    display_status()
                }
            }
        }
    }
}

function display_status() {

    $.post('/update', {},
        function(data){
            data = JSON.parse(data);
            let processed_files = data['processed_files']
            let progress_bar_value = Math.ceil(processed_files / selected_files_number * 100);
            console.log(processed_files, selected_files_number)
            if(processed_files !== selected_files_number){

                $('#progressBar').attr('aria-valuenow', progress_bar_value).css('width', progress_bar_value + '%').text(progress_bar_value + '%');
                display_status()
            }
            else {
                $('#progressBar').attr('aria-valuenow', 100) .css('width', 100 + '%').text(100 + '%');
            }
        }
    )
}

$(function () {
    let invoice_data = [];
    for (let i = 0; i < file_names.length; i += 1){
        invoice_data.push({"name": file_names[i]})
    }
    console.log(invoice_data)
    initTable(invoice_data)
})

