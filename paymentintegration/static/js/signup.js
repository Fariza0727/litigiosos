/*------------------------------
---------- signup.js -----------
------------------------------*/

//Functions
$(function() {
    /*------------------------------
    ---------- Captcha -------------
    ------------------------------*/
    // Add refresh button after field (this can be done in the template as well)
    $('img.captcha').after(
        $('<a href="#void" class="captcha-refresh" style= "text-decoration: none;font-size: 16px;">&nbsp;&nbsp;<i class="fas fa-sync-alt"></i>&nbsp;</a>')
    );
    // Click-handler for the refresh-link
    $('.captcha-refresh').click(function(){
        var $form = $(this).parents('form');
        var url = location.protocol + "//" + window.location.hostname + ":"
                  + location.port + "/captcha/refresh/";
        // Make the AJAX-call
        $.getJSON(url, {}, function(json) {
            $form.find('input[name="captcha_0"]').val(json.key);
            $form.find('img.captcha').attr('src', json.image_url);
        });
        return false;
    });
    /*------------------------------
    ---------- ./Captcha -----------
    ------------------------------*/

    
    /*------------------------------
    --------- Inputs Form ----------
    ------------------------------*/
    $('#id_captcha_1').ready(function(){
        $('#id_captcha_1').addClass('form-control');
    });
    /*------------------------------
    -------- ./Inputs Form ---------
    ------------------------------*/
});