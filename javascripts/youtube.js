function makeYoutubeAutoplay(elementId, videoId) {
  player = new YT.Player(elementId, {
    height: '390',
    width: '640',
    videoId: videoId,
    modestbranding: 1,
    events: {
      'onReady': onPlayerReady,
    }
  });
  player.hasStarted = false;

  players.push([player, elementId])

  // The API will call this function when the video player is ready.
  function onPlayerReady(event) {
    event.target.mute();
  }
}

/** @author http://stackoverflow.com/a/7557433/1684970 */
function isElementInViewport(el) {
  if (typeof jQuery === "function" && el instanceof jQuery) el = el[0];
  var rect = el.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}
