document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/v1/posts')
        .then(res => res.json())
        .then(posts => {
            const list = document.getElementById('post-list');
            const noPostsMessage = document.getElementById('no-posts-message');

            // 메시지 보여주기
            if (!posts.length) {
                noPostsMessage.style.display = 'block';  
                return;
            }

            posts.forEach(post => {
                const li = document.createElement('li');
                
                const link = document.createElement('a');
                link.href = `/${post.id}`;
                link.textContent = post.title;

                li.appendChild(link);
                li.append(`: ${post.content}`);
                list.appendChild(li);
            });
        })
        .catch(err => {
            console.error(err);
        });
});
