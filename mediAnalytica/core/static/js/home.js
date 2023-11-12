const container = document.getElementById("lottie-container");
// Configuration options for the Lottie animation
const animationConfig = {
    container: container, // The container element
    renderer: "svg", // Choose the rendering mode (svg, canvas, html)
    loop: true, // Set to true for a looping animation
    autoplay: true, // Set to true to start the animation automatically
    path: "../static/animation_lobf8rfw.json", // Path to your JSON animation file
};
// Create a Lottie animation by passing the configuration
const anim = lottie.loadAnimation(animationConfig);