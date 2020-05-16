$("document").ready(function() {
    $('body').on('keyup mouseup', function () {
        $.ajax({"url":"/plane/add_click/"
        })
        console.log("click")
    })
});