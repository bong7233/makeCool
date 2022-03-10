const genres = document.querySelectorAll(".listing_genres");

// 부위별 영상 가져오기
const clickGenreBtn = (e) => {
  $("#thumbnail-box").empty();
  $(`.listingBox_neck`).css("border", "2px solid #5280a8");
  $(`.listingBox_waist`).css("border", "2px solid #5280a8");
  $(`.listingBox_wrist`).css("border", "2px solid #5280a8");
  $(`.listingBox_lowerBody`).css("border", "2px solid #5280a8");
  let genre = e.currentTarget.getAttribute("data-genre");
  genreBucket = genre;
  $(`.listingBox_${genreBucket}`).css("border", "2px solid red");
  $.ajax({
    type: "POST",
    url: "/api/videos/buName",
    data: { buName_give: genreBucket },
    success: (response) => {
      let rows = response.list;
      for (let i = 0; i < 15; i++) {
        let title = rows[i].title;
        let img = rows[i].image;
        let video_id = rows[i].video_id;
        let desc = rows[i].desc;
        let bu_name = rows[i].bu_name;
        let temp_html = `<button
                            type="button"
                            class="thumbnail"
                            data-bs-toggle="modal"
                            data-bs-target="#exampleModal"
                            data-bs-title="${title}"
                            data-bs-desc="${desc}"
                            data-bs-videoID="${video_id}"
                            data-bs-buName="${bu_name}"
                          >
                            <div class="col">
                              <div class="card shadow-sm">
                                <img
                                  src="${img}"
                                  width="100%"
                                  height="180px"
                                  title="${title}"
                                  alt="${title}"
                                />
                                <div class="card-body">
                                  <p class="thunmbnail__title card-text">${title}</p>
                                </div>
                              </div>
                            </div>
                          </button>`;
        $("#thumbnail-box").append(temp_html);
      }
    },
  });
};

// 영상 목록 보여주기
const listing = () => {
  $.ajax({
    type: "GET",
    url: "/api/videos",
    data: {},
    success: () => {},
  });
};

genres.forEach((genre) => {
  genre.addEventListener("click", clickGenreBtn);
  genre.addEventListener("click", listing);
});

// 로그아웃
$(document).ready(() => {
  $("#logout").click(() => {
    $.removeCookie("mytoken");
    alert("안녕히가세요");
    window.location.href = "/";
  });
});
