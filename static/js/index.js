// Global variables
var tag_str = '';
var order_str = '';


// Starting of filter buttons

// Change the value of the dropdownMenu button when
// user clicks something on the menu
$(".dropdown-menu li a").click(function () {
    let selText = $(this).text();
    $('#dropdownMenuButton1').html(selText);
});


// Get request for filter by drop down button
$(".dropdown-item").click(function (){
    let currentURL = window.location.href;
    currentURL = currentURL.replace('#', '')
    if (currentURL.includes('manufacturers')) { // When doing a get req on manufacturers no / showed up
        currentURL += '/';
    }
    let sortParam = $(this).attr('id');// This is the text that is on the buttons
    if (tag_str == '') {
        currentURL += 'filter?';
    } else {
        currentURL += 'filter?' + tag_str + '&';
    }
    order_str = 'order_by=' + sortParam;
    currentURL += order_str;
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
    if (order_str == '') {
        currentURL += 'filter?';
    } else {
        currentURL += 'filter?' + order_str + '&';
    }
    if (sortParam === 'All') {
        console.log('Hæ');
        tag_str = '';
        currentURL = currentURL.replace('&', '')
    } else {
        tag_str = 'tag=' + sortParam;
        currentURL += tag_str;
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








