



// Starting of filter buttons

// Change the value of the dropdownMenu button when
// user clicks something on the menu
$(".dropdown-menu li a").click(function () {
    let selText = $(this).text();
    $('#dropdownMenuButton1').html(selText);
});


// Get request for filter by drop down button
$(".dropdown-item").click(function (){
    let sortParam = $(this).attr('id');// This is the text that is on the buttons
    $.ajax({
        url: "http://localhost:8000/home/filter/?order_by=" + sortParam,
        type: 'GET',
        dataType: 'json',
        success: function (res){
            console.log(res);
            var newHTML = res.map( d=>{
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
   $.ajax({
       url:'',
       type: 'GET',
       success: function (res){
           console.log('Success!!')
       }
   })
});



// end of categories buttons








