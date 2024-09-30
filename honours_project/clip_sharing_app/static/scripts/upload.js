const ERR_COLOUR = '#C4462D'
const BORDER_COLOUR = '#C2C2C2'

$(() => {
    $('.error').hide()
})

const load_video = file => new Promise( (resolve, reject) => {
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
})

$('input[type="file"]').on('change', event => {
    const file = event.target.files[0]
    const filename = file.name 
    const filesize = file.size / (1024 * 1024) // Size in MB

    $('.error').hide()
    $('.outer').css('border-color', BORDER_COLOUR)
    $('label>span').text(filename)

    $('input[type="submit"]').show()
})