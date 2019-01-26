$(document).ready(function() {

    var ram=$('#search-keyword');
    var omshubham=$('#youtube-url');
    var tebriwal=$('#query-search');
    var maa_ka_bharosa=$('#summarise-link');
    $("#user-info").on("submit", function() {
        event.preventDefault();  
        var url1= $(ram).val();
        var url2= $(omshubham).val();
        console.log(url1);         
        searchVideo("hi", "hi", url1, url2);    
        searchKeyword("hi", "hi", url1, url2);        
    });

    $('#summarise-info').on("submit", function() {
        event.preventDefault();
        var url=$(maa_ka_bharosa).val();
        console.log(url);
        // var video = "../static/images/1_1.mp4";
        // $("#embedded-video").attr("src", video);
        $.ajax({
            url: "/sum",
            type: "POST",
            data: {
                "url2": url,
            },
            success: function(response) {
                console.log("done");
                var video = "../static/images/1_1.mp4";
                $("#embedded-video").attr("src", video);
            }
        });
    });

    $("#find-local").on("change", function() {
        console.log(this);
        var keyword= $(ram).val();
        var local_file=$(this).val;
        localVideo(keyword);
    });

    $("#find-photo").on("change", function() {
        //alert("aaaaaaa");
        console.log(this);
        var keyword= $(ram).val();
        var local_file=$(this).val;
        localPhoto(keyword);
    });

    $("#query-info").on("submit", function() {
        event.preventDefault();
        var q=$(tebriwal).val();
        executeQuery(q);
    });

    function onClientLoad() {
        gapi.client.load('youtube', 'v3', onYouTubeApiLoad);
    }
    
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

        $.getJSON(url, params, showResults);
    }
    
    function search(query) {
        getRequest(query);
    }

    function showResults(results) {
        var entries = results.items;
        console.log(results.items);
        $.each(entries, function (index, value) {
            var vidTitle = value.snippet.title,
                vidId = value.id.videoId,
                vidDescription = value.snippet.description,
                vidImage = value.snippet.thumbnails.medium.url;
            appendResults(vidTitle, vidId, vidDescription, vidImage);
        })
    };

    function appendResults(title, ID, description, image) {
        $('<div class="media"><div class="media-left"><a href="https://www.youtube.com/watch?v=' + ID + '" target="_blank"><img class="media-object" src="' + image + '" alt=""></a><br><br></div><div class="media-body"><h4 class="media-heading"> ' + title + '</h4><p>' + description + '</p><a href="https://www.youtube.com/watch?v=' + ID + '" class="btn btn-default" target="_blank">Watch Video</a> <p>https://www.youtube.com/watch?v=' + ID + '</p></div>').appendTo(".well");
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
    function searchByKeyword(str) {
        var keyword;
        if (str.localeCompare("hi") != 0)
            keyword = str;
        else
            keyword = $("#search-video").val().trim()
        console.log(keyword);
        if (keyword.length == 0) return;
        search(keyword);
    }


    function executeQuery(query) {
        if(query.length == 0)   return;
        var copyquery = query;
        query = query.split(" ");        
        var summarize = "summarize", findWord = "find", search = "search"; 
        console.log(query[0]);
        if(query[0].localeCompare(summarize) == 0) {

        } else if(query[0].localeCompare(findWord) == 0) {
            searchVideo(query[1], query[3]);
            searchKeyword(query[1], query[3]);
        } else if(query[0].localeCompare(search) == 0) {
            event.preventDefault();     
            var len = copyquery.length;
            copyquery = copyquery.substr(6, len-6);
            console.log('ho gya'); 
            searchByKeyword(copyquery);
        } else {
            document.getElementById("query-search").innerHTML = "Error!! Type properly";
        }
    }

    function searchVideo(keyword1, url1, key, ur) {
        var url;
        if(url1.localeCompare("hi") == 0)
            url = ur;
        else
            url = url1;
        if(url.length == 0) return;

        if(url.search("youtube") >= 1){
            if(url.search('embed') === -1){
                url = "https://www.youtube.com/embed/" + url.split("watch?v=")[1];
            }
        }        

        $("#embedded-video").attr("src", url);     
    }

    function searchKeyword(keyword1, url1, key, ur){
        var keyword;
        if(keyword1.localeCompare("hi") == 0)
            keyword = key;
        else
            keyword = keyword1;
        if(keyword.length == 0) return;
        var results = $("#results");
        results.html(""); // Delete content in table
        
        var url = $("#embedded-video").attr("src");
        $.ajax({
            url: "/search_keyword",
            type: "POST",
            data: {
                "url": url,
                "keyword": keyword
            },
            success: function(data){                          
                var data_size = Object.keys(data).length;                

                var output = "";
                
                $.each(data, function(index, value){   
                    var key = Object.keys(value)[0];                                     
                    output += "<button type='button' class='btn btn-danger timestamp' value='" + value[key] + "'>" + '<i class="fa fa-play" aria-hidden="true"></i>&nbsp' +  '<span style="color:black;">' + key + "</span>" + "</button>&nbsp";
                    
                    if((parseInt(index) + 1) % 5 == 0){
                        output += "<br>";
                    }
                });

                results.html(output);
                $(".timestamp").click(function(){      
                    var value = $(this).attr("value");                                                  
                    var new_url = url + "?start="+ parseInt(value)+"&autoplay=1&mute=1" ;
                   $("#embedded-video").attr("src", new_url);
                });
            }
        });
    }

    function localVideo(keyword) {
        //alert(local_file);
        // $.ajax({
        //     url: "/video_to_text.py",
        //     success: function(response) {
        //         console.log("done");
        //     },
        //     error: function(request, status, error) {
        //         console.log("Error: " + error);
        //     }
        // });
        $("#embedded-video").attr("src", "../static/images/videoplayback.mp4");
        var url = $("#embedded-video").attr("src");
        var results = $("#results");
        //var keyword = "census";
        $.ajax({
            url: "/search_keyword_locally",
            type: "POST",
            data: {
                "url": url,
                "keyword": keyword
            },
            success: function(data){                          
                var data_size = Object.keys(data).length;                

                var output = "";
                
                $.each(data, function(index, value){   
                    var key = Object.keys(value)[0];                                     
                    output += "<button type='button' class='btn btn-danger timestamp' value='" + value[key] + "'>" + '<i class="fa fa-play" aria-hidden="true"></i>&nbsp' +  '<span style="color:black;">' + key + "</span>" + "</button>&nbsp";
                    console.log(value[key]);
                    console.log(key);
                    if((parseInt(index) + 1) % 5 == 0){
                        output += "<br>";
                    }
                });

                results.html(output);
                var url1 = "../static/images/videoplayback1.mp4";
                $(".timestamp").click(function(){      
                    var temp = url;
                    url = url1;
                    url1 = temp;
                    var value = $(this).attr("value");                                                  
                    var new_url =  url + "#t="+ parseInt(value);
                    console.log(new_url);
                    $("#embedded-video").attr("src", new_url);
                    //$("#embedded-video").attr("src", "../static/images/video.mp4#t=10");
                });
            }
        });
    }

    function localPhoto(keyword) {
        //alert(local_file);
        // $.ajax({
        //     url: "/video_to_text.py",
        //     success: function(response) {
        //         console.log("done");
        //     },
        //     error: function(request, status, error) {
        //         console.log("Error: " + error);
        //     }
        // });
        if(keyword[0] == 's')
            $("#embedded-video").attr("src", "../static/images/video2.mp4");
        if(keyword[0] == 't')
            $("#embedded-video").attr("src", "../static/images/video_text.mp4");
        if(keyword[0] == 'f')
            $("#embedded-video").attr("src", "../static/images/videofast.mp4");
        var url = $("#embedded-video").attr("src");
        var results = $("#results");
        // var keyword = "person";
        $.ajax({
            url: "/search_photo_locally",
            type: "POST",
            data: {
                "url": url,
                "keyword": keyword
            },
            success: function(data){                          
                var data_size = Object.keys(data).length;                

                var output = "";
                
                $.each(data, function(index, value){   
                    var key = Object.keys(value)[0];                                     
                    output += "<button type='button' class='btn btn-danger timestamp' value='" + value[key] + "'>" + '<i class="fa fa-play" aria-hidden="true"></i>&nbsp' +  '<span style="color:black;">' + key + "</span>" + "</button>&nbsp";
                    console.log(value[key]);
                    console.log(key);
                    if((parseInt(index) + 1) % 5 == 0){
                        output += "<br>";
                    }
                });

                results.html(output);
                var url1 ;
                if(keyword[0] == 's')
                    url1 = "../static/images/video1.mp4";
                if(keyword[0] == 't')
                    url1 = "../static/images/video_text1.mp4";
                if(keyword[0] == 'f')
                    url1 = "../static/images/videofast1.mp4";
                $(".timestamp").click(function(){      
                    var temp = url;
                    url = url1;
                    url1 = temp;
                    var value = $(this).attr("value");                                                  
                    var new_url =  url + "#t="+ parseInt(value);
                    console.log(new_url);
                    $("#embedded-video").attr("src", new_url);
                    //$("#embedded-video").attr("src", "../static/images/video.mp4#t=10");
                });
            }
        });
    }
});
