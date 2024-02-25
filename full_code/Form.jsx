import "./Form.css";

const Form = ({ children, mode, handleResponse, generatedValue}) => {
  const dummyTest = `Question 1: Multiple Choice (Instructive)
  What is the primary advantage of using Vertex AI for machine learning projects?
  A) It requires extensive coding knowledge.
  B) It automatically selects the best machine learning model and tunes parameters.
  C) It exclusively uses pre-existing models like Vision API.
  D) It only supports image classification projects.
  
  Question 2: True/False (Analytical)
  True or False: AutoML and Vertex AI eliminate the need for machine learning practitioners to understand the underlying details of machine learning models and algorithms.
  Rationale: This statement encourages students to think critically about the balance between the convenience of AutoML and the importance of foundational knowledge in machine learning, fostering an understanding of the tool's role in the broader context of ML development.
  
  Question 3: Short Answer (Reflective)
  How could the use of AutoML in a car manufacturing company's quality control process improve operational efficiency and product quality?
  Rationale: This question prompts students to apply lecture concepts to a real-world scenario, encouraging them to reflect on the practical applications and benefits of AutoML in industry-specific contexts, specifically in automating the differentiation between good and defective parts using specialized data.
  
  Question 4: Multiple Choice (Comprehensive)
  Which of the following is NOT a feature of AutoML as discussed in the lecture?A) Customizing models with specialized data without writing code.B) Training models exclusively on Google's pre-existing databases.C) Deploying models directly from the cloud.D) Analyzing documents and categorizing them using AutoML Natural Language.
  Rationale: This question assesses students' overall understanding of AutoML's capabilities and limitations, ensuring they grasp the breadth of features AutoML offers and recognize its flexibility beyond Google's pre-existing databases.
  
  Question 5: True/False (Diagnostic)
  True or False: AutoML's graphical user interfaces (GUIs) support only image classification and natural language processing projects."
  `;

  const handleSummarySubmit = async (event) => {
    event.preventDefault();
    console.log("submitted");
    const formData = new FormData(event.target);
    const transcript = formData.get('transcript'); // Assuming your form has an input with name='transcript'
  
    try {
      const summaryData = await fetchSummary(transcript);
      console.log('Summary:', summaryData);
      handleResponse(summaryData);
    } catch (error) {
      console.error('Could not fetch summary:', error);
    }
  };

  async function fetchSummary(transcript) {
    const response = await fetch('http://127.0.0.1:5000/create_summary', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ transcript: transcript })
    });
  
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  
    const data = await response.json();
    return data;
  }

  const handleTranscriptComprehension = async (event) => {
    event.preventDefault();
    console.log("submitted");
    const formData = new FormData(event.target);
    const transcript = formData.get('transcript'); // Assuming your form has an input with name='transcript'
  
    try {
      const testData = await fetchTest(transcript);
      console.log('Test:', testData);
      handleResponse(testData);
    } catch (error) {
      console.error('Could not fetch summary:', error);
    }
  };

  async function fetchTest(transcript) {
    const response = await fetch('http://127.0.0.1:5000/create_test', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ transcript: transcript })
    });
  
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  
    const data = await response.json();
    return data;
  }
  

  if (mode === "transcript") {
    return (
      <form onSubmit={handleTranscriptComprehension}>
        <textarea
          className="form-input transcript"
          name="transcript"
          placeholder="Enter transcript here..."
        ></textarea>
        {children}
      </form>
    );
  } else if (mode === "edit") {
    return (
      <form action="/submit-your-form-endpoint" method="">
        <textarea
          className="form-input edit"
          name="transcript"
          placeholder="Generated Test"
          value={generatedValue}
        ></textarea>
        {children}
      </form>
    );
  } else if (mode === "test") {
    return (
      <form action="/submit-your-form-endpoint" method="">
        <textarea
          className="form-input test"
          name="transcript"
          placeholder="Generated Test"
          value={dummyTest}
          disabled
        ></textarea>
        {children}
      </form>
    );
  } else if (mode === "summarise") {
    return (
      <form onSubmit={handleSummarySubmit}>
        <textarea
          className="form-input transcript"
          name="transcript"
          placeholder="Enter transcript here..."
        ></textarea>
        {children}
      </form>
    );
  } 
};

export default Form;
