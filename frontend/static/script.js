// Function to toggle the review form visibility
function toggleReviewForm() {
    var form = document.getElementById("review-form");
    if (form.style.display === "none") {
        form.style.display = "block";  // Show the form
    } else {
        form.style.display = "none";  // Hide the form
    }
}

// Set the rating when a star is clicked
var stars = document.querySelectorAll("#rating-stars .star");

stars.forEach(function(star) {
    star.addEventListener("click", function() {
        var rating = this.getAttribute("data-value");
        document.getElementById("rating").value = rating;  // Set the hidden input's value
        updateStarDisplay(rating);  // Update the visual display of stars
    });

    // Add hover effect on star
    star.addEventListener("mouseover", function() {
        var rating = this.getAttribute("data-value");
        updateStarDisplayOnHover(rating);
    });

    // Reset stars when mouse leaves
    star.addEventListener("mouseout", function() {
        var currentRating = document.getElementById("rating").value;
        updateStarDisplay(currentRating);  // Reset to the current rating if hovering ends
    });
});

function updateStarDisplay(rating) {
    stars.forEach(function(star) {
        var starValue = star.getAttribute("data-value");
        if (starValue <= rating) {
            star.style.color = "#FFD700";  // Highlight the star if it's part of the rating
        } else {
            star.style.color = "#ccc";  // Reset the star to default
        }
    });
}

// Function to update the star display when hovering (before clicking)
function updateStarDisplayOnHover(rating) {
    stars.forEach(function(star) {
        var starValue = star.getAttribute("data-value");
        if (starValue <= rating) {
            star.style.color = "#FFD700";  // Highlight the star on hover
        } else {
            star.style.color = "#ccc";  // Reset the star on hover leave
        }
    });
}

// Function to initialize the stars based on the current rating (if available)
function initializeStars() {
    var currentRating = document.getElementById("rating").value;
    if (currentRating) {
        updateStarDisplay(currentRating);  // Apply the current rating on page load
    }
}

// Call initializeStars when the page loads
document.addEventListener("DOMContentLoaded", initializeStars);
