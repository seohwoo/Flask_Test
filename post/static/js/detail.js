function formatDateTime(isoString) {
    if (!isoString) return '-';
    const date = new Date(isoString);

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

document.addEventListener('DOMContentLoaded', () => {
    const postId = window.location.pathname.split('/').pop();

    fetch(`/api/v1/posts/${postId}`)
        .then(res => { return res.json();})
        .then(post => {
            document.title = `게시글 ${post.id}`;
            document.getElementById('title').textContent = post.title;
            document.getElementById('content').textContent = post.content;
            document.getElementById('created_at').textContent = formatDateTime(post.created_at);
            document.getElementById('updated_at').textContent = formatDateTime(post.updated_at);
            document.getElementById('update-link').href = `/update/${post.id}`;
            
            const deleteLink = document.getElementById('delete-link');
            deleteLink.href = "#";  // 페이지 이동 막기
            deleteLink.addEventListener('click', (e) => {
                e.preventDefault();  // 기본 링크 이동 방지
                const confirmDelete = confirm("정말로 이 게시글을 삭제하시겠습니까?");
                if (!confirmDelete) return;

                fetch(`/api/v1/posts/${post.id}`, {
                    method: 'DELETE'
                })
                .then(res => {
                    if (!res.ok) throw new Error();
                    return res.json();
                })
                .then(() => {
                    window.location.href = '/';  // 메인으로 이동
                })
                .catch(err => {
                    console.error(err);
                });
            });

        })
        .catch(err => {
            console.error(err);
        });
});