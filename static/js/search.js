function onClientLoad() {
    gapi.client.load('youtube', 'v3', onYouTubeApiLoad);
}
// Called automatically when YouTube API interface is loaded (see line 9).
function onYouTubeApiLoad() {
    gapi.client.setApiKey('AIzaSyCsJxPieXjWm2p5Ba8M187SjbGfq47OCTw');
}

function getRequest(searchTerm) {
    var url = 'https://www.googleapis.com/youtube/v3/search';

    var params = {
        part: 'snippet',
        key: 'AIzaSyCsJxPieXjWm2p5Ba8M187SjbGfq47OCTw',
        q: searchTerm
    };
    console.log(searchTerm);
    $.getJSON(url, params, showResults);
}

function search(query) {
    getRequest(query);
}

function searchByKeyword(str) {
    var keyword;
    if (str.localeCompare("hi") != 0)
        keyword = str;
    else
        keyword = $("#search-video").val().trim()
    console.log(keyword);
    if (keyword.length == 0) return;
    search(keyword);
    // call Youtube API search.list in JS
}
$("#video-info").on("submit", function () {
    event.preventDefault();
    console.log('ho gya');
    searchByKeyword("hi");
});

// $("#user-info").on("submit", function () {
//     event.preventDefault();
//     console.log('ho gya\n');
//     // document.getElementById('response').innerHTML = 'ho gya' ;    
//     searchVideo();
//     searchKeyword();
// });

// function showResults(results) {
//     var html = "";
//     var entries = results.items;
//     console.log(results.items);
//     $.each(entries, function (index, value) {
//         var title = value.snippet.title;
//         var thumbnail = value.snippet.thumbnails.default.url;
//         html += '<p>' + title + '</p>';
//         html += '<img src="' + thumbnail + '">';
//     }); 

//     //$('#response').html(html);
// }
function showResults(results) {
    var entries = results.items;
    console.log(results.items);
    $.each(entries, function (index, value) {
        var vidTitle = value.snippet.title,
            vidId = value.id.videoId,
            vidDescription = value.snippet.description,
            vidImage = value.snippet.thumbnails.medium.url;
        // appendResults(vidTitle, vidId, vidDescription, vidImage);
    })
};

function appendResults(title, ID, description, image) {
    $('<div class="media"><div class="media-left"><a href="https://www.youtube.com/watch?v=' + ID + '" target="_blank"><img class="media-object" src="' + image + '" alt=""></a></div><div class="media-body"><h4 class="media-heading"> ' + title + '</h4><p>' + description + '</p><a href="https://www.youtube.com/watch?v=' + ID + '" class="btn btn-default" target="_blank">Watch Video</a> <p>https://www.youtube.com/watch?v=' + ID + '</p></div>').appendTo(".well");
};

// Triggered by this line: request.execute(onSearchResponse);
function onSearchResponse(response) {
    document.getElementById('response').innerHTML = 'tat';
    var responseString = JSON.stringify(response, '', 2);
    document.getElementById('response').innerHTML = responseString;
}

function copyLink(ID) {
    var copyText = document.getElementById("copylink");
    copyText.value = ID;
}