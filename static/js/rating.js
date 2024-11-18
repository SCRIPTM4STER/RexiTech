const ratingInput = document.getElementById('rating');
const starsFilled = document.querySelector('.stars-icons-filled');
const maxRate = parseFloat(ratingInput.max);
const starSize = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--star-size'));

ratingInput.addEventListener('input', function () {
    // Get the current value of the input
    const ratingValue = parseFloat(ratingInput.value);
    
    // Calculate the width based on the rating
    const filledWidth = Math.round(ratingValue * starSize);

    // Update the width of the filled stars
    starsFilled.style.width = `${filledWidth}px`;
});


