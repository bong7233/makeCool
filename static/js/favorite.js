// 좋아요 여부에따라 하트 표시하기
const isliked = () => {
  let n = document.getElementById("heart");

  if (user_info.like.includes(videoid)) {
    n.setAttribute("class", "fas fa-heart");
  } else {
    n.setAttribute("class", "far fa-heart");
  }
};

// 댓글 작성시 랜덤 토큰 생성
let rand = () => {
  return Math.random().toString(36).substr(2); // remove `0.`
};
let token = () => {
  return rand() + rand(); // to make it longer
};

// 하트 표시
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

// 좋아요 제거
const undoLike = () => {
  $.ajax({
    type: "POST",
    url: `/api/undo_like`,
    data: {
      id_give: user_info.id,
      video_id_give: videoid,
    },
    success: (response) => {
      let num = document.getElementById("heart-count");
      let count = response["count"];
      num.innerHTML = "" + count;
      location.reload();
    },
  });
};

// 좋아요 하트 토글 설정
const heartColor = (event) => {
  let node = event;

  //좋아요가 이미 눌려있는경우
  if (node.getAttribute("class") == "fas fa-heart") {
    node.setAttribute("class", "far fa-heart");
    undoLike();
    //좋아요가 안눌려 있는 경우
  } else {
    node.setAttribute("class", "fas fa-heart");
    addLike();
  }
};

// 로그아웃
$(document).ready(() => {
  $("#logout").click(() => {
    $.removeCookie("mytoken");
    alert("안녕히가세요");
    window.location.href = "/";
  });
});
