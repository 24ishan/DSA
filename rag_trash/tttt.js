const likeButton = [...document.querySelectorAll('button')]
  .find(btn => btn.querySelector('.Hidden')?.textContent.trim() === 'Like');

console.log(likeButton);


likeButton?.click();

(() => {
  if (window.autoLikeRunning) {
    console.log("Already running.");
    return;
  }

  window.autoLikeRunning = true;

  const MIN_DELAY = 1500;
  const MAX_DELAY = 4000;

  const getLikeButton = () =>
    [...document.querySelectorAll("button")]
      .find(btn =>
        btn.querySelector(".Hidden")?.textContent.trim() === "Like"
      );

  const randomDelay = () =>
    Math.floor(
      Math.random() * (MAX_DELAY - MIN_DELAY + 1)
    ) + MIN_DELAY;

  const loop = async () => {
    while (window.autoLikeRunning) {
      const button = getLikeButton();

      if (button) {
        button.click();
        console.log("Clicked Like");
      } else {
        console.log("Like button not found.");
      }

      await new Promise(resolve =>
        setTimeout(resolve, randomDelay())
      );
    }
  };

  window.stopAutoLike = () => {
    window.autoLikeRunning = false;
    console.log("Auto-clicker stopped.");
  };

  console.log("Auto-clicker started.");
  console.log("Run stopAutoLike() to stop.");

  loop();
})();


stopAutoLike()