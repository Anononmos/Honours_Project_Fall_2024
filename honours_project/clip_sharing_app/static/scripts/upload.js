const ERR_COLOUR = '#C4462D'
const BORDER_COLOUR = '#C2C2C2'

const TIME_LIMIT = 60
const SIZE_LIMIT = 50

// Displays error message

const display_error = (message) => {
    $('.outer').css('border-color', ERR_COLOUR)
    $('.error>span').text(message)
    $('.error').show()
}

// Gets duration of video file

const load_video = (file) => new Promise( 
    (resolve, reject) => {
        let video = document.createElement('video')

        try {
            video.preload = 'metadata'

            video.onloadedmetadata = () => {
                window.URL.revokeObjectURL(video.src)

                resolve(video)
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

// Hide error message upon page load

$(document).ready(() => {
    $('.error').hide()
})

$('input[type="file"]').on('change', async event => {
    const file = event.target.files[0]
    const filename = file.name 
    const filesize = file.size / (1024 * 1024) // Size in MB

    $('.error').hide()
    $('.outer').css('border-color', BORDER_COLOUR)
    $('label>span').text(filename)

    try {
        var video = await load_video(event.currentTarget.files[0])
        
    } catch (error) {
        display_error(error.message)

        return
    }

    if (video.duration > TIME_LIMIT) {
        display_error(`The upload's duration is over ${TIME_LIMIT} seconds.`)

        return
    }

    if (filesize > SIZE_LIMIT) {
        display_error(`The upload is over ${SIZE_LIMIT} MB in size.`)

        return
    }

    $('input[type="submit"]').show()
})