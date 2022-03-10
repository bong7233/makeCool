const exampleModal = document.getElementById("exampleModal");
let videoid;

// Modal 창 구현
exampleModal.addEventListener("show.bs.modal", (event) => {
  const button = event.relatedTarget;

  const title = button.getAttribute("data-bs-title");
  const desc = button.getAttribute("data-bs-desc");
  const videoID = button.getAttribute("data-bs-videoID");
  const modalTitle = exampleModal.querySelector(".modal-title");
  const modalDesc = exampleModal.querySelector(".modal-desc");
  const modalVideo = exampleModal.querySelector(".modal-video");
  videoid = videoID;
  getLike();
  modalVideo.src = `https://www.youtube.com/embed/${videoID}?autoplay=1&mute=1&loop=1&playlist=${videoID}`;
  modalTitle.textContent = title;
  modalDesc.textContent = desc;
});

// modal 창 닫을때 영상 종료
exampleModal.addEventListener("hidden.bs.modal", () => {
  const modalVideo = exampleModal.querySelector(".modal-video");
  modalVideo.src = "";
});
