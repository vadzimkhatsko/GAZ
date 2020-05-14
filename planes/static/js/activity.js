$("document").ready(function() {
    $('document.body').on('keyup mouseup', function () {
        $.ajax({"url":"/planning/add_click/"
        })
        console.log("hello")
    })
    console.log("hello")
});