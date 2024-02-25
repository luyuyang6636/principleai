import Card from "./Card";
import "./Home.css";

const Home = () => {
  const direct = () => {};
  return (
    <>
      <div className="big-container">
        <div className="header-container">
          <h1>principle.ai</h1>
          <p>Start transforming your teaching approach today.</p>
        </div>
        <div className="card-section">
          <Card imgSource={""} title={"Note Generation"} onClick={direct} />
          <Card imgSource={""} title={"Comprehension Test"} onClick={""} />
          <Card imgSource={""} title={"Keyword Finder"} onClick={""} />
        </div>
      </div>
    </>
  );
};

export default Home;
