// Global variables
var tagStr = '';
var orderStr = '';
const baseUrl = 'http://127.0.0.1:8000';

// Starting of filter buttons

// Change the value of the dropdownMenu button when
// user clicks something on the menu
$("#sort-dropdown li a").click(function () {
    let selText = $(this).text();
    $('#dropdownMenuButton1').html(selText);
});


// Get request for filter by drop down button
$(".sort-dropitem").click(function (){
    let currentURL = window.location.href;
    currentURL = currentURL.replace('#', '')
    if (currentURL.includes('manufacturers')) { // When doing a get req on manufacturers no / showed up
        currentURL += '/';
    }
    let sortParam = $(this).attr('id');// This is the text that is on the buttons
    if (tagStr == '') {
        currentURL += 'filter?';
    } else {
        currentURL += 'filter?' + tagStr + '&';
    }
    orderStr = 'order_by=' + sortParam;
    currentURL += orderStr;
    $.ajax({
        url: currentURL,
        type: 'GET',
        dataType: 'json',
        success: function (res){
            let newHTML = res.map( d=>{
                return templateString(d)
            });
            $('#product-row').html(newHTML.join(''));
        }
    });
});

// End of filter buttons

// Start of categories buttons

$('.categories').click(function (){
    let sortParam = $(this).text();
    let currentURL = window.location.href;
    currentURL = currentURL.replace('#',''); // The # was not helping, we dont know why it appears
    if (currentURL.includes('manufacturers')) { // When doing a get req on manufacturers no / showed up
        currentURL += '/';
    }
    if (orderStr == '') {
        currentURL += 'filter?';
    } else {
        currentURL += 'filter?' + orderStr + '&';
    }
    if (sortParam === 'All') {
        console.log('Hæ');
        tagStr = '';
        currentURL = currentURL.replace('&', '')
    } else {
        tagStr = 'tag=' + sortParam;
        currentURL += tagStr;
    }
   $.ajax({
       url: currentURL,
       type: 'GET',
       success: function (res){
           let newHTML = res.map( d=>{
                return templateString(d)
            });
            $('#product-row').html(newHTML.join(''));
       }
   })
});

// end of categories buttons
function templateString(d) {
        return `
                   <div class="product top-buffer col-xl-4 col-lg-4 col-md-6 col-sm-12 col-12 border" id="single-prod">
                     <a href="../products/${d.id}" class="text-decoration-none">
                        <div class="shop-default shop-cards shop-tech">
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="block product border z-depth-2-top z-depth-2--hover">
                                        <div class="block-image">
                                                <img src="${d.first_image}" class="img-center">
                                        </div>
                                        <div class="block-body text-center">
                                            <h3 class="heading heading-5 strong-600 text-capitalize">
                                                ${d.name}
                                            </h3>
                                            <p class="product-description">
                                                ${d.weight} g
                                            </p>
                                            <p class="product-price" style="color:black;">${d.price} ISK</p>
                                            <div class="product-buttons mt-4">
                                                <div class="row align-items-center">
                                                    <div class="col-2">
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </a>
                </div>`

}

// Search bar
$('.form-control').keypress(function (event){
   if (event.keyCode == 13){
       event.preventDefault();
       let keyword = $(this).val();
       let filter = {
           'keyword': keyword
       };
       if (tagStr !== '') {
           filter['tag'] = tagStr.split('=')[1];
       }
       if (orderStr !== '') {
           filter['tag'] = orderStr.split('=')[1];
       }
       $.ajax({
           url: baseUrl + '/search',
           type: 'GET',
           data: filter,
           dataType: 'json',
           success: function (res){
               let newHTML = res.map(d => {
                    return templateString(d)
                });
                $('#product-row').html(newHTML.join(''));
           }
       });


   };
});



// Get req for search history
$('#our-searchbar').click(function (event){ // Pick the searchbar
    event.preventDefault();

    $.ajax({
        url: baseUrl + '/history',
        type: 'GET',
        dataType: 'json',
        success: function (res){
            let newHTML = res.map(d => {
                return `
                <li id="${d.id}" class="dropdown-item search-keyword">${d.keyword}</li>
                `
            });
            $('.search-drop-menu').html(newHTML.join('')); // pick the dropdown menu ul tag
        }
    })
})

$('.search-drop-menu').on("click",".search-keyword", function (event){
    let selText = $(this).text();
    $('#our-searchbar').val(selText);
    $('#our-searchbar').focus();
});


// Change the search history text value to the desired value
// end of search bar

// Cart functionality
function addOneToCart (event, amount=1) {
    let prodId = event.id;
    let url = baseUrl + '/orders/cart';
    axios.post(url, {product: prodId, volume: amount})
        .then(function (response) {
            getCartNumber()

        })
        .catch(function (error) {

        });
}

function getCartNumber(){
    let url = baseUrl + '/orders/cart/count'
    axios.get(url)
        .then(function (res){
            console.log(res.data);
            // Add number to cart html here
            let cartNumberTag = document.getElementById('cart-number');
            console.log(cartNumberTag.id);
            cartNumberTag.innerText = res.data;

        })
        .catch(function (err){
        console.log(err);
    });
}


function deleteFromCart(event) {
    // Get the div, and remove it
    let row = document.getElementById("product" + event.id)
    row.remove()
    axios.post(baseUrl +'/orders/cart/remove',{id: event.id})
        .then(function (res){
            getCartNumber()
            getCartTotal()
        })
        .catch(function(err){
           console.log(err);
        });

}

function getCartTotal(){
    let url = baseUrl + '/orders/cart/total'
    axios.get(url)
        .then(function (res){
            // Add number to cart html here
            console.log(res.data);
            let cartTotal = document.getElementById('cart-total');
            cartTotal.innerText = res.data;

        })
        .catch(function (err){
            console.log(err);
    });
}
    //let url = baseUrl + /cart
    //let productId = event.id
    //axios.delete(url, {id: productId})

function confirmOrder () {

    let url = baseUrl + '/orders/confirm'
    axios.post(url)
        .then(function (res){
            window.location.href = baseUrl + '/orders/gratz';

        })
        .catch(function (err){
            console.log(err);
    });
};



function AddManyToCart(event){
    // Get the number from the quantity input field
    // Add this product to cart with this much quantity
    let amount = document.getElementById('product-quantity').value;
    amount = parseInt(amount);
    addOneToCart(event, amount);
}

// Quantity functionality


$('.prod-details-incr').click(function(e){
    e.preventDefault();

    fieldName = $(this).attr('data-field');
    type      = $(this).attr('data-type');
    var input = $("input[name='"+fieldName+"']");
    var currentVal = parseInt(input.val());
    if (!isNaN(currentVal)) {
        if(type == 'minus') {

            if(currentVal > input.attr('min')) {
                input.val(currentVal - 1).change();
            }
            if(parseInt(input.val()) == input.attr('min')) {
                $(this).attr('disabled', true);
            }

        } else if(type == 'plus') {

            if(currentVal < input.attr('max')) {
                input.val(currentVal + 1).change();
            }
            if(parseInt(input.val()) == input.attr('max')) {
                $(this).attr('disabled', true);
            }

        }
    } else {
        input.val(0);
    }
});
$('.prod-details-amount').focusin(function(){
   $(this).data('oldValue', $(this).val());
});
$('.prod-details-amount').change(function() {

    minValue =  parseInt($(this).attr('min'));
    maxValue =  parseInt($(this).attr('max'));
    valueCurrent = parseInt($(this).val());

    name = $(this).attr('name');
    if(valueCurrent >= minValue) {
        $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the minimum value was reached');
        $(this).val($(this).data('oldValue'));
    }
    if(valueCurrent <= maxValue) {
        $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the maximum value was reached');
        $(this).val($(this).data('oldValue'));
    }


});
$(".prod-details-amount").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });


// functionality for plus and minus in cart

function incrementQuantity(ev){ // increment the item in cart by one
    let parentDiv = ev.parentNode;
    let currentAmount = parentDiv.querySelector('span').innerHTML;
    let productPrice = parentDiv.id;
    let currentPrice = document.getElementById('current-item-price' + ev.id).innerHTML;
    let cartTotal = document.getElementById('cart-total').innerText;
    let maxValue = parentDiv.querySelector('span').getAttribute('max');

    // Increment the html tag by 1
    parentDiv.querySelector('span').innerHTML = (parseInt(currentAmount) + 1).toString();
    currentAmount = parentDiv.querySelector('span').innerHTML

    if(parseInt(currentAmount) > parseInt(maxValue)){ // maximum value
        parentDiv.querySelector('span').innerHTML = maxValue.toString()
        alert('Sorry the maximum value was reached')
        return;
    }

    // Check if the html tag has reached it max value or not, if so then throw alert and back out of the process

    addOneToCart(ev);

    // Increment the price of the item by 1 product
    let updatedPrice = parseInt(currentPrice) + parseInt(productPrice) + ' isk';
    document.getElementById('current-item-price' + ev.id).innerHTML = updatedPrice;

    let updatedCartTotal = parseInt(cartTotal) + parseInt(productPrice);
    document.getElementById('cart-total').innerText = updatedCartTotal + ' isk'


}

function decrementQuantity(ev){ // decrement the item in cart by one
    let parentDiv = ev.parentNode;
    let currentAmount = parentDiv.querySelector('span').innerHTML;
    let productPrice = parentDiv.id;
    let currentPrice = document.getElementById('current-item-price' + ev.id).innerHTML;
    let cartTotal = document.getElementById('cart-total').innerText;
    let minValue = parentDiv.querySelector('span').getAttribute('min');



    // Decrement the html tag by 1
    parentDiv.querySelector('span').innerHTML = (parseInt(currentAmount) - 1).toString();
    currentAmount = parentDiv.querySelector('span').innerHTML

    // Delete one from cart
    if(parseInt(currentAmount) < parseInt(minValue)){ // minimum value value
        deleteFromCart(ev);
        return;
    } else {
        deleteOneFromCart(ev);
        return;
    }
    // Increment the price of the item by 1 product
    let updatedPrice = parseInt(currentPrice) - parseInt(productPrice) + ' isk';
    document.getElementById('current-item-price' + ev.id).innerHTML = updatedPrice;

    let updatedCartTotal = parseInt(cartTotal) - parseInt(productPrice);
    document.getElementById('cart-total').innerText = updatedCartTotal + ' isk'
}

function deleteOneFromCart(event){
    // Get the number from the quantity input field
    // Add this product to cart with this much quantity
    let amount = -1;
    addOneToCart(event, amount);
}





