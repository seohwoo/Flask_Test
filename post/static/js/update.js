document.addEventListener('DOMContentLoaded', () => {
    const postId = window.location.pathname.split('/').pop();
    const form = document.getElementById('update-form');
    const errorBox = document.getElementById('error-message');

    fetch(`/api/v1/posts/${postId}`)
        .then(res => { return res.json();})
        .then(post => {
            document.title = `수정 ${post.id}`;
            document.getElementById('title').value = post.title;
            document.getElementById('content').textContent = post.content;
        })
        .catch(err => {
            console.error(err);
        });

        form.addEventListener('submit', function (e) {
            e.preventDefault(); // 새로고침 방지
    
            // 공백 제거
            const title = form.title.value.trim();
            const content = form.content.value.trim();
    
            if (!title || !content) {
                errorBox.textContent = '제목과 내용을 모두 입력하세요.';
                return;
            }
    
            fetch(`/api/v1/posts/${postId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title, content }),
            })
            .then(res => {
                if (!res.ok) throw new Error();
                return res.json();
            })
            .then(() => {
                window.location.href = `/${postId}`;  // 작성 성공 → 목록으로 이동
            })
            .catch(err => {
                console.error(err);
                errorBox.textContent = '글 수정 중 오류가 발생했습니다.';
            });
        });
});