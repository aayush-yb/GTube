
function showResults(e) { 
	$.each(e, function (e, t) { 
		var a = t.snippet.title, s = t.id.videoId, i = t.snippet.description, n = t.snippet.thumbnails.medium.url; 
		appendResults(a, s, i, n) }) 
} 
function appendResults(e, t, a, s) { 
	$('<div class="media"><div class="media-left"><a href="https://www.youtube.com/watch?v=' + t + '" target="_blank"><img class="media-object" src="' + s + '" alt=""></a></div><div class="media-body"><h4 class="media-heading"> ' + e + "</h4><p>" + a + '</p><a href="https://www.youtube.com/watch?v=' + t + '" class="btn btn-default" target="_blank">Watch Video</a></div></div>').appendTo(".well") 
} 
function getRequest(e) { 
	var t = { part: "snippet", key: "AIzaSyCsJxPieXjWm2p5Ba8M187SjbGfq47OCTw", q: e }; 
	endPoint = "https://www.googleapis.com/youtube/v3/search/", $.getJSON(endPoint, t, function (e) { 
		showResults(e.items), console.log(e.items) 
	}) 
} 
function clearResults() { 
	$(".well .media").fadeOut(), $(".video-search").val("").focus() 
} 
$(function () { 
	$("form").submit(function (e) { 
		e.preventDefault(); 
		console.log("hey there");
		var t = $("#search-keyword").val();
		console.log(t);
		console.log(e);
		//var t = $(".video-search").val(); 
		getRequest(t) 
	}) 
}), $(".search-clear").on("click", clearResults);