$(document).ready(function () {
    $("#body").fadeIn();
    $("#loader").fadeOut();
    $("#whitebg").fadeOut();
    $("#checksTable").DataTable();
    $("#checksTable2").DataTable();
    $("#availablefields").DataTable({
        "order": [[ 2, "desc" ]]
    });
    $('#checksTable tbody').on( 'click', 'tr', function () {

        var selectedcheck = $($(this).children()[0]).html();
        console.log(selectedcheck);
        // if going from unselected -> selected, append to container, else remove
        if (!$(this).hasClass('selected')) {
            var newcheck = $("<div></div>").addClass("selectedcheck").html(selectedcheck);
            $(".selectedcheckscontainer").append(newcheck);
            $("#checks_to_execute").val($("#checks_to_execute").val() + "," + selectedcheck);
        }
        else {
            // remove selectedcheck in container matching selectedcheck
            $(".selectedcheckscontainer .selectedcheck:contains(\"" + selectedcheck + "\")").remove();
            deleteValue("," +selectedcheck,"checks_to_execute");
        }
        console.log("New checks val: " + $("#checks_to_execute").val());
        $(this).toggleClass('selected');
    } );

});


// add replaceAll func to String object to remove all occurences of specific text (e.g. removing strings from textarea
(function() {
    if (!String.replaceAll) {
        String.prototype.replaceAll = function replaceAll(replace, value) {
            return this.replace(new RegExp(replace, 'g'), value);
        };
}
}());
// And modify delete function should look like this:

function deleteValue(strtoremove,textareaid) {
    var textarea = document.getElementById(textareaid);
    var data = textarea.value;
    textarea.value = textarea.value.replaceAll(strtoremove, "");
}

function openbulkuploadform(){
    $("#singlehostformcontainer").fadeOut();
    $("#bulkuploadformcontainer").fadeIn();

}
function openaddhostform(){
    $("#singlehostformcontainer").fadeIn();
    $("#bulkuploadformcontainer").fadeOut();
}