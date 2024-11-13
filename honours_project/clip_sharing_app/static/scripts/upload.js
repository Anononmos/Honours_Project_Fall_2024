/**
 * Displays the message as a popup error.
 * @param {string} message 
 */
const display_error = (message) => {
    const ERR_COLOUR = '#C4462D'

    $('input[type="submit"]').hide()
    $('.outer').css('border-color', ERR_COLOUR)
    $('.error>span').text(message)
    $('.error').show()
}


/**
 * Hides the popup error.
 */
const hide_error = () => {
    const BORDER_COLOUR = '#C2C2C2'

    $('.error').hide()
    $('.outer').css('border-color', BORDER_COLOUR)
}


const show_filename = filename => {
    $('label>span').text(filename)
}

/**
 * Gets duration of video file. Asynchronous because the input file's metadata has to be loaded into an HTML video element.
 * @param {File} file 
 * @returns {Promise<number>} The video's duration.
 * @throws {Error} When file fails to load inside a HTML video element.
 */
const get_duration = (file) => new Promise( 
    (resolve, reject) => {
        let video = document.createElement('video')

        try {
            video.preload = 'metadata'

            video.onloadedmetadata = () => {
                window.URL.revokeObjectURL(video.src)

                resolve(video.duration)
            }

            video.onerror = () => {
                if (video.src) {
                    window.URL.revokeObjectURL(video.src)
                }

                reject('Invalid video. Please select a video file.')
            }

            video.src = window.URL.createObjectURL(file)
        }
        catch (err) {
            if (video.src) {
                window.URL.revokeObjectURL(video.src)
            }

            reject(err)
        }
    }
)


/**
 * Returns true if filesize is less than or equal to 50 MB.
 * @param {File} file 
 * @returns {boolean}
 */
const validate_filesize = file => {
    const LIMIT = 50    // Size in MB
    const filesize = file.size / (1024 * 1024)  // Size in MB

    return Math.floor(filesize) <= LIMIT
}


/**
 * Returns true if video's duration is less than or equal to 60 seconds.
 * @param {File} file 
 * @returns {boolean}
 * @throws Error if get_duration throws error.
 */
const validate_duration = async file => {
    const LIMIT = 60    // In seconds

    try {
        const duration = await get_duration(file)

        return Math.floor(duration) <= LIMIT
    }
    catch (error) {
        throw error
    }
}


// Hide error popup on page load.
$(document).ready(hide_error)

$('input[type="file"]').on('change', async event => {
    const SIZE_LIMIT = 50   // In MB
    const DURATION_LIMIT = 60   // In seconds

    const file = event.currentTarget.files[0]
    const filename = file.name 

    hide_error()
    show_filename(filename)

    if (!validate_filesize(file)) {
        display_error(`The upload is over ${SIZE_LIMIT} MB in size.`)

        return
    }

    try {
        if (! await validate_duration(file)) {
            display_error(`The upload is over ${DURATION_LIMIT} seconds in length.`)

            return
        }   
        
    } catch (error) {
        display_error(`The upload cannot have its duration accessed.`)

        return
    }

    $('input[type="submit"]').show()
})