// Get script data
const data = document.currentScript.dataset;
// Get like button to change class
let like_button = $('#like-button');
// Set sending post request on `like_button` click
$(document).on(
  'click',
  '#like-button',
  function(event) {
    // Send ajax post request
    $.ajax(
      {
        type: 'POST',
        url: data.url,
        data: {
          'csrfmiddlewaretoken': data.csrf,
        },
        dataType: 'json',
        success: function(response){
          // If like is set: color like button by `liked` class+
          if (response["is_liked"]){
            like_button.addClass('liked');
          }
          else {
            like_button.removeClass('liked')
          }
        },
      }
    );
  }
)
