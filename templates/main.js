$(function(){
	$(document).bind('keydown', 'ctrl+return', function(){
		$('#submit').click();
	});
	$(document).bind('keydown', 'A', function(){
		$('#fumi').click();
	});
	$(document).bind('keydown', 'S', function(){
		$('#other').click();
	});
	$(document).bind('keydown', 'D', function(){
		$('#aikawa').click();
	});
	$(document).bind('keydown', 'F', function(){
		$('#yui').click();
	});
	$(document).bind('keydown', 'H', function(){
		$('#kei').click();
	});
	$(document).bind('keydown', 'J', function(){
		$('#yukari').click();
	});
	$(document).bind('keydown', 'K', function(){
		$('#yuzuko').click();
	});
	$(document).bind('keydown', 'L', function(){
		$('#okasan').click();
	});
});
