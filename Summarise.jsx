import "./Summarise.css";
import Header from "./Header";
import Desc from "./Desc";
import Form from "./Form";
import Button from "./Button";
// import ContentDisplay from "./ContentDisplay"
import { useState } from "react";

const Summarise = () => {
  const [response, setResponse] = useState("");

  const handleResponse = (output) => {
    setResponse(output.message);
  };

  if (response !== "") {
    return (
      <div className="big-container">
        <div className="header-container">
          <Desc write={"Summarised Text"} />
        </div>
        <div
          className="response-body"
          dangerouslySetInnerHTML={{
            __html: response.split("classname=").join("class="),
          }}
        />
        <Button name={"Back"} onClick={() => setResponse("")} />
      </div>
    );
  } else {
    return (
      <>
        <div className="header-container">
          <Header />
          <Desc write={"Summarise Text"} />
        </div>
        <div className="form-container">
          <Form mode="summarise" handleResponse={handleResponse}>
            <Button name="summarise" />
          </Form>
        </div>
      </>
    );
  }
};

export default Summarise;
