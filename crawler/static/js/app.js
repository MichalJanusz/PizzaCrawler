console.log('dziala');

let compare_button = $('#ajax-button');

// wyciągam pierwotne wersje elementów
let ph_div = $('#ph-div');
let domino_div = $('#domino-div');

let ph_html = ph_div.html();
let domino_html = domino_div.html();

let content_div = $('#comparing-content');


// kliknięcie przycisku porównywania
compare_button.click(function(){

    // nadanie początkowych wartości divom
    ph_div.html(ph_html);
    domino_div.html(domino_html);

    // wyłączenie przycisku na czas trwania ajaxa
    compare_button.css("pointer-events", "none");

    // pobieram jakie id wysyła formularz
    let id = $('#id_pizza').val();
    // console.log(id);

    // ajax wysyła zapytanie do url-a obsługującego skrypt scrapingowy dominos
    $.ajax({
        //w GET wysyłam id pizzy która ma zostać sprawdzona
    url: "/json/dominos?pizza=" + id,
        })
        .done(function(data) {
            // pobieram dane zwrócone z JSONa
            let pizza_name = data.name;
            let pizza_price = data.price;
            $('#domino-name').html(pizza_name);
            $('#domino-price').html(pizza_price);

            // podmieniam wewnętrzny html diva dominosa nową wartością utworzoną wyżej
            // domino_div.html(div_new_html);
        });

    // ajax wysyła zapytanie do url-a obsługującego skrypt scrapingowy pizzahut
    $.ajax({
    url: "/json/pizzahut?pizza=" + id,
        })
        .done(function(data) {
            // console.log(data);
            // zmienne z danymmi z JSONa
            let pizza_name = data.name;
            let pizza_price = data.price;
            $('#ph-name').html(pizza_name);
            $('#ph-price').html(pizza_price);
            $('.site-link').toggle();

            // włącza przycisk po skończeniu się ajaxa
            compare_button.css("pointer-events", "auto");

        });

    let div_attr = content_div.attr('style');

    // jeśli div z wynikami jest niewidoczny - pokaż div
    if (div_attr==='display: none;'){
        content_div.slideToggle()
    }


});

let start_order_button = $('#start-order');


start_order_button.click(function() {

    let info = $('#id_additional').val();
    let payment = $('#id_payment').val();


    $.ajax({
        //w GET wysyłam id pizzy która ma zostać sprawdzona
    url: `/test/?additional=${info}&payment=${payment}`,
    })
        .done(function(data) {
            let firstname = data.firstname;
            let lastname = data.lastname;
            let address = `${data.city} ${data.street} ${data.house_nr} ${data.flat_nr}`;
            let phone = data.phone;
            let orderdetails = `${data.order_items} za ${data.order_price}`;
            let info = data.deliveryinstruction;
            $('#firstname').html(firstname);
            $('#lastname').html(lastname);
            $('#address').html(address);
            $('#phone').html(phone);
            $('#details').html(orderdetails);
            $('#info').html(info);
        });
});

