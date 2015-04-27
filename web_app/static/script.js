jQuery(document).ready(function ()
    {
        $("input[name='group1']").change(radioValueChanged);
    })


function radioValueChanged()
{
    radioValue = $(this).val();
    if($(this).is(":checked") && radioValue == "server")
    {
        $('#component_params').hide();
    }
    else
    {
        $('#component_params').show();
    }
}