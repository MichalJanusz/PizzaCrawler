console.log('dziala');

let button = $('#ajax_button');

button.click(function(){
    button.css("pointer-events", "none");
    let id = $('#id_pizza').val();
    console.log(id);
    $.ajax({
    url: "json/dominos?pizza=" + id,
        })
        .done(function(data) {
            console.log(data)
        });
    $.ajax({
    url: "json/pizzahut?pizza=" + id,
        })
        .done(function(data) {
            console.log(data);
            button.css("pointer-events", "auto");

        });

    content_div.slideToggle()
});
let content_div = $('#comparing_content');