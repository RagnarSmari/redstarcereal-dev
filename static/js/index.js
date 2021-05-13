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
                                                <p class="product-price">${d.price} ISK</p>
                                                <div class="product-buttons mt-4">
                                                    <div class="row align-items-center">
                                                        <div class="col-2">
                                                            <button type="button" class="btn-icon" data-toggle="tooltip" data-placement="top" title="" data-original-title="Favorite">
                                                                <i class="fa fa-heart"></i>
                                                            </button>
                                                        </div>
                                                        <div class="col-8">
                                                            <button type="button" class="btn btn-block btn-primary btn-circle btn-icon-left">
                                                                <i class="fa fa-shopping-cart"></i>Add to cart
                                                            </button>
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
                                                <p class="product-price">${d.price} ISK</p>
                                                <div class="product-buttons mt-4">
                                                    <div class="row align-items-center">
                                                        <div class="col-2">
                                                            <button type="button" class="btn-icon" data-toggle="tooltip" data-placement="top" title="" data-original-title="Favorite">
                                                                <i class="fa fa-heart"></i>
                                                            </button>
                                                        </div>
                                                        <div class="col-8">
                                                            <button type="button" class="btn btn-block btn-primary btn-circle btn-icon-left">
                                                                <i class="fa fa-shopping-cart"></i>Add to cart
                                                            </button>
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
            });
            $('#product-row').html(newHTML.join(''));
       }
   })
});

// end of categories buttons


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
                                                    <p class="product-price">${d.price} ISK</p>
                                                    <div class="product-buttons mt-4">
                                                        <div class="row align-items-center">
                                                            <div class="col-2">
                                                                <button type="button" class="btn-icon" data-toggle="tooltip" data-placement="top" title="" data-original-title="Favorite">
                                                                    <i class="fa fa-heart"></i>
                                                                </button>
                                                            </div>
                                                            <div class="col-8">
                                                                <button type="button" class="btn btn-block btn-primary btn-circle btn-icon-left">
                                                                    <i class="fa fa-shopping-cart"></i>Add to cart
                                                                </button>
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
function addOneToCart (event) {

    let prodId = event.id
    let amount = 1;
    let url = baseUrl + '/orders/cart';

    axios.post(url,{product: prodId, volume: amount})

        .then(function (response){
            getCartNumber()

        })
        .catch(function (error){

        });
};

function getCartNumber(){
    let url = baseUrl + '/orders/cart/count'
    axios.get(url)
        .then(function (res){
            // Add number to cart html here
            let cartNumberTag = document.getElementById('cart-number');
            cartNumberTag.innerText = res.data;

        })
        .catch(function (err){
        console.log(err);
    });
}


function deleteFromCart(event) {

    axios.post(baseUrl +'/orders/cart/remove',{id: event.id})
        .then(function (res){
            let row = document.getElementById("row" + event.id)
            row.remove()
            getCartNumber()
            getCartTotal()

        })
        .catch(function(err){
           console.log(error)
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








