import Header from "./Header";
import Desc from "./Desc";
import Button from "./Button";
import Form from "./Form";
import Testname from "./SectionName";
import { useState } from "react";
import "./App.css";

function App() {
  const [pageIndex, setPageIndex] = useState(0);

  const changePageIndex = (n) => {
    if (n !== 0) {
      setPageIndex((prevPageIndex) => prevPageIndex + n);
    } else {
      setPageIndex(0);
    }
  };

  if (pageIndex === 0) {
    return (
      <>
        <div className="header-container">
          <Header />
          <Desc write={"Comprehension Test"}/>
        </div>
        <div className="form-container">
          <Form mode="transcript">
            <Button name="create" onClick={() => changePageIndex(1)} />
          </Form>
        </div>
      </>
    );
  } else if (pageIndex === 1) {
    return (
      <>
        <div className="header-container">
          <Header />
          <Testname subjectName={"Test for History"} />
        </div>
        <div className="form-container">
          <Form mode={"edit"}>
            <div className="button-section">
              <Button name="back" onClick={(e) => changePageIndex(0, e)} />
              <Button
                name="regenerate"
                onClick={(e) => changePageIndex(1, e)}
              />
              <Button name="run test" onClick={(e) => changePageIndex(1, e)} />
            </div>
          </Form>
        </div>
      </>
    );
  } else if (pageIndex === 2) {
    return (
      <>
        <div className="header-container">
          <Header />
          <Testname text={"Test for History"} />
        </div>
        <div className="form-container">
          <Form mode={"test"}>
            <Button name="submit test" onClick={(e) => changePageIndex(1, e)} />
          </Form>
        </div>
      </>
    );
  } else if (pageIndex === 3) {
    return (
      <>
        <div className="header-container">
          <Header />
          <Testname text={"Analysis"} />
        </div>
        <div className="form-container">
          <Form mode={"test"}>
            <div className="button-section">
              <Button
                name="back to main page"
                onClick={(e) => changePageIndex(0, e)}
              />
              <Button
                name="save to Notes"
                onClick={() => console.log("Saved to notes")}
              />
            </div>
          </Form>
        </div>
      </>
    );
  }
}

export default App;