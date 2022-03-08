$(document).ready(function () {
  listing_neck();
});

function listing_neck() {
  $("#thumbnail-box").empty();
  $(".listingBox_neck").css("opacity", "1");
  $(".listingBox_waist").css("opacity", "0.6");
  $(".listingBox_wrist").css("opacity", "0.6");
  $(".listingBox_lowerBody").css("opacity", "0.6");
  $.ajax({
    type: "GET",
    url: "/api/main/neck",
    data: {},
    success: function (response) {
      console.log(response);
      let rows = response.main_list;
      for (let i = 0; i < 15; i++) {
        let title = rows[i].title;
        let img = rows[i].image;
        let video_id = rows[i].video_id;
        let desc = rows[i].desc;
        let temp_html = `<button
                            type="button"
                            class="thumbnail"
                            data-bs-toggle="modal"
                            data-bs-target="#exampleModal"
                            data-bs-title="${title}"
                            data-bs-desc="${desc}"
                            data-bs-videoID="${video_id}"
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

function listing_waist() {
  $("#thumbnail-box").empty();
  $(".listingBox_neck").css("opacity", "0.6");
  $(".listingBox_waist").css("opacity", "1");
  $(".listingBox_wrist").css("opacity", "0.6");
  $(".listingBox_lowerBody").css("opacity", "0.6");
  $.ajax({
    type: "GET",
    url: "/api/main/waist",
    data: {},
    success: function (response) {
      console.log(response);
      let rows = response.main_list;
      for (let i = 0; i < 15; i++) {
        let title = rows[i].title;
        let img = rows[i].image;
        let video_id = rows[i].video_id;
        let desc = rows[i].desc;
        let temp_html = `<button
                            type="button"
                            class="thumbnail"
                            data-bs-toggle="modal"
                            data-bs-target="#exampleModal"
                            data-bs-title="${title}"
                            data-bs-desc="${desc}"
                            data-bs-videoID="${video_id}"
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

function listing_wrist() {
  $("#thumbnail-box").empty();
  $(".listingBox_neck").css("opacity", "0.6");
  $(".listingBox_waist").css("opacity", "0.6");
  $(".listingBox_wrist").css("opacity", "1");
  $(".listingBox_lowerBody").css("opacity", "0.6");
  $.ajax({
    type: "GET",
    url: "/api/main/wrist",
    data: {},
    success: function (response) {
      console.log(response);
      let rows = response.main_list;
      for (let i = 0; i < 15; i++) {
        let title = rows[i].title;
        let img = rows[i].image;
        let video_id = rows[i].video_id;
        let desc = rows[i].desc;
        let temp_html = `<button
                            type="button"
                            class="thumbnail"
                            data-bs-toggle="modal"
                            data-bs-target="#exampleModal"
                            data-bs-title="${title}"
                            data-bs-desc="${desc}"
                            data-bs-videoID="${video_id}"
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

function listing_lowerBody() {
  $("#thumbnail-box").empty();
  $(".listingBox_neck").css("opacity", "0.6");
  $(".listingBox_waist").css("opacity", "0.6");
  $(".listingBox_wrist").css("opacity", "0.6");
  $(".listingBox_lowerBody").css("opacity", "1");
  $.ajax({
    type: "GET",
    url: "/api/main/lowerBody",
    data: {},
    success: function (response) {
      let rows = response.main_list;
      for (let i = 0; i < 15; i++) {
        let title = rows[i].title;
        let img = rows[i].image;
        let video_id = rows[i].video_id;
        let desc = rows[i].desc;
        let temp_html = `<button
                            type="button"
                            class="thumbnail"
                            data-bs-toggle="modal"
                            data-bs-target="#exampleModal"
                            data-bs-title="${title}"
                            data-bs-desc="${desc}"
                            data-bs-videoID="${video_id}"
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