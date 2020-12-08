let total_files = null;
$(document).ready(function () {
    $('#btnSubmit').click(function () {
        total_files = document.getElementsByName('file')[0]["files"].length;
        if (total_files !== 0) {
            $('form').submit();
            setTimeout(posts, 100);
            $('.progress').css("visibility", "visible");
            posts();
        } else {
            window.alert("Please select the folder to upload!")
        }
    });

    if (res_data !== "") {
        let file_names = JSON.parse(res_data).pdf_file_names;
        console.log(file_names)
        $('#p_file_names').empty()
        $('#p_file_names').append('<option value="0">' + "Select PDF file" + '</option>')
        for (let i = 0; i < file_names.length; i++) {
            $('#p_file_names').append('<option value="' + file_names[i] + '">' + file_names[i] + '</option>')
        }
    }
});
function posts() {

    $.post('/update', {},
        function(data){
            data = JSON.parse(data);
            //do task here
            const processed_files = data['processed_files']
            const progress_bar_value = Math.ceil(processed_files / total_files * 100);

            if(processed_files !== total_files){

                $('#progressBar').attr('aria-valuenow', progress_bar_value)
                    .css('width', progress_bar_value + '%').text(progress_bar_value + '%');

                posts()
            }
        }
    )
}
function showResult() {
    let selected_pdf = $("#p_file_names").val();
    console.log(selected_pdf)
    $.post(
        "/show_result",
        {
            pdf_file: selected_pdf,
        },
        function (data) {
            let invoice_result = JSON.parse(data).invoice_result
            $('#result').css("visibility", "visible");
            $('#barcode').text("Barcode:  " + invoice_result.Barcode)
            $('#liefer').text("Lieferschein Nr:  " + invoice_result.Lieferschein_Nr)
            $('#date').text("DTS_Date:  " + invoice_result.DTS_Date)
            $('#time').text("DTS_Time:  " + invoice_result.DTS_Time)
            $('#gew').text("Gewicht:  " + invoice_result.Gewicht)
            $('#volume').text("Volume:  " + invoice_result.Volume)
            $('#pdf_image').attr('src', "../../static/upload/" + selected_pdf.replace(".pdf", "") + ".jpg")
            $('#pdf_image').css("visibility", "visible");
        }
    )
}
