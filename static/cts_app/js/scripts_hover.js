$(document).ready(function () {
    
    //Highlights collasible header on output pages during
    //mouseover event
    $('.collapsible').hover(
        function() {
            $(this).data('bgcolor', $(this).css('background-color')).css({
                'background-color': '#9AB2CB',
                'cursor': 'pointer'
            });
        },
        function() {
            $(this).css('background-color', $(this).data('bgcolor'));
        }
    );

    if (window.location.href.includes("chemspec/output")) {
        addRefToMeasuredPka();  // adds tooltip of ref to measured pka value    
    }
    
});



// Adds reference info to measured pka in speciation output
function addRefToMeasuredPka() {

    const measuredBullet = $('#pkaValues dd:contains("Measured Values")');
    let run_data = JSON.parse(document.getElementById('run_data').textContent);
    let measuredPkaRef = run_data['measured']['data']['ref'];
    let tooltipHtml = measuredPkaRef + ' <i>(click to copy)</i>';

     $(measuredBullet).qtip({
        content: {
            text: tooltipHtml
        },
        style: {
            classes: 'qtip-light'
        },
        position: {
            my: 'bottom right',
            at: 'center right',
            target: 'mouse'
        },
        events: {
            render: function(event, api) {
                $(measuredBullet).on('click', function() {
                    navigator.clipboard.writeText(measuredPkaRef).then(() => {
                        // alert("Reference copied.");
                    });
                });
            }
        }
    });

}