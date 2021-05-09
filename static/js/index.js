



// Starting of filter buttons

// Change the value of the dropdownMenu button when
// user clicks something on the menu
$(".dropdown-menu li a").click(function () {
    var selText = $(this).text();
    $('#dropdownMenuButton1').html(selText);
});


// Get request for filter by drop down button
$(".dropdown-item").click(function (){
    let sortParam = $(this).text();// This is the text that is on the buttons
    sortParam = check_sort_param(sortParam);
    console.log(sortParam);
    $.ajax({
        url: "http://localhost:8000/home/?order_by=" + sortParam,
        type: 'GET',
        success: function (res) {
            console.log('success!');
            alert(res);
        }
    })
});


// Get request for filter by drop down button
$(".categories").click(function (){
    $.ajax({
        url: "http://localhost:8000/products/1",
        type: 'GET',
        success: function (res) {
            console.log('success!!');
            alert(res);
        }
    })
})

function check_sort_param(sortParam){
    if (sortParam ===  '<p>Price &#129043</p>'){ // Price down
        return '-price'
    }
    else if (sortParam === 'Price <p>&#129041</p>') { // Price up
        return 'price'
    }
    else if (sortParam === 'Name <p>&#129043;</p>') { // Name down
        return '-name'
    }
    else if (sortParam === 'Name <p>&#129041</p>') { // Name up
        return 'name'
    }
    else {
        return 'price'
    }

}







