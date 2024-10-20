const ERR_COLOUR = '#C4462D'
const BORDER_COLOUR = '#C2C2C2'

const display_error = message => {
    $('video').hide()
    $('.outer').css('border-color', ERR_COLOUR)
    $('.error>span').text(message)
    $('.error').show()
}


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

    $('.error').hide()

    const url = $('#client').data('url')
    $('#client').removeAttr('data-url')

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
    $('.error').hide()
    $('.outer').css('border-color', BORDER_COLOUR)
    $('video').show()

    URL.revokeObjectURL( $('video').attr('src') )
})

$('video').on('error', event => {
    const message = 'The video failed to load.'

    display_error(message)
})