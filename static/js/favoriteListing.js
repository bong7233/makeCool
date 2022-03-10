// 시작시 리스트 불러오기
$(document).ready(function () {
  listing();
});

// 리스트 불러오기
const listing = () => {
  $.ajax({
    type: "GET",
    url: "/api/videos/favorite",
    data: {},
    success: (response) => {
      const row = response.favorites;
      console.log(row.length);
      if (row.length === 0) {
        let temp_html = `<div><span>즐겨찾기 정보가 없습니다</span></div>`;
        $("#thumbnail-box").append(temp_html);
      }
      row.map((data) => {
        $.ajax({
          type: "GET",
          url: "/api/videos",
          data: {},
          success: (response) => {
            const rows = response.list;
            rows.map((list) => {
              const video = list.video_id;
              // 즐겨찾기 한 비디오 키값과 데이터베이스의 비디오 키값이 동일한 경우만 리스트 출력
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
                // 리스트에 추가
                $("#thumbnail-box").append(temp_html);
              }
            });
          },
        });
      });
    },
  });
};
