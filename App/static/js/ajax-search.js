$().ready(function() {
    $("input.food_search").autocomplete({
        source: "/food/ajax",
        minLength: 2,
        open: function() {
            setTimeout(function() {
                $(".ui-autocomplete").css("z-index", 99);
            }, 0);
        }
    });
});
