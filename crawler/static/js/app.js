console.log('dziala');

let button = $('#ajax-button');

// wyciągam pierwotne wersje elementów
let ph_div = $('#ph-div');
let domino_div = $('#domino-div');

let ph_html = ph_div.html();
let domino_html = domino_div.html();

let content_div = $('#comparing-content');


// kliknięcie przycisku porównywania
button.click(function(){

    // nadanie początkowych wartości divom
    ph_div.html(ph_html);
    domino_div.html(domino_html);

    // wyłączenie przycisku na czas trwania ajaxa
    button.css("pointer-events", "none");

    // pobieram jakie id wysyła formularz i wypisuje to w konsoli
    let id = $('#id_pizza').val();
    console.log(id);

    // ajax wysyła zapytanie do url-a obsługującego skrypt scrapingowy dominos
    $.ajax({
        //w GET wysyłam id pizzy która ma zostać sprawdzona
    url: "json/dominos?pizza=" + id,
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
    url: "json/pizzahut?pizza=" + id,
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
            button.css("pointer-events", "auto");

        });

    let div_attr = content_div.attr('style');

    // jeśli div z wynikami jest niewidoczny - pokaż div
    if (div_attr==='display: none;'){
        content_div.slideToggle()
    }


});



