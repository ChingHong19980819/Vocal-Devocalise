const obs = new OBSWebSocket();

obs.connect('ws://localhost:4455', 'OVKTgmaQbm6JkK83').then((info) => {
    console.log(info)
    startRecording();
    getSceneName()
    setTimeout(() => {
        changeScene('Hello 2')
    }, 5000);
    setTimeout(() => {
        changeScene('Hello')
    }, 10000);
    setTimeout(() => {
        stopRecording();
    }, 15000);


    obs.call('GetSceneTransitionList').then((data) => {
        console.log(data)
    }).catch(error => {
        console.error('Error starting recording:', error);
    });
}, () => {
    console.error('Error Connecting')
})



function startRecording() {
    obs.call('StartRecord').then((data) => {
        console.log(data)
        console.log(data)
    }).catch(error => {
        console.error('Error starting recording:', error);
    });
}

function getSceneName() {
    obs.call('GetSceneList').then((data) => {
        console.log(data)
    }).catch(error => {
        console.error('Error starting recording:', error);
    });
}

function changeScene(sceneName) {
    obs.call('SetCurrentProgramScene', { sceneName: sceneName }).then((data) => {
        console.log(data)
    }).catch(error => {
        console.error('Error starting recording:', error);
    });
}

// Stop recording
function stopRecording() {
    obs.call('StopRecord').then((data) => {
        console.log(data)
    }).catch(error => {
        console.error('Error stopping recording:', error);
    });
}


eel.get_downloaded_song()
eel.get_devocalised_song()
eel.get_downloading_song()


eel.expose(getCompletedSong);
document.getElementById('env').innerText = `NODE_ENV: ${process.env.GH_TOKEN}`;


function getCompletedSong(arr) {
    var parent = document.getElementById('song-container');

    for (let s = 0; s < arr.length; s++) {
        var newChild = `<div> ` + arr[s] + ` </div>`;
        parent.insertAdjacentHTML('beforeend', newChild);
    }

}

eel.expose(getDownloadingSong);
function getDownloadingSong(arr) {
    var parent = document.getElementById('song-container');

    for (let s = 0; s < arr.length; s++) {
        var newChild = `<div> ` + arr[s] + ` </div>`;
        parent.insertAdjacentHTML('beforeend', newChild);
    }

}

eel.expose(getDownloadedSong);
function getDownloadedSong(arr) {
    var parent = document.getElementById('song-container');

    for (let s = 0; s < arr.length; s++) {
        var newChild = `<div> ` + arr[s] + ` </div>`;
        parent.insertAdjacentHTML('beforeend', newChild);
    }
}

eel.expose(getDownloadProgress);
function getDownloadProgress(song, progress) {
    console.log(song, progress)
}

eel.expose(errorMessage);
function errorMessage(message) {
    console.log(message)
}

function startDownload() {
    const inputElement = document.getElementById('direct-download-url');

    // Get the value of the input element
    const inputValue = inputElement.value;
    inputElement.value = ''
    // Display the input value in the console

    eel.startNewDownload(inputValue)
}