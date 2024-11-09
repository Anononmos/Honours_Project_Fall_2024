/**
 * Displays error message as a popup.
 * @param {string} message 
 */
const display_error = message => {
    const ERR_COLOUR = '#C4462D'

    $('video').hide()
    $('.outer').css('border-color', ERR_COLOUR)
    $('.error>span').text(message)
    $('.error').show()
}


/**
 * Hides the error popup.
 */
const hide_error = () => {
    const BORDER_COLOUR = '#C2C2C2'

    $('video').show()
    $('.outer').css('border-color', BORDER_COLOUR)
    $('.error').hide()
}


/**
 * Gets the HTML media url from the DOM and removes the data attribute.
 * @returns {string} Extracted media url and removes the url attribute from the HTML DOM and the data cache.
 */
const extract_media_url = () => {
    const url = $('#client').data('url')

    $('#client').removeAttr('data-url')
    $('#client').removeData('url')

    return url
}


/**
 * Requests video file contents from a media url. Converts file contents to blob.
 * @param {string} url 
 * @returns {Blob | undefined} Converts file contents into blob. Returns nothing if error is thrown.
 * @throws Error if HTTP request to media url fails.
 */
const fetch_video = async url => {
    try {
        const response = await fetch(url)
        
        if (!response.ok) {
            throw new Error(`Video could not be retrieved.`)
        }

        const blob = await response.blob()
        
        return blob

    }
    catch (error) {
        display_error(error.message) 

        return
    }
}


$(document).ready( async () => {
    // Gets file url from server which is then hidden from being viewed within the HTML
    // Fetch the file to convert into a blob url
    // Load the blob url

    hide_error()

    const url = extract_media_url()
    const blob = await fetch_video(url)

    try {
        const src = URL.createObjectURL(blob)

        $('video').attr('src', src)
    }
    catch (error) {
        display_error('Failed to load the requested video.')

        console.log(error)
    }
} )

$('video').on('loadedmetadata', event => {
    hide_error()

    URL.revokeObjectURL( $('video').attr('src') )
})

$('video').on('error', event => {
    const message = 'The video failed to load.'

    display_error(message)
})