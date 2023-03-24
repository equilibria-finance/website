var currentIndex = 0;
let prevScrollPos = window.pageYOffset;
let last = 0;
const innerContainer = document.querySelectorAll(".inner-container");

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
		if (currentIndex < 4 && !up) {
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
	event.preventDefault();
});

document.addEventListener("touchend", function () {
	if (endY < startY) {
		scroll(true);
	} else if (endY > startY) {
		scroll(false);
	}
});

window.onscroll = function (e) {
	var up = prevScrollPos > this.scrollY;
	prevScrollPos = this.scrollY;
	scroll(up);
};
