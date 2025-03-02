
window.addEventListener('load', function(){
    chrome.storage.sync.set({'title': document.title}, function() {
        console.log('Title saved');
    });
})
