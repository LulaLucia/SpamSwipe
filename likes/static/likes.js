function getLikes(item,callback) {
    const url = `/likes/${item}`;
    fetch(url)
        .then(resp => resp.json())
        .then(callback);
}

var lastItem; // useful for demos and debugging
    
// this function is useful as a callback.
function debug(val) {
    lastItem = val;
    console.log(val);
}

function printLikes(item) {
    getLikes(item, debug);
}

// This is probably the one we would most likely use in real life

function incrLikes(item, callback) {
    const url = `/likes/${item}`;
    fetch(url, {method: 'POST'})
        .then(resp => resp.json())
        .then(callback);
}

function putLikes(item, count, callback) {
    const url = `/likes/${item}`;
    let data = new FormData();
    data.append('item', item);
    data.append('set_likes', count);
    fetch(url, {
        method: 'PUT',
        body: data})
        .then(resp => resp.json())
        .then(callback);
}

