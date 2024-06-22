$(document).ready(function(){

    var csrf = $("input[name=csrfmiddlewaretoken]").val(); 
    
    $(document).on('change', '[type="range"]',
        function() {
            $.ajax({
                url:"",
                type:'post',
                data: {                    
                    sli: $(this).val(),
                    csrfmiddlewaretoken:csrf
                },
                success: function(response){
                    $("#summarize").text(response.summary)
                }
            });
            // console.log($(this).val());
    });

    $("#com_button").click(
        function() {
            $.ajax({
                url:"",
                type:'post',
                data: {                    
                    left_book: $('#book_sel').val(),
                    right_book: $('#book_sel_2').val(),
                    csrfmiddlewaretoken:csrf
                },
                success: function(response){
                    $("#sim_res").text(response.sim_value)           
                }
            });
            // console.log($('#book_sel').val());
            // console.log($('#book_sel_2').val());
    });
});