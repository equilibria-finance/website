var currentIndex = 0;
let prevScrollPos = window.pageYOffset;
let last = 0;
const innerContainer = document.querySelectorAll(".inner-container");
const sidebarContainer = document.getElementById(
	"side-bar-container"
);

document.getElementById("hamburger").addEventListener("click", () => {
	document.body.style.overflow = "hidden";
	sidebarContainer.classList.add("side-bar-show");
	sidebarContainer.classList.remove("side-bar-hide");
});
document.getElementById("close").addEventListener("click", () => {
	document.body.style.overflow = "auto";
	sidebarContainer.classList.add("side-bar-hide");
	sidebarContainer.classList.remove("side-bar-show");
});

function scrollToSmoothly(pos, time) {
	var currentPos = window.pageYOffset;
	var start = null;
	if (time == null) time = 500;
	(pos = +pos), (time = +time);
	window.requestAnimationFrame(function step(currentTime) {
		start = !start ? currentTime : start;
		var progress = currentTime - start;
		if (currentPos < pos) {
			window.scrollTo(
				0,
				((pos - currentPos) * progress) / time + currentPos
			);
		} else {
			window.scrollTo(
				0,
				currentPos - ((currentPos - pos) * progress) / time
			);
		}
		if (progress < time) {
			window.requestAnimationFrame(step);
		} else {
			window.scrollTo(0, pos);
		}
	});
}

var element, rect, position;

scroll = (up) => {
	const now = new Date().getTime();
	if (now - last > 1000) {
		last = now;
		if (currentIndex > 0 && up) {
			innerContainer[currentIndex].classList.add("hide");
			setTimeout(() => {
				innerContainer[currentIndex + 1].classList.remove("active");
				innerContainer[currentIndex + 1].classList.remove("hide");
			}, 500);
			currentIndex--;
			element = document.getElementById(`${currentIndex}-container`);
			rect = element.getBoundingClientRect();
			position = rect.top + window.scrollY;
			innerContainer[currentIndex].classList.add("active");
			scrollToSmoothly(position, 500);
		}
		if (currentIndex + 1 < 6 && !up) {
			innerContainer[currentIndex].classList.add("hide");
			setTimeout(() => {
				innerContainer[currentIndex - 1].classList.remove("active");
				innerContainer[currentIndex - 1].classList.remove("hide");
			}, 500);
			currentIndex++;
			element = document.getElementById(`${currentIndex}-container`);
			rect = element.getBoundingClientRect();
			position = rect.top + window.scrollY;
			innerContainer[currentIndex].classList.add("active");
			scrollToSmoothly(position, 500);
		}
	}
};

var startY, endY;

document.addEventListener("touchstart", function (event) {
	startY = event.touches[0].clientY;
});

document.addEventListener("touchmove", function (event) {
	endY = event.touches[0].clientY;
});

document.addEventListener("touchend", function (event) {
	if (startY != 0 && endY != 0) {
		if (startY - endY > 20) {
			scroll(false);
		} else if (endY - startY > 20) {
			scroll(true);
		}
	}
	startY = 0;
	endY = 0;
});

window.onscroll = function (e) {
	var up = prevScrollPos > this.scrollY;
	prevScrollPos = this.scrollY;
	scroll(up);
};
document
	.getElementById("show-more-btn")
	.addEventListener("click", () => {
		currentIndex = 0;
		scroll(false);
	});

document.addEventListener("DOMContentLoaded", function () {
	var fullURL = window.location.href;
	if (fullURL.includes("#")) {
		var sectionID = fullURL.split("#")[1];
		if (sectionID == "whitepaper") {
			currentIndex = 2;
			scroll(false);
		}
	}
});
