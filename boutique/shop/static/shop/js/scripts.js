/*!
* Start Bootstrap - Shop Homepage v5.0.5 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project


document.addEventListener('DOMContentLoaded', function() {

    update_counters();
    add_to_cart();
    remove_from_cart();
    
    
    //setInterval(update_counters, 5000);

    if (document.querySelector('.toggle_watchlist') != undefined) {

        document.querySelectorAll('.toggle_watchlist').forEach(button => {

            const listing_id = button.dataset.listing_id;

            fetch(`/api/watching?listing_id=${listing_id}`)
            .then(response => response.json())
            .then(data => {
                update_button_display(button, data.on_watchlist);
            })
            .catch(error => {
                console.log("*** api/watching error **", error);
            })

            button.onclick = function() {

                const listing_id = this.dataset.listing_id;
                console.log(`Toggle watchlist for listing id=${listing_id}`);
                fetch(`/api/toggle?listing_id=${listing_id}`)
                .then(response => response.json())
                .then(data => {
                    update_button_display(this, data.on_watchlist);
                    update_innerHTML('#mw', data['my_watches'])
                })
                .catch(error => {
                    console.log("*** api/toggle error **", error);
                })
            }
        })
    }
});

function update_button_display(button, watching) {
    console.log(`update_button-dispay: ${button} ${watching}`);
    let filename = button.src;
    if (watching) {
        filename = filename.replace("hollow","filled");
    } else {
        filename = filename.replace("filled","hollow");
    }
    button.src = filename;
}

function update_counters() {
    fetch("/api/counters")
    .then(response => response.json())
    .then(data => {
        update_innerHTML('#cl', data['cart'])
        //update_innerHTML('#ml', data['my_listings'])
        //update_innerHTML('#mw', data['my_watches'])
    })
    .catch(error => {
        console.log('**** api/counters error **', error);
    });
}

function update_innerHTML(element_id, value) {
    if (document.querySelector(element_id) != undefined) {
        document.querySelector(element_id).innerHTML = value;
    }
}

function add_to_cart() {
    
    if (document.querySelector('.add-to-cart-submit') != undefined){

    document.querySelector('#add-to-cart-form').onsubmit = ()=> {
        form = document.querySelector('#add-to-cart-form');
        console.log(form)
        const formData = new FormData(form);
        fetch(form.action, {
            method: "POST",
            body: formData,
            
            
        })
        console.log(formData)
        .then(response => {
            console.log('add: got a response');
            return response.json()})
        .then(data => {
            console.log(`add: data=${data}`)
            //update_counters();

        })
        .catch(error => {
            console.log("*** api/error **", error);
        })

        //document.querySelector('#comment_text').value = ''
        return false;
    }
}
}

function remove_from_cart() {
    
    
    if (document.querySelector('.remove-from-cart-button') != undefined){
        
    document.querySelector('#remove-from-cart-form').onsubmit = ()=> {
        form = document.querySelector('#remove-from-cart-form');
        const formData = new FormData(form);
        fetch(form.action, {
            method: "POST",
            body: formData,
            
        })
        console.log(formData)
        .then(response => {
            console.log('remove: got a response');
            return response.json()})
        .then(data => {
            console.log(`remove: data=${data}`)
            //update_counters();

        })
        //.catch(error => {
            //console.log("*** api/error **", error);
        //})

        //document.querySelector('#comment_text').value = ''
        return false;
    }
}
}
