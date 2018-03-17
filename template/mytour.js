// Create a new tour
var tour = new Tour();

// Add your steps
tour.addSteps([
  {
    element: ".message.message-1", // element selector to show the popover next to;
    title: "Welcome to ai.tutor!",
    content: "We're going to make this quick and useful."
  },
  {
    element: ".message.message-2",
    title: "Let's finish this thing off with a bang.",
    content: "Boom, bang, bam!"
  }
]);

// Initialize method on the Tour class. Get's everything loaded up and ready to go.
tour.init();

// This starts the tour itself
tour.start();
