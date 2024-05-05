let page = 1;

const writeButton = document.getElementById("reply-write");
const ul = document.querySelector("#replies-wrap ul");
const moreButton = document.getElementById("more-replies");

replyService.getList(post_id, page + 1).then((replies) => {
    if (replies.length !== 0){
        moreButton.style.display = "flex";
    }
});

const showList = (replies) => {
    let text = ``;
    replies.forEach((reply) => {
        text += `
            <li>
                <div>
                    <section class="content-container">
                        <div class="profile">
                            <div><img src="/upload/${reply.member_path}" width="15px"></div>
                            <h6 class="writer">${reply.member_name}</h6>
                        </div>
                        <h4 class="title">${reply.reply_content}</h4>
                        <section class="reply-update-wrap" id="update-form${reply.id}">
                            <textarea id="" cols="30" rows="1" placeholder="내 댓글">${reply.reply_content}</textarea>
                            <div class="button-wrap">
                                <button class="update-done ${reply.id}">작성완료</button>
                                <button class="calcel ${reply.id}">취소</button>
                            </div>
                        </section>
                        <h6 clss="post-info">
                            <span class="date">${timeForToday(reply.created_date)}</span>
        `;
        if(reply.member_id === Number(memberId)) {
            text += `
                            <span class="date">·</span>
                            <span class="update ${reply.id}">수정</span>
                            <span class="date">·</span>
                            <span class="delete ${reply.id}">삭제</span>
            `
        }
        text += `
                        </h6>
                    </section>
                </div>
            </li>
        `;
    });
    return text;
}

moreButton.addEventListener("click", (e) => {
    replyService.getList(post_id, ++page, showList).then((text) => {
        ul.innerHTML += text;
    });

    replyService.getList(post_id, page + 1).then((replies) => {
    if (replies.length === 0){
        moreButton.style.display = "none";
    }
});

});

writeButton.addEventListener("click", async (e) => {
    const replyContent = document.getElementById("reply-content");
    await replyService.write({
        reply_content: replyContent.value,
        post_id: post_id
    });
    replyContent.value = "";

    page = 1
    const text = await replyService.getList(post_id, page, showList);
    ul.innerHTML = text;

    const replies = await replyService.getList(post_id, page + 1);
    if (replies.length !== 0){
        moreButton.style.display = "flex";
    }
});

replyService.getList(post_id, page, showList).then((text) => {
    ul.innerHTML = text;
});

// ul 태그의 자식 태그까지 이벤트가 위임된다.
ul.addEventListener("click", async (e) => {
    if(e.target.classList[0] === 'update'){
        const replyId = e.target.classList[1]
        const updateForm = document.getElementById(`update-form${replyId}`)

        updateForm.style.display = "block";
        updateForm.previousElementSibling.style.display = "none";

    }else if(e.target.classList[0] === 'calcel'){
        const replyId = e.target.classList[1]
        const updateForm = document.getElementById(`update-form${replyId}`)
        updateForm.style.display = "none";
        updateForm.previousElementSibling.style.display = "block";

    }else if(e.target.classList[0] === 'update-done'){
        const replyId = e.target.classList[1]
        const replyContent = document.querySelector(`#update-form${replyId} textarea`);
        await replyService.update({replyId: replyId, replyContent: replyContent.value})
        page = 1
        const text = await replyService.getList(post_id, page, showList);
        ul.innerHTML = text;
        const replies = await replyService.getList(post_id, page + 1);
        if (replies.length !== 0){
            moreButton.style.display = "flex";
        }

    }else if(e.target.classList[0] === 'delete'){
        const replyId = e.target.classList[1];
        await replyService.remove(replyId);
        page = 1
        const text = await replyService.getList(post_id, page, showList);
        ul.innerHTML = text;

        const replies = await replyService.getList(post_id, page + 1);
        if (replies.length !== 0){
            moreButton.style.display = "flex";
        }
    }
});











function timeForToday(datetime) {
    const today = new Date();
    const date = new Date(datetime);

    let gap = Math.floor((today.getTime() - date.getTime()) / 1000 / 60);

    if (gap < 1) {
        return "방금 전";
    }

    if (gap < 60) {
        return `${gap}분 전`;
    }

    gap = Math.floor(gap / 60);

    if (gap < 24) {
        return `${gap}시간 전`;
    }

    gap = Math.floor(gap / 24);

    if (gap < 31) {
        return `${gap}일 전`;
    }

    gap = Math.floor(gap / 31);

    if (gap < 12) {
        return `${gap}개월 전`;
    }

    gap = Math.floor(gap / 12);

    return `${gap}년 전`;
}












