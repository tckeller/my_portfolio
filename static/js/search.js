function articleSearchFunction() {
    // Get the uppercase version of the search query. We don't want to be case sensitive.
    var input = document.getElementById('articleSearch');
    var input_lower = input.value.toLowerCase();

    var searched_elements = document.getElementsByClassName('searched_element');

    // Loop through all the blog-links.
    for (var i = 0; i < searched_elements.length; i++) {
        var element_name = searched_elements[i].getElementsByClassName('searched_name')[0];
            var textValue = element_name.textContent || element_name.innerText;

            // If the name does not contain the search, remove it.
            if (textValue.toLowerCase().indexOf(input_lower) > -1) {
                searched_elements[i].style.display = "";
            } else {
                searched_elements[i].style.display = "none";
            }
    }
}