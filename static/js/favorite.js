$(document).ready(function () {
  listing();
});
function listing() {
  $.ajax({
    type: "GET",
    url: "/api/videos/favorite",
    data: {},
    success: function (response) {
      const row = response.favorites;
      row.map((data) => {
        $.ajax({
          type: "GET",
          url: "/api/videos",
          data: {},
          success: function (response) {
            const rows = response.list;
            rows.map((list) => {
              const video = list.video_id;
              if (video === data) {
                let title = list.title;
                let img = list.image;
                let video_id = list.video_id;
                let desc = list.desc;
                let bu_name = list.bu_name;
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
            });
          },
        });
      });
    },
  });
}
