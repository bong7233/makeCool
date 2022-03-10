// 좋아요 여부 확인
const isliked = () => {
  let n = document.getElementById("heart");

  if (user_info.like.includes(videoid)) {
    n.setAttribute("class", "fas fa-heart");
  } else {
    n.setAttribute("class", "far fa-heart");
  }
};

// 랜덤토큰 생성
let rand = () => {
  return Math.random().toString(36).substr(2); // remove `0.`
};
let token = () => {
  return rand() + rand(); // to make it longer
};

// 코멘트 작성 창 보여주기
const writeComment = () => {
  let display = document.getElementById("comment-box");
  if (display.style.display == "") {
    display.style.display = "block";
  } else {
    display.style.display = "";
  }
};

// 코멘트 작성
const postComment = () => {
  $.ajax({
    type: "POST",
    url: `/api/post_comment`,
    data: {
      id_give: user_info.id,
      user_give: user_info.name,
      comment_give: $("textarea#msg").val(),
      comment_id_give: token(),
      video_id_give: videoid,
    },
    success: () => {
      $("textarea#msg").val("");
      getComment();
    },
  });
};

// 함수 중복호출 방지
let isRun = false;

// 댓글 가져오기
const getComment = () => {
  if (isRun == true) {
    return;
  }
  isRun = true;
  $("#comment-list").empty();
  $.ajax({
    type: "GET",
    url: `/api/get_comment?video_id_give=${videoid}`,
    data: {},
    success: (response) => {
      comment_list = response.comment;
      for (let i = 0; i < comment_list.length; i++) {
        let comment = comment_list[i];
        let user = comment.name;
        let com = comment["comment"];
        let com_id = comment.comment_id;
        html_temp = `<div class="comm-one" com_id =${com_id}>
                      <span>${user}</span>
                      <p>${com}</p>
                      <i  onclick= 'deleteComment(this)' class="fas fa-trash-alt trash-icon" id='trash-icon'></i>
                      </div>`;
        $("#comment-list").append(html_temp);
        isRun = false;
      }
    },
  });
};

// 좋아요 여부 확인
const getLike = () => {
  $.ajax({
    type: "GET",
    url: `/api/get_like?video_id_give=${videoid}&user_id_give=${user_info["id"]}`,
    data: {},
    success: (response) => {
      let num = document.getElementById("heart-count");
      let heart = document.getElementById("heart");
      num.innerHTML = response.count;
      response.isliked == true
        ? heart.setAttribute("class", "fas fa-heart")
        : heart.setAttribute("class", "far fa-heart");
    },
  });
};

// 댓글 삭제
const deleteComment = (event) => {
  let node = event;
  let parent = node.parentElement;
  let com_id = parent.getAttribute("com_id");

  $.ajax({
    type: "POST",
    url: `/api/delete_comment`,
    data: {
      comment_id_give: com_id,
      user_name_give: user_info.name,
      video_id_give: videoid,
    },
    success: (response) => {
      alert(response.msg);
      getComment();
    },
  });
};

// 좋아요 추가
const addLike = () => {
  $.ajax({
    type: "POST",
    url: `/api/add_like`,
    data: {
      id_give: user_info.id,
      video_id_give: videoid,
    },
    success: (response) => {
      let num = document.getElementById("heart-count");
      let count = response["count"];
      num.innerHTML = "" + count;
    },
  });
};

// 좋아요 취소
const undoLike = () => {
  $.ajax({
    type: "POST",
    url: `/api/undo_like`,
    data: {
      id_give: user_info["id"],
      video_id_give: videoid,
    },
    success: (response) => {
      let num = document.getElementById("heart-count");
      let count = response["count"];
      num.innerHTML = "" + count;
    },
  });
};

// 좋아요 하트 토글 설정
const heartColor = (event) => {
  let node = event;

  //좋아요 눌린 경우
  if (node.getAttribute("class") == "fas fa-heart") {
    node.setAttribute("class", "far fa-heart");
    undoLike();
    //좋아요 눌리지 않은 경우
  } else {
    node.setAttribute("class", "fas fa-heart");
    addLike();
  }
};
