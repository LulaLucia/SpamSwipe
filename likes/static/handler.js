// https://stackoverflow.com/questions/23508221/vanilla-javascript-event-delegation

function incrLikesHandler(event) {
    const target = event.target;
    console.log('target', target);
    const button = target.closest('[data-item]');
    console.log('button', button);
    if(button) {
        const item = button.getAttribute('data-item');
        console.log('button item', item);
        incrLikes(item,
                  (val) => {
                      console.log('server returned this data', val);
                      const updatedCount = val.likes;
                      console.log('updatedCount', updatedCount);
                      // find the closest ancestor that is an LI
                      const li = target.closest('li');
                      // find the descendant of the LI that has a class of "likes"
                      const span = li.querySelector('.likes');
                      // update the text of that span
                      span.textContent = updatedCount;
                  });
    }
}
