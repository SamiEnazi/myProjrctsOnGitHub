console.log('hi');

function addgenre() {
    $('#genreslist ').change(function() {
        console.log($('#genreslist').val());
    });
}