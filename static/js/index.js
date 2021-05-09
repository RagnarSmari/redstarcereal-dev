



// Starting of filter buttons

// Change the value of the dropdownMenu button when
// user clicks something on the menu
$(".dropdown-menu li a").click(function () {
    var selText = $(this).text();
    $('#dropdownMenuButton1').html(selText);
});

$('#dropdownMenuButton1').on('click',function (){
    console.log('im here')
    let buttonValue = $(this).text();
    console.log(buttonValue);
})


$('#dropdownMenuButton1').change(function (){
    console.log('im here')
    let buttonValue = $(this).text();
    console.log(buttonValue);
});








