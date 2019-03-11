$(document).ready( function () {
    /* Make table sortable */
    $('#main_member_list').DataTable({
        paging: false,
        bFilter: true,
        bInfo : false
    });
});
