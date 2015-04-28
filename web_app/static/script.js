jQuery(document).ready(function ()
    {
        $("input[name='group1']").change(radioValueChanged);
        $("#search").bind("click", search);
    })


function search() {
    radioValue = $("input:radio[name ='group1']:checked").val();

    if(radioValue == "server")
    {
        data = $('#server_form').serializeArray();
        $('#component_table').hide();
        $('#server_table').show();
        $("#server_table tr:gt(0)").remove();


        fv = []
        $("#server_fuel_verions").children("input:checked").map(function() {
            fv.push(this.value)
            return this.value;
        });
        server_name = $("#server_name").val()

        $.ajax({
            type: "POST",
            traditional : true,
            data: {name: server_name, fuel_versions: JSON.stringify(fv)},
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
        data = $('#component_form').serializeArray();
        $("#component_table tr:gt(0)").remove();
        fv = []
        $("#component_fuel_verions").children("input:checked").map(function() {
            fv.push(this.value)
            return this.value;
        });
        types = [$("#component_types").val()]
        server_name = $('#server_name2').val()
        name = $('#component_name').val()

        $.ajax({
            type: "POST",
            url: '/api/search/component',
            dataType : "json",
            traditional : true,
            data: {name: name,
                   server: server_name,
                   types: JSON.stringify(types),
                   fuel_versions: JSON.stringify(fv)},
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