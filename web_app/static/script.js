jQuery(document).ready(function ()
    {
        $("input[name='group1']").change(radioValueChanged);
        $("#search").bind("click", search);
    })


function search() {
    data = $('#server_form').serializeArray();
    radioValue = $("input:radio[name ='group1']:checked").val();

    if(radioValue == "server")
    {
        $('#component_table').hide();
        $('#server_table').show();

        $.ajax({
            type: "POST",
            data: data,
            url: '/api/search/server',
            dataType : "json",
            success: function (data, textStatus) {
                $.each(data, function(i, val) {
                         row = "<tr> \
                             <td>" + val.name + "</td> \
                             <td>" + val.vendor + "</td> \
                             <td>" + val.fuel_version + "</td> \
                             <td>" + val.specification_url + "</td> \
                             <td>" + val.availability + "</td> \
                             <td>" + val.comments + "</td> \
                             </tr>"

                        $("#server_table").append(row)
                });
            }
        });
    }
    else
    {
        $('#component_table').show();
        $('#server_table').hide();
        data = $('#component_form').serializeArray()
        $.ajax({
            type: "POST",
            url: '/api/search/component',
            dataType : "json",
            data: data,
            success: function (data, textStatus) {
                $.each(data, function(i, val) {
                    $.each(data, function(i, val) {
                         row = "<tr> \
                             <td>" + val.name + "</td> \
                             <td>" + val.vendor + "</td> \
                             <td>" + val.type + "</td> \
                             <td>" + val.hw_id + "</td> \
                             <td>" + val.driver + "</td> \
                             <td>" + val.fuel_versions + "</td> \
                             <td>" + val.comments + "</td> \
                             </tr>"

                        $("#component_table").append(row)
                    });
                });
            }
        });
    }
}


function radioValueChanged() {
    radioValue = $(this).val();
    if($(this).is(":checked") && radioValue == "server")
    {
        $('#component_form').hide();
        $('#server_form').show();
    }
    else
    {
        $('#server_form').hide();
        $('#component_form').show();
    }
}