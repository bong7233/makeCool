const genres = document.querySelectorAll(".listing_genres");

genres.forEach(function (genre) {
  genre.addEventListener("click", clickGenreBtn);
  genre.addEventListener("click", listing);
});

function clickGenreBtn(e) {
  $("#thumbnail-box").empty();
  let genre = e.currentTarget.getAttribute("data-genre");
  genreBucket = genre;
  console.log(genreBucket);
  $.ajax({
    type: "POST",
    url: "/api/videos/buName",
    data: { buName_give: genreBucket },
    success: function (response) {
      console.log(response);
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
}

function listing() {
  $.ajax({
    type: "GET",
    url: "/api/videos",
    data: {},
    success: function (response) {
      console.log(response);
    },
  });
}

/*************************
 * 로그아웃
 **************************/
$(document).ready(function () {
  $("#logout").click(function () {
    $.removeCookie("mytoken");

    alert("로그아웃!");

    window.location.href = "/";
  });
});
