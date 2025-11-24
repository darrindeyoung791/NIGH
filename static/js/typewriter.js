// Typewriter effect for simulating AI responses in chat interface
class ChatTypewriter {
  constructor(element, options = {}) {
    this.element = element;
    this.text = options.text || '';
    this.delay = options.delay || 50;
    this.startDelay = options.startDelay || 1000;
    this.onComplete = options.onComplete || null;
  }

  async type() {
    // Add a delay before starting to simulate thinking
    await this.wait(this.startDelay);

    // Clear the element
    this.element.innerHTML = '';

    // Type each character
    for (let i = 0; i < this.text.length; i++) {
      this.element.innerHTML += this.text.charAt(i);
      await this.wait(this.delay);
    }

    // Call the complete callback if provided
    if (this.onComplete) {
      this.onComplete();
    }
  }

  async wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Reset the typewriter to initial state
  reset() {
    this.element.innerHTML = '';
  }
}

// Initialize chat interface with Intersection Observer
document.addEventListener('DOMContentLoaded', function() {
  const aiResponseElement = document.querySelector('.ai-typing-text');
  if (aiResponseElement) {
    const chatContainer = document.querySelector('.ai-insights-section');

    // Create a new typewriter instance
    const createTypewriter = () => {
      return new ChatTypewriter(aiResponseElement, {
        text: "好的，根据数据库，以下是满足您要求的几所学校：\n\n1. 英国国家文理中学\n是英国唯一纯STEM私立高中，与空客、阿斯顿·马丁等企业签有协议，课程内容紧贴行业需求，学生参与真实项目机会多，创业孵化生态活跃。\n\n……",
        delay: 30, // Speed of typing
        startDelay: 1000, // Initial delay before typing starts (simulating AI processing)
        onComplete: function() {
          console.log('Chat typewriter effect completed');
        }
      });
    };

    // Set up Intersection Observer
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Reset and start the typewriter when the section comes into view
          const typewriter = createTypewriter();
          typewriter.reset();
          typewriter.type();
        }
      });
    }, {
      threshold: 0.5 // Trigger when 50% of the element is visible
    });

    // Start observing the AI insights section
    if (chatContainer) {
      observer.observe(chatContainer);
    }
  }
});